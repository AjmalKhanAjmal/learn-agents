from abc import abstractmethod, ABC

from app.schemas.retrieval import RetrievedChunk


class BaseHybridRetriever(ABC):
    @abstractmethod
    def hybrid_retrievel(self):
        pass


class HybridRetrievalService(BaseHybridRetriever):
    def __init__(
        self,
        vector_store,
        keyword_store,
        fusion_service,
        rerank_service_obj,
        llm_service,
    ):
        self.vector_store = vector_store
        self.keyword_store = keyword_store
        self.fusion_service = fusion_service
        self.rerank_service_obj = rerank_service_obj
        self.llm_service = llm_service

    async def hybrid_retrievel(self, query, top_k):
        try:
            semantic_results = self.vector_store.similarity_search(
                query=query, top_k=top_k
            )
            final_semantic_results = []
            for document, score in semantic_results:
                final_semantic_results.append(
                    RetrievedChunk(
                        chunk_id=document.metadata["chunk_id"],
                        content=document.page_content,
                        score=float(score),
                        metadata=document.metadata,
                    )
                )

            keyword_results = self.keyword_store.search(query=query, top_k=top_k)

            # hybrid_results = {
            #     symantic_results,
            #     keyword_results
            # }

            hybrid_results = {
                "symantic_results": semantic_results,
                "keyword_results": keyword_results,
            }
            fused_results = self.fusion_service.fuse(
                semantic_results=final_semantic_results,
                keyword_results=keyword_results,
                top_k=top_k,
            )

            reranked_results = self.rerank_service_obj.rerankService(
                query, fused_results
            )

            from app.services.context_compressor import ContextCompressor

            compressor = ContextCompressor(
                embedding_model="all-MiniLM-L6-v2",
                similarity_threshold=0.40,
                max_tokens=1000,
                preserve_neighbors=True,
            )

            compressed_results = compressor.compress(
                query=query, documents=reranked_results
            )

            final_results = await self.llm_service.generation_service(
                max_output_tokens=200, temperature=0.3, documents=compressed_results
            )
            return final_results
            # return compressed_results
            # return hybrid_results

        except Exception as error:
            raise error
