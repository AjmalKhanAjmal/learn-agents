from abc import ABC, abstractmethod
from typing import Any
from langchain_core.documents import Document
from opensearchpy import OpenSearch, helpers
from app.core.exceptions import BM25Error
from app.core.logger import logger
from app.schemas.retrieval import RetrievedChunk
from app.core.config import settings
import time
from uuid import uuid4


class BaseKeywordStore(ABC):

    @abstractmethod
    def create_index(self, documents: list[Document]) -> int:
        pass

    @abstractmethod
    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[RetrievedChunk]:
        pass
class BM25Store(BaseKeywordStore):

    def __init__(
        self,
        host: str | None = None,
        port: int | None = None,
        index_name: str | None = None,
    ):
        start_time = time.perf_counter()

        self.host = host or settings.OPENSEARCH_HOST
        self.port = port or settings.OPENSEARCH_PORT
        self.index_name = index_name or settings.OPENSEARCH_INDEX

        logger.info(
            "Initializing OpenSearch BM25 store. host=%s port=%s index=%s",
            self.host,
            self.port,
            self.index_name,
        )

        try:
            self.client = OpenSearch(
                hosts=[{"host": self.host, "port": self.port}],
                http_auth=(
                settings.OPENSEARCH_USERNAME,
                settings.OPENSEARCH_PASSWORD,
                ),
                # use_ssl=False
                use_ssl=True,
                verify_certs=False,
                timeout=30,
                max_retries=3,
                retry_on_timeout=True,
            )

            elapsed_ms = (time.perf_counter() - start_time) * 1000

            logger.info(
                "OpenSearch BM25 store initialized successfully. "
                "index=%s duration_ms=%.2f",
                self.index_name,
                elapsed_ms,
            )

        except Exception:
            logger.exception(
                "Failed to initialize OpenSearch BM25 store. "
                "host=%s port=%s index=%s",
                self.host,
                self.port,
                self.index_name,
            )
            raise

    def _ensure_index(self) -> None:
        try:
            if self.client.indices.exists(index=self.index_name):
                logger.debug(
                    "OpenSearch index already exists. index=%s",
                    self.index_name,
                )
                return

            logger.info(
                "Creating OpenSearch BM25 index. index=%s",
                self.index_name,
            )

            body = {
                "settings": {
                    "index": {
                        "number_of_shards": 1,
                        "number_of_replicas": 0,
                        "similarity": {
                            "default_bm25": {
                                "type": "BM25",
                                "k1": 1.2,
                                "b": 0.75,
                            }
                        },
                    }
                },
                "mappings": {
                    "properties": {
                        "chunk_id": {"type": "keyword"},
                        "document_id": {"type": "keyword"},
                        "tenant_id": {"type": "keyword"},
                        "source": {"type": "keyword"},
                        "chunk_index": {"type": "integer"},
                        "content": {
                            "type": "text",
                            "similarity": "default_bm25",
                        },
                        "metadata": {
                            "type": "object",
                            "properties": {
                                "chunk_id": {"type": "keyword"},
                                "document_id": {"type": "keyword"},
                                "tenant_id": {"type": "keyword"},
                                "source": {"type": "keyword"},
                                "chunk_index": {"type": "integer"},
                            },
                        },
                    }
                },
            }

            self.client.indices.create(
                index=self.index_name,
                body=body,
            )

            logger.info(
                "OpenSearch BM25 index created successfully. index=%s",
                self.index_name,
            )
            
        except Exception as error:
            # if (
            #     "resource_already_exists_exception" in str(error)
            #     and self.client.indices.exists(index=self.index_name)
            # ):
            #     logger.info(
            #         "OpenSearch index already exists. index=%s",
            #         self.index_name,
            #     )
            #     return

            logger.exception("Failed to ensure OpenSearch index.")
            raise

    @staticmethod
    def _document_record(document: Document) -> dict[str, Any]:
        metadata = dict(document.metadata or {})

        chunk_id = metadata.get("chunk_id")

        if not chunk_id:
            raise ValueError(
                "Every document must contain metadata['chunk_id']"
            )

        if not document.page_content.strip():
            raise ValueError(
                f"Chunk {chunk_id} has empty page_content"
            )

        return {
            "chunk_id": str(chunk_id),
            "document_id": (
                str(metadata["document_id"])
                if metadata.get("document_id") is not None
                else ""
            ),
            "tenant_id": (
                str(metadata["tenant_id"])
                if metadata.get("tenant_id") is not None
                else ""
            ),
            "source": str(metadata.get("source", "")),
            "chunk_index": metadata.get("chunk_index"),
            "content": document.page_content,
            "metadata": metadata,
        }

    def create_index(self, documents: list[Document]) -> int:
        operation_id = str(uuid4())
        start_time = time.perf_counter()
        document_count = len(documents)

        logger.info(
            "Starting OpenSearch BM25 indexing. "
            "operation_id=%s document_count=%d index=%s",
            operation_id,
            document_count,
            self.index_name,
        )

        try:
            if not documents:
                logger.warning(
                    "OpenSearch indexing skipped because no documents "
                    "were provided. operation_id=%s index=%s",
                    operation_id,
                    self.index_name,
                )
                return 0

            self._ensure_index()

            actions = []

            for document in documents:
                record = self._document_record(document)

                opensearch_id = (
                    f"{record['tenant_id']}:"
                    f"{record['document_id']}:"
                    f"{record['chunk_id']}"
                )

                actions.append(
                    {
                        "_op_type": "index",
                        "_index": self.index_name,
                        "_id": opensearch_id,
                        "_source": record,
                    }
                )

            logger.debug(
                "Prepared bulk indexing actions. "
                "operation_id=%s action_count=%d",
                operation_id,
                len(actions),
            )

            indexed, errors = helpers.bulk(
                self.client,
                actions,
                raise_on_error=False,
                request_timeout=60,
            )

            elapsed_ms = (time.perf_counter() - start_time) * 1000

            if errors:
                logger.error(
                    "OpenSearch bulk indexing completed with failures. "
                    "operation_id=%s indexed_count=%d failed_count=%d "
                    "duration_ms=%.2f",
                    operation_id,
                    indexed,
                    len(errors),
                    elapsed_ms,
                )

                raise BM25Error(
                    f"OpenSearch failed to index {len(errors)} chunks."
                )

            logger.info(
                "OpenSearch BM25 indexing completed successfully. "
                "operation_id=%s requested_count=%d indexed_count=%d "
                "duration_ms=%.2f",
                operation_id,
                document_count,
                indexed,
                elapsed_ms,
            )

            return indexed

        except BM25Error:
            raise

        except Exception as error:
            elapsed_ms = (time.perf_counter() - start_time) * 1000

            logger.exception(
                "OpenSearch BM25 indexing failed. "
                "operation_id=%s document_count=%d index=%s "
                "duration_ms=%.2f error_type=%s",
                operation_id,
                document_count,
                self.index_name,
                elapsed_ms,
                type(error).__name__,
            )

            raise BM25Error(str(error)) from error

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[RetrievedChunk]:
        operation_id = str(uuid4())
        start_time = time.perf_counter()

        logger.debug(
            "Starting OpenSearch BM25 search. "
            "operation_id=%s top_k=%d index=%s",
            operation_id,
            top_k,
            self.index_name,
        )

        try:
            if not query or not query.strip():
                logger.warning(
                    "BM25 search skipped because the query is empty. "
                    "operation_id=%s",
                    operation_id,
                )
                return []

            if top_k < 1:
                raise ValueError("top_k must be at least 1")

            if not self.client.indices.exists(index=self.index_name):
                logger.warning(
                    "BM25 search skipped because the index does not exist. "
                    "operation_id=%s index=%s",
                    operation_id,
                    self.index_name,
                )
                return []

            response = self.client.search(
                index=self.index_name,
                body={
                    "size": top_k,
                    "query": {
                        "match": {
                            "content": {
                                "query": query,
                            }
                        }
                    },
                },
            )

            results = []

            for hit in response["hits"]["hits"]:
                record = hit["_source"]

                results.append(
                    RetrievedChunk(
                        chunk_id=record["chunk_id"],
                        content=record["content"],
                        score=float(hit["_score"]),
                        metadata=record["metadata"],
                    )
                )

            elapsed_ms = (time.perf_counter() - start_time) * 1000

            logger.info(
                "OpenSearch BM25 search completed. "
                "operation_id=%s result_count=%d top_k=%d "
                "duration_ms=%.2f",
                operation_id,
                len(results),
                top_k,
                elapsed_ms,
            )

            return results

        except Exception as error:
            elapsed_ms = (time.perf_counter() - start_time) * 1000

            logger.exception(
                "OpenSearch BM25 search failed. "
                "operation_id=%s index=%s duration_ms=%.2f "
                "error_type=%s",
                operation_id,
                self.index_name,
                elapsed_ms,
                type(error).__name__,
            )

            raise BM25Error(str(error)) from error
