# from app.rag.embedder import embed
# from app.rag.vector_store import search


# def retrieve(question):
#     vector = embed([question])[0]

#     return search(vector)         

from app.rag.vector_store import search


def retrieve(question):

    docs = search(
        query=question,
        k=3
    )

    return docs