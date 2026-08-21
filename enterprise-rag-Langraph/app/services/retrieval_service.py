from app.core.logger import logger
from app.core.exceptions import RetrievalServiceError
from app.schemas.retrieval import RetrievalResponse


class RetrievalService:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def retrieve(
        self,
        query: str,
        tenant_id,
        document_id,
        top_k: int = 3,
        score_threshold: float | None = None,
    ):
        try:
            metadata_filter = {}
            if tenant_id is not None or "":
                metadata_filter["tenant_id"] = tenant_id
            if document_id is not None or "":
                metadata_filter["document_id"] = document_id

            logger.info("Started retrivel for query")
            results = self.vector_store.similarity_search(
                query, metadata_filter, top_k, score_threshold
            )
            logger.info("Retrieving completed ", len(results))

            return results
        # {
        #         "query": query,
        #         "data": results,
        #         "secret": "THIS SHOULD NOT BE IN PUBLIC RESPONSE",
        #     }
        # return RetrievalResponse(query=query)

        except Exception as error:
            logger.error("Error while retriving , ", str(error))
            # raise error
            raise RetrievalServiceError(f"Error while retrieving: {str(error)}")
