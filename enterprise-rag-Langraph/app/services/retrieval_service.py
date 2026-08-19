from app.core.logger import logger
from app.core.exceptions import RetrievalServiceError
from app.schemas.retrieval import RetrievalResponse


class RetrievalService:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def retrieve(
        self, query: str, top_k: int = 3, score_threshold: float | None = None
    ):
        try:
            logger.info("Started retrivel for query")
            results = self.vector_store.similarity_search(query, top_k, score_threshold)
            logger.info("Retrieving completed ", len(results))
            # return results
            return RetrievalResponse(query=query, data=results)
        except Exception as error:
            logger.error("Error while retriving , ", str(error))
            # raise error
            raise RetrievalServiceError(f"Error while retrieving: {str(error)}")
