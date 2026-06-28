from app.rag.vector_store import search
from app.rag.bm25_store import search_bm25


def hybrid_search(query,k=3):

    semantic_results = search(
        query=query,
        k=k
    )

    keyword_results = search_bm25(
        query=query,
        k=k
    )

    merged=[]

    for doc in semantic_results:
        merged.append(doc.page_content)

    for doc,score in keyword_results:
        merged.append(doc)

    merged = list(
        dict.fromkeys(merged)
    )

    return merged[:k]