from abc import ABC, abstractmethod

from app.schemas.retrieval import RetrievedChunk


class BaseReranker(ABC):
    @abstractmethod
    def rerank(
        self, query: str, documents: list[RetrievedChunk]
    ) -> list[tuple[RetrievedChunk, float]]:
        pass
