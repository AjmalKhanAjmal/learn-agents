from sentence_transformers import CrossEncoder

from app.core.logger import logger
from app.rerankers.base import BaseReranker
from app.schemas.retrieval import RetrievedChunk


class CrossEncoderReranker(BaseReranker):
    
    def __init__(self,model_name:str,max_length:int = 512,batch_size:int = 16):
        self.model_name =model_name
        self.max_length = max_length
        self.batch_size = batch_size
        
        try:
            logger.info("Loading ranker model ", self.model_name)
            self.model = CrossEncoder(model_name,max_length=max_length)
            logger.info(
                "Reranker model loaded successfully."
            )
        except Exception as error:
            raise error
        
    def rerank(self,query:str,documents:list[RetrievedChunk]) -> list[tuple[RetrievedChunk, float]]:
            try:
                logger.info("starting reranking for %d documents",len(documents))
                # pairs 
                
                
                
                pairs = [
                [query, document.content]
                for document in documents
            ]
                
            except Exception as error:
                raise error            
        
        
        
    
#     from sentence_transformers import CrossEncoder

# from app.core.logger import logger
# from app.core.exceptions import RerankerError
# from app.models.retrieved_chunk import RetrievedChunk
# from app.rerankers.base import BaseReranker


# class CrossEncoderReranker(BaseReranker):

#     def __init__(
#         self,
#         model_name: str,
#         batch_size: int = 16,
#         max_length: int = 512
#     ):

#         self.model_name = model_name
#         self.batch_size = batch_size
#         self.max_length = max_length

#         try:

#             logger.info(
#                 "Loading reranker model: %s",
#                 model_name
#             )

#             self.model = CrossEncoder(
#                 model_name,
#                 max_length=max_length
#             )

#             logger.info(
#                 "Reranker model loaded successfully."
#             )

#         except Exception as error:

#             logger.exception(
#                 "Failed to load reranker model."
#             )

#             raise RerankerError(
#                 f"Failed to load reranker model: {error}"
#             ) from error

    # def rerank(
    #     self,
    #     query: str,
    #     documents: list[RetrievedChunk]
    # ) -> list[tuple[RetrievedChunk, float]]:

    #     if not query.strip():

    #         raise RerankerError(
    #             "Query cannot be empty."
    #         )

    #     if not documents:

    #         return []

    #     try:

    #         logger.info(
    #             "Starting reranking for %d documents.",
    #             len(documents)
    #         )

    #         pairs = [
    #             [query, document.content]
    #             for document in documents
    #         ]

    #         scores = self.model.predict(
    #             pairs,
    #             batch_size=self.batch_size,
    #             show_progress_bar=False
    #         )

    #         reranked = [
    #             (document, float(score))
    #             for document, score in zip(
    #                 documents,
    #                 scores
    #             )
    #         ]

    #         reranked.sort(
    #             key=lambda item: item[1],
    #             reverse=True
    #         )

    #         logger.info(
    #             "Reranking completed."
    #         )

    #         return reranked

    #     except Exception as error:

    #         logger.exception(
    #             "Reranking failed."
    #         )

    #         raise RerankerError(
    #             f"Reranking failed: {error}"
    #         ) from error
    