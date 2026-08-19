from abc import ABC, abstractmethod

# from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain_core.documents import Document
from app.core.config import settings
from uuid import uuid4
from app.core.logger import logger


class BaseVectorStore(ABC):
    @abstractmethod
    def add_documents(self):
        pass

    @abstractmethod
    def similarity_search(
        self, query: str, top_k: int = 3, score_threshold: float | None = None
    ):
        pass


class PineconeVectorStoreService(BaseVectorStore):
    def __init__(self, embeddings):
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.index = self.pc.Index(settings.PINECONE_INDEX)
        self.embeddings = embeddings

        # self.embeddings = HuggingFaceEmbeddings(
        #     model_name=settings.EMBEDDING_MODEL
        # )

        # self.vector_store = PineconeVectorStore(
        #     index = self.index,
        #     embedding=self.embeddings
        # )# try by removing keys

        self.vector_store = PineconeVectorStore(
            embedding=self.embeddings, index=self.index
        )  # try by removing keys

    def add_documents(self, documents: list[Document]) -> int:
        try:
            ids = [str(uuid4()) for _ in documents]
            # chucks = [
            # Document(page_content=chunk)
            # for chunk in documents
            # ]
            data = self.vector_store.add_documents(documents=documents, ids=ids)

            #             data =  self.index.delete(
            #     delete_all=True
            # )

            return data
        except Exception as error:
            raise error

    def similarity_search(
        self, query: str, top_k: int = 3, score_threshold: float | None = None
    ):
        try:
            logger.info("Runnning pinecone similarity search.")
            results = self.vector_store.similarity_search_with_score(
                query=query, k=top_k
            )

            if score_threshold is not None:

                results = [
                    (document, score)
                    for document, score in results
                    if score >= score_threshold
                ]

            logger.info("Retrieved %d chunks.", len(results))

            if not len(results) > 0:
                return {"message": "data empty"}

            return results
        except Exception as error:
            raise error

        #   if score_threshold is not None:

        #         results = [
        #             (document, score)
        #             for document, score in results
        #             if score >= score_threshold
        #         ]

        #     logger.info(
        #         "Retrieved %d chunks.",
        #         len(results)
        #     )
