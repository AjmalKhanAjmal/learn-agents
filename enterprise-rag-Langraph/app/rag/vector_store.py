
import time
from abc import ABC, abstractmethod
from uuid import uuid4
 
from langchain_core.documents import Document
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

from app.core.config import settings
from app.core.logger import logger


class BaseVectorStore(ABC):

    @abstractmethod
    def add_documents(self, documents: list[Document]) -> list[str]:
        pass

    @abstractmethod
    def similarity_search(
        self,
        query: str,
        top_k: int = 3,
        score_threshold: float | None = None,
    ):
        pass


class PineconeVectorStoreService(BaseVectorStore):

    def __init__(self, embeddings):
        start_time = time.perf_counter()

        logger.info(
            "Initializing Pinecone vector store service."
        )

        try:
            self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
            self.index = self.pc.Index(settings.PINECONE_INDEX)
            self.embeddings = embeddings

            self.vector_store = PineconeVectorStore(
                embedding=self.embeddings,
                index=self.index,
            )

            elapsed_ms = (time.perf_counter() - start_time) * 1000

            logger.info(
                "Pinecone vector store service initialized successfully. "
                "index=%s duration_ms=%.2f",
                settings.PINECONE_INDEX,
                elapsed_ms,
            )

        except Exception:
            logger.exception(
                "Failed to initialize Pinecone vector store service. "
                "index=%s",
                settings.PINECONE_INDEX,
            )
            raise

    def add_documents(self, documents: list[Document]) -> list[str]:
        document_count = len(documents)

        if not documents:
            logger.warning(
                "Document upload skipped because the input is empty."
            )
            return []

        start_time = time.perf_counter()
        operation_id = str(uuid4())

        logger.info(
            "Starting document upload to Pinecone. "
            "operation_id=%s document_count=%d index=%s",
            operation_id,
            document_count,
            settings.PINECONE_INDEX,
        )

        try:
            ids = [str(uuid4()) for _ in documents]

            result = self.vector_store.add_documents(
                documents=documents,
                ids=ids,
            )

            elapsed_ms = (time.perf_counter() - start_time) * 1000

            logger.info(
                "Document upload completed successfully. "
                "operation_id=%s requested_count=%d duration_ms=%.2f",
                operation_id,
                document_count,
                elapsed_ms,
            )

            return result

        except Exception:
            elapsed_ms = (time.perf_counter() - start_time) * 1000

            logger.exception(
                "Document upload failed. "
                "operation_id=%s document_count=%d index=%s "
                "duration_ms=%.2f",
                operation_id,
                document_count,
                settings.PINECONE_INDEX,
                elapsed_ms,
            )
            raise

    def similarity_search(
        self,
        query: str,
        metadata_filter = {},
        top_k: int = 3,
        score_threshold: float | None = None,
    ):
        try:
            logger.info(
                "Running Pinecone similarity search. query=%s, k=%s, filter=%s",
                query,
                top_k,
                metadata_filter,
            )
            # logger.info("Runnning pinecone similarity search.")

            results = self.vector_store.similarity_search_with_score(
                query=query, k=top_k, filter=metadata_filter
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
