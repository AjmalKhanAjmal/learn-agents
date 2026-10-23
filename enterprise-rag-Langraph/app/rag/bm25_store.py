from abc import ABC, abstractmethod
from typing import Any

from langchain_core.documents import Document
from opensearchpy import OpenSearch, helpers

from app.core.exceptions import BM25Error
from app.core.logger import logger
from app.schemas.retrieval import RetrievedChunk
from app.core.config import settings

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
        self.host = host or settings.OPENSEARCH_HOST
        self.port = port or settings.OPENSEARCH_PORT
        self.index_name = index_name or settings.OPENSEARCH_INDEX

        self.client = OpenSearch(
            hosts=[{"host": host, "port": port}],
            use_ssl=False,
            verify_certs=False,
            timeout=30,
            max_retries=3,
            retry_on_timeout=True,
        )

    def _ensure_index(self) -> None:
        if self.client.indices.exists(index=self.index_name):
            return

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
        try:
            logger.info("Indexing chunks in OpenSearch BM25.")

            if not documents:
                return 0

            self._ensure_index()

            actions = []

            for document in documents:
                record = self._document_record(document)

                # Composite ID prevents collisions between tenants/documents.
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

            indexed, errors = helpers.bulk(
                self.client,
                actions,
                raise_on_error=False,
                request_timeout=60,
            )

            if errors:
                logger.error(
                    "OpenSearch bulk indexing had %d failed actions.",
                    len(errors),
                )
                raise BM25Error(
                    f"OpenSearch failed to index {len(errors)} chunks."
                )

            logger.info("OpenSearch indexed %d chunks.", indexed)
            return indexed

        except BM25Error:
            raise
        except Exception as error:
            logger.exception("OpenSearch BM25 indexing failed.")
            raise BM25Error(str(error)) from error

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[RetrievedChunk]:
        try:
            if not query or not query.strip():
                return []

            if top_k < 1:
                raise ValueError("top_k must be at least 1")

            if not self.client.indices.exists(index=self.index_name):
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

            return results

        except Exception as error:
            logger.exception("OpenSearch BM25 search failed.")
            raise BM25Error(str(error)) from error
