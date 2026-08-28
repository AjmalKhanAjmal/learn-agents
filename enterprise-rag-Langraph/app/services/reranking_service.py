from app.core.logger import logger
# from app.core.exceptions import RerankingServiceError
from app.schemas.retrieval import RetrievedChunk



class RerankingService:

    def __init__(
        self,
        reranker
    ):

        self.reranker = reranker

    def rerank(
        self,
        query: str,
        documents: list[RetrievedChunk],
        top_k: int = 5
    ):

        if top_k <= 0:

            # raise RerankingServiceError(
            #     "top_k must be greater than zero."
            # )

        if not documents:

            logger.info(
                "No documents available for reranking."
            )

            return []

        try:

            logger.info(
                "Starting reranking service."
            )

            reranked = self.reranker.rerank(
                query=query,
                documents=documents
            )

            final_results = []

            for document, rerank_score in reranked[:top_k]:

                final_results.append(
                    {
                        "chunk_id":document.chunk_id,
                        "content":document.content,
                        "retrieval_score":document.score,
                        "rerank_score":rerank_score,
                        "metadata":{
                            **document.metadata
                        }
                    }
                )

            logger.info(
                "Reranking service completed. "
                "Returning %d results.",
                len(final_results)
            )

            return final_results

        except Exception as error:

            logger.exception(
                "Reranking service failed."
            )

            # raise RerankingServiceError(
            #     f"Reranking failed: {error}"
            # ) from error