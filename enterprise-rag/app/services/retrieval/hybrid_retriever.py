"""
Hybrid Retrieval + Cross-Encoder Reranking pipeline.

Pipeline
--------
1.  Dense retrieval  — cosine similarity via Pinecone
2.  BM25 retrieval   — keyword match via rank-bm25
3.  Score fusion     — Reciprocal Rank Fusion (RRF) weighted merge
4.  Cross-encoder    — pointwise reranking of fused candidates
5.  Top-k selection  — return the k highest-reranked chunks
"""
from __future__ import annotations

import time
from functools import lru_cache
from typing import Any

from app.core.config import settings
from app.core.exceptions import RetrievalError
from app.core.logging import get_logger
from app.models.schemas import RetrievedChunk
from app.services.embedding.embedder import EmbeddingService
from app.services.retrieval.bm25_retriever import BM25Retriever
from app.services.retrieval.vector_store import VectorStore

logger = get_logger(__name__)

# RRF constant — 60 is the widely-used default
_RRF_K = 60


class HybridRetriever:
    """
    Combines dense and sparse retrieval with cross-encoder reranking.

    Parameters
    ----------
    vector_store   : Pinecone-backed dense retriever
    bm25_retriever : In-process BM25 sparse retriever
    embedder       : Sentence-transformer embedding service
    dense_weight   : Score weight for dense results in RRF fusion (0-1)
    bm25_weight    : Score weight for BM25 results in RRF fusion (0-1)
    """

    def __init__(
        self,
        vector_store: VectorStore,
        bm25_retriever: BM25Retriever,
        embedder: EmbeddingService,
        dense_weight: float | None = None,
        bm25_weight: float | None = None,
    ) -> None:
        self.vector_store = vector_store
        self.bm25_retriever = bm25_retriever
        self.embedder = embedder
        self.dense_weight = dense_weight or settings.dense_weight
        self.bm25_weight = bm25_weight or settings.bm25_weight
        self._reranker = None  # lazy loaded

    # ── Public ─────────────────────────────────────────────────────────────────

    def retrieve(
        self,
        query: str,
        top_k: int | None = None,
        filters: dict[str, Any] | None = None,
    ) -> list[RetrievedChunk]:
        """
        Full hybrid → rerank pipeline.

        Returns top_k chunks sorted by reranker score (highest first).
        """
        top_k = top_k or settings.top_k_rerank
        t0 = time.monotonic()

        # ── Step 1: Dense retrieval ────────────────────────────────────────────
        query_vec = self.embedder.embed_query(query)
        dense_results = self.vector_store.query(
            query_vector=query_vec,
            top_k=settings.top_k_dense,
            filters=filters,
        )
        logger.debug("dense_retrieved", count=len(dense_results))

        # ── Step 2: BM25 retrieval ─────────────────────────────────────────────
        bm25_results = self.bm25_retriever.search(
            query=query,
            top_k=settings.top_k_bm25,
        )
        logger.debug("bm25_retrieved", count=len(bm25_results))

        # ── Step 3: RRF score fusion ───────────────────────────────────────────
        fused = self._reciprocal_rank_fusion(dense_results, bm25_results)
        if not fused:
            logger.warning("hybrid_retrieval_empty", query=query[:80])
            return []

        # ── Step 4: Cross-encoder reranking ───────────────────────────────────
        reranked = self._rerank(query, fused, top_k)

        elapsed_ms = (time.monotonic() - t0) * 1000
        logger.info(
            "retrieval_complete",
            dense=len(dense_results),
            bm25=len(bm25_results),
            fused=len(fused),
            reranked=len(reranked),
            elapsed_ms=round(elapsed_ms, 1),
        )
        return reranked

    # ── RRF Fusion ─────────────────────────────────────────────────────────────

    def _reciprocal_rank_fusion(
        self,
        dense: list[dict[str, Any]],
        bm25: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """
        Weighted Reciprocal Rank Fusion.

        RRF score = Σ  weight_i / (k + rank_i)

        Merges both result sets into a single ranked list, deduplicating
        by chunk_id and carrying forward the full metadata.
        """
        scores: dict[str, float] = {}
        meta_store: dict[str, dict[str, Any]] = {}

        # Dense results (rank = position in Pinecone result list, 1-indexed)
        for rank, item in enumerate(dense, start=1):
            cid = item["id"]
            rrf = self.dense_weight / (_RRF_K + rank)
            scores[cid] = scores.get(cid, 0.0) + rrf
            if cid not in meta_store:
                meta_store[cid] = {
                    "chunk_id": cid,
                    "document_id": item["metadata"].get("document_id", ""),
                    "filename": item["metadata"].get("filename", "unknown"),
                    "text": item["metadata"].get("text", ""),
                    "metadata": item["metadata"],
                    "sources": ["dense"],
                    "dense_score": item["score"],
                }
            else:
                meta_store[cid]["sources"].append("dense")

        # BM25 results
        for rank, item in enumerate(bm25, start=1):
            cid = item["chunk_id"]
            rrf = self.bm25_weight / (_RRF_K + rank)
            scores[cid] = scores.get(cid, 0.0) + rrf
            if cid not in meta_store:
                meta_store[cid] = {
                    "chunk_id": cid,
                    "document_id": item.get("document_id", ""),
                    "filename": item.get("filename", "unknown"),
                    "text": item.get("text", ""),
                    "metadata": {},
                    "sources": ["bm25"],
                    "bm25_score": item["bm25_score"],
                }
            else:
                meta_store[cid]["sources"].append("bm25")
                meta_store[cid]["bm25_score"] = item["bm25_score"]

        # Sort by fused RRF score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        fused = []
        for rank, (cid, rrf_score) in enumerate(ranked, start=1):
            entry = {**meta_store[cid], "rrf_score": rrf_score, "fused_rank": rank}
            fused.append(entry)

        return fused

    # ── Cross-encoder reranking ────────────────────────────────────────────────

    @property
    def reranker(self):
        """Lazy-load the cross-encoder model."""
        if self._reranker is None:
            try:
                from sentence_transformers import CrossEncoder  # type: ignore
                logger.info("loading_reranker", model=settings.reranker_model)
                self._reranker = CrossEncoder(
                    settings.reranker_model,
                    max_length=512,
                    device=settings.embedding_device,
                )
                logger.info("reranker_loaded")
            except Exception as exc:
                logger.error("reranker_load_failed", error=str(exc))
                raise RetrievalError(f"Failed to load cross-encoder: {exc}") from exc
        return self._reranker

    def _rerank(
        self,
        query: str,
        candidates: list[dict[str, Any]],
        top_k: int,
    ) -> list[RetrievedChunk]:
        """
        Score each (query, passage) pair with the cross-encoder and return
        the top_k passages sorted by pointwise relevance score.
        """
        if not candidates:
            return []

        pairs = [[query, c["text"]] for c in candidates]

        try:
            ce_scores: list[float] = self.reranker.predict(pairs, show_progress_bar=False).tolist()
        except Exception as exc:
            logger.warning("reranker_failed_fallback_to_rrf", error=str(exc))
            # Graceful fallback: use RRF scores directly
            ce_scores = [c["rrf_score"] for c in candidates]

        # Attach CE score and sort
        scored = sorted(
            zip(ce_scores, candidates),
            key=lambda x: x[0],
            reverse=True,
        )

        results: list[RetrievedChunk] = []
        for final_rank, (ce_score, chunk_meta) in enumerate(scored[:top_k], start=1):
            sources = chunk_meta.get("sources", [])
            if len(set(sources)) > 1:
                method = "hybrid"
            elif "dense" in sources:
                method = "dense"
            else:
                method = "bm25"

            results.append(
                RetrievedChunk(
                    chunk_id=chunk_meta["chunk_id"],
                    document_id=chunk_meta["document_id"],
                    filename=chunk_meta.get("filename", "unknown"),
                    text=chunk_meta["text"],
                    score=round(float(ce_score), 6),
                    rank=final_rank,
                    retrieval_method=method,
                    metadata={
                        **chunk_meta.get("metadata", {}),
                        "rrf_score": chunk_meta.get("rrf_score", 0.0),
                        "dense_score": chunk_meta.get("dense_score"),
                        "bm25_score": chunk_meta.get("bm25_score"),
                    },
                )
            )

        return results


@lru_cache(maxsize=1)
def get_hybrid_retriever() -> HybridRetriever:
    """Application-wide singleton — avoids re-loading the cross-encoder."""
    from app.services.embedding.embedder import get_embedding_service
    from app.services.retrieval.bm25_retriever import get_bm25_retriever

    return HybridRetriever(
        vector_store=VectorStore(),
        bm25_retriever=get_bm25_retriever(),
        embedder=get_embedding_service(),
    )