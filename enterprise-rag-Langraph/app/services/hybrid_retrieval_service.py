from abc import abstractmethod, ABC


class BaseHybridRetriever(ABC):
    @abstractmethod
    def hybrid_retrievel(self):
        pass


class HybridRetrievalService(BaseHybridRetriever):
    def __init__(self, vector_store, keyword_store):
        self.vector_store = vector_store
        self.keyword_store = keyword_store
        