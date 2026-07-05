from app.rag.vector_store import search
from app.rag.bm25_store import search_bm25


# def hybrid_search(query,k=3):

#     semantic_results = search(
#         query=query,
#         k=k
#     )

#     keyword_results = search_bm25(
#         query=query,
#         k=k
#     )
#     print("keyword_results",keyword_results)

#     merged=[]

#     for doc in semantic_results:
#         merged.append(doc.page_content)

#     for doc,score in keyword_results:
#         merged.append(doc)

#     merged = list(
#         dict.fromkeys(merged)
#     )

#     return merged[:k]


def hybrid_search(query, k=20):

    # Semantic search from Pinecone
    semantic_results = search(
        query=query,
        k=k
    )

    # Keyword search from BM25
    keyword_results = search_bm25(
        query=query,
        k=k
    )

    merged = []

    # Add semantic results
    for doc in semantic_results:
        merged.append(doc.page_content)

    # Add only valid BM25 results
    for doc, score in keyword_results:

        if score > 0:
            merged.append(doc)

    # Remove duplicate chunks
    merged = list(
        dict.fromkeys(merged)
    )

    return merged[:k]