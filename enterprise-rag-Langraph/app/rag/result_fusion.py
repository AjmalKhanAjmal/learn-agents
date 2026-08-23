from app.core.logger import logger
from app.schemas.retrieval import RetrievedChunk


class ResultFusionService:

    def __init__(
        self,
        rrf_constant: int = 60
    ):

        self.rrf_constant = rrf_constant

    def fuse(
        self,
        semantic_results: list[RetrievedChunk],
        keyword_results: list[RetrievedChunk],
        top_k: int = 5
    ) -> list[RetrievedChunk]:

        logger.info(
            "Starting RRF result fusion."
        )

        scores = {}

        chunks = {}

        self._process_results(
            semantic_results,
            scores,
            chunks
        )

        self._process_results(
            keyword_results,
            scores,
            chunks
        )

        ranked_results = sorted(
            chunks.values(),
            key=lambda chunk: scores[chunk.chunk_id],
            reverse=True
        )

        final_results = []

        for chunk in ranked_results[:top_k]:

            chunk.metadata = {
                **chunk.metadata,
                "rrf_score": scores[chunk.chunk_id]
            }

            final_results.append(
                chunk
            )

        logger.info(
            "RRF fusion completed. Returning %d chunks.",
            len(final_results)
        )

        return final_results

    def _process_results(
        self,
        results: list[RetrievedChunk],
        scores: dict[str, float],
        chunks: dict[str, RetrievedChunk]
    ):

        for rank, chunk in enumerate(
            results,
            start=1
        ):

            chunk_id = chunk.chunk_id

            rrf_score = (
                1.0 /
                (
                    self.rrf_constant +
                    rank
                )
            )

            if chunk_id not in scores:

                scores[chunk_id] = 0.0

            scores[chunk_id] += rrf_score

            if chunk_id not in chunks:

                chunks[chunk_id] = chunk