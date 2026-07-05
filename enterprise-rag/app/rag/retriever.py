from app.rag.vector_store import search
from app.rag.hybrid_retriever import hybrid_search
from app.rag.reranker import rerank_documents


# def retrieve(question):

#     # docs = search(
#     #     query=question,
#     #     k=3
#     # )
#     docs = hybrid_search(
#         query=question,
#         k=3
#     )

#     return docs





def retrieve(query):

    # Step 1:
    # Get top 20 candidate chunks
    candidate_chunks = hybrid_search(
        query=query,
        k=20
    )

    print(
        "Candidate Chunks:",
        len(candidate_chunks)
    )

    # Step 2:
    # Re-rank and select best 5
    reranked_results = rerank_documents(
        query=query,
        documents=candidate_chunks,
        top_k=5
    )

    print("\n===== RERANKED RESULTS =====")

    for i, (doc, score) in enumerate(
        reranked_results
    ):
        print(
            f"\nRank {i + 1}"
        )

        print(
            "Score:",
            float(score)
        )

        print(
            "Document:",
            doc[:300]
        )

    # Return only text
    return [
        doc
        for doc, score in reranked_results
    ]