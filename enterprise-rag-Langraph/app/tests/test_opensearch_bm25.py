    
from app.services.retrieval.opensearch_bm25 import OpenSearchBM25Store


def test_opensearch_bm25():
    store = OpenSearchBM25Store(
        index_name="enterprise_chunks_v1"
    )

    created = store.create_index()
    print("Index created:", created)    

    chunks = [
        {
            "chunk_id": "bm25-demo-001",
            "document_id": "demo-document-001",
            "tenant_id": "demo-tenant",
            "source": "bm25_demo.txt",
            "page_number": 1,
            "content": (
                "BM25 is a keyword search algorithm "
                "for information retrieval."
            ),
        },
        {
            "chunk_id": "bm25-demo-002",
            "document_id": "demo-document-002",
            "tenant_id": "demo-tenant",
            "source": "hybrid_demo.txt",
            "page_number": 1,
            "content": (
                "Hybrid retrieval combines keyword search "
                "with semantic vector search."
            ),
        },
        {
            "chunk_id": "bm25-demo-003",
            "document_id": "demo-document-003",
            "tenant_id": "other-tenant",
            "source": "vector_demo.txt",
            "page_number": 1,
            "content": (
                "Vector embeddings represent semantic meaning "
                "for similarity search."
            ),
        },
    ]

    result = store.index_chunks(chunks)
    print("Indexing result:", result)

    store.client.indices.refresh(index=store.index_name)

    results = store.search(
        query="BM25 keyword retrieval",
        k=3,
        tenant_id="demo-tenant",
    )

    for rank, item in enumerate(results, start=1):
        print(
            f"Rank {rank} | "
            f"ID: {item['chunk_id']} | "
            f"Score: {item['score']:.4f} | "
            f"Content: {item['content']}"
        )

    assert result["failed"] == 0
    assert result["indexed"] == 3
    assert results
    assert all(
        item["tenant_id"] == "demo-tenant"
        for item in results
    )
    assert results[0]["chunk_id"] == "bm25-demo-001"


if __name__ == "__main__":
    test_opensearch_bm25()
