from abc import abstractmethod, ABC


class BaseHybridRetriever(ABC):
    @abstractmethod
    def hybrid_retrievel(self):
        pass


class HybridRetrievalService(BaseHybridRetriever):
    def __init__(self, vector_store, keyword_store):
        self.vector_store = vector_store
        self.keyword_store = keyword_store
    
    def hybrid_retrievel(self,query,top_k):
        try:
            symantic_results =  self.vector_store.similarity_search(
                            query=query,
                            top_k=top_k
                        )
                    
            keyword_results = self.keyword_store.search (query = query,
                    top_k=top_k)
            
            # hybrid_results = {
            #     symantic_results,
            #     keyword_results
            # }
            
            hybrid_results = {
                          "symantic_results":  symantic_results,
                            "keyword_results":keyword_results
                        }
            
            return hybrid_results
                    
        except Exception as error:
            raise error