
from typing import Any

from opensearchpy import OpenSearch, helpers


class OpenSearchBM25Store:
    """BM25 document indexing and retrieval using OpenSearch."""

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 9201,
        index_name: str = "enterprise_chunks_v1",
        timeout: int = 30,
    ) -> None:
        self.index_name = index_name

        self.client = OpenSearch(
            hosts=[{"host": host, "port": port}],
            use_ssl=False,
            verify_certs=False,
            timeout=timeout,
            max_retries=3,
            retry_on_timeout=True,
        )

    def create_index(self) -> bool:
        """Create the index with explicit field mappings."""

        if self.client.indices.exists(index=self.index_name):
            return False

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
                    "page_number": {"type": "integer"},
                    "content": {
                        "type": "text",
                        "similarity": "default_bm25",
                    },
                }
            },
        }

        self.client.indices.create(
            index=self.index_name,
            body=body,
        )
        return True

    def index_chunks(
        self,
        chunks: list[dict[str, Any]],
    ) -> dict[str, int]:
        """Bulk-index chunks using stable chunk IDs."""

        actions = []

        for chunk in chunks:
            chunk_id = chunk.get("chunk_id")
            content = chunk.get("content")

            if not chunk_id:
                raise ValueError("Every chunk must have a chunk_id")

            if not isinstance(content, str) or not content.strip():
                raise ValueError(
                    f"Chunk {chunk_id} must have non-empty content"
                )

            actions.append(
                {
                    "_op_type": "index",
                    "_index": self.index_name,
                    "_id": chunk_id,
                    "_source": chunk,
                }
            )

        if not actions:
            return {"indexed": 0, "failed": 0}

        success, errors = helpers.bulk(
            self.client,
            actions,
            raise_on_error=False,
            request_timeout=60,
        )

        return {
            "indexed": success,
            "failed": len(errors),
        }

    def search(
        self,
        query: str,
        k: int = 5,
        tenant_id: str | None = None,
        document_id: str | None = None,
    ) -> list[dict[str, Any]]:
        """Retrieve the top-k chunks using BM25."""

        if not query or not query.strip():
            return []

        if k < 1:
            raise ValueError("k must be at least 1")

        filters = []

        if tenant_id is not None:
            filters.append({"term": {"tenant_id": tenant_id}})

        if document_id is not None:
            filters.append({"term": {"document_id": document_id}})

        query_body = {
            "size": k,
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "content": {
                                    "query": query,
                                }
                            }
                        }
                    ],
                    "filter": filters,
                }
            },
        }

        response = self.client.search(
            index=self.index_name,
            body=query_body,
        )

        return [
            {
                **hit["_source"],
                "score": hit["_score"],
            }
            for hit in response["hits"]["hits"]
        ]
