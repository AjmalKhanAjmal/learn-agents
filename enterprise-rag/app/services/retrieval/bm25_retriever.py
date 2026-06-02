"""
BM25 retrieval service.

Maintains an in-process BM25 index over all indexed chunk texts.
The index is rebuilt whenever new chunks are registered.

For production at scale, replace with a dedicated search service
(Elasticsearch / OpenSearch) that persists state across restarts.
"""
from __future__ import annotations

import re
import threading
from typing import Any

from rank_bm25 import BM25Okapi  # type: ignore

from app.core.logging import get_logger

logger = get_logger(__name__)


class BM25Retriever:
    """
    Thread-safe BM25 index over document chunks.

    Usage
    -----
    retriever = BM25Retriever()
    retriever.add_chunks(chunks_with_metadata)   # call after indexing
    results = retriever.search("your query", top_k=20)
    """

    _TOKENISE_RE = re.compile(r"\b\w+\b", re.UNICODE)

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._corpus: list[list[str]] = []          # tokenised texts
        self._metadata: list[dict[str, Any]] = []   # parallel metadata list
        self._bm25: BM25Okapi | None = None

    # ── Index management ───────────────────────────────────────────────────────

    def add_chunks(self, chunks: list[dict[str, Any]]) -> None:
        """
        Add chunks to the BM25 index.

        Parameters
        ----------
        chunks : list of dicts with at least keys:
                 'chunk_id', 'document_id', 'text', and optionally 'filename'.
        """
        if not chunks:
            return

        with self._lock:
            for c in chunks:
                tokens = self._tokenise(c["text"])
                self._corpus.append(tokens)
                self._metadata.append(c)

            self._bm25 = BM25Okapi(self._corpus)
            logger.info("bm25_index_updated", total_chunks=len(self._corpus))

    def remove_by_document(self, document_id: str) -> int:
        """Remove all chunks belonging to *document_id*. Returns removed count."""
        with self._lock:
            keep_idx = [
                i for i, m in enumerate(self._metadata)
                if m.get("document_id") != document_id
            ]
            removed = len(self._metadata) - len(keep_idx)
            if removed == 0:
                return 0

            self._corpus = [self._corpus[i] for i in keep_idx]
            self._metadata = [self._metadata[i] for i in keep_idx]
            self._bm25 = BM25Okapi(self._corpus) if self._corpus else None

            logger.info(
                "bm25_chunks_removed",
                document_id=document_id,
                removed=removed,
                remaining=len(self._corpus),
            )
            return removed

    def clear(self) -> None:
        with self._lock:
            self._corpus.clear()
            self._metadata.clear()
            self._bm25 = None

    # ── Search ─────────────────────────────────────────────────────────────────

    def search(
        self,
        query: str,
        top_k: int = 20,
        document_ids: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """
        BM25 keyword search.

        Parameters
        ----------
        query        : natural language query
        top_k        : maximum results to return
        document_ids : optional allowlist — restrict to specific documents

        Returns
        -------
        List of dicts: {chunk_id, document_id, filename, text, bm25_score, rank}
        Sorted descending by BM25 score.
        """
        with self._lock:
            if self._bm25 is None or not self._corpus:
                logger.warning("bm25_index_empty")
                return []

            query_tokens = self._tokenise(query)
            if not query_tokens:
                return []

            scores: list[float] = self._bm25.get_scores(query_tokens).tolist()

        # Build result list (outside lock for speed)
        scored: list[tuple[float, dict[str, Any]]] = []
        for score, meta in zip(scores, self._metadata):
            if document_ids and meta.get("document_id") not in document_ids:
                continue
            if score > 0:
                scored.append((score, meta))

        scored.sort(key=lambda x: x[0], reverse=True)
        top = scored[:top_k]

        results = []
        for rank, (score, meta) in enumerate(top, start=1):
            results.append(
                {
                    "chunk_id": meta["chunk_id"],
                    "document_id": meta.get("document_id", ""),
                    "filename": meta.get("filename", "unknown"),
                    "text": meta["text"],
                    "bm25_score": round(score, 6),
                    "rank": rank,
                }
            )

        logger.debug("bm25_search_done", query_tokens=len(query_tokens), returned=len(results))
        return results

    @property
    def index_size(self) -> int:
        return len(self._corpus)

    # ── Tokenisation ───────────────────────────────────────────────────────────

    def _tokenise(self, text: str) -> list[str]:
        """Lowercase word tokenisation. Extend here for stemming/stop-words."""
        return self._TOKENISE_RE.findall(text.lower())


# ── Application-wide singleton ─────────────────────────────────────────────────
_bm25_retriever: BM25Retriever | None = None


def get_bm25_retriever() -> BM25Retriever:
    global _bm25_retriever
    if _bm25_retriever is None:
        _bm25_retriever = BM25Retriever()
    return _bm25_retriever