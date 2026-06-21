# import faiss
# import numpy as np

# index = None
# documents = []


# def create_index(vectors, chunks):
#     global index
#     global documents

#     dimension = len(vectors[0])

#     index = faiss.IndexFlatL2(dimension)

#     index.add(np.array(vectors))

#     documents = chunks


# def search(query_vector, k=3):
#     global index

#     distances, indices = index.search(
#         np.array([query_vector]),
#         k
#     ) 
#     results = []

#     for idx in indices[0]:
#         results.append(documents[idx])

#     return results





# app/rag/vector_store.py

from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_core.documents import Document

from app.rag.embedder import embeddings
from app.core.config import (
    PINECONE_API_KEY,
    PINECONE_SYMANTIC_INDEX
    # PINECONE_INDEX
)

pc = Pinecone(
    api_key=PINECONE_API_KEY
)

# index = pc.Index(
#     PINECONE_INDEX
# )

# vector_store = PineconeVectorStore(
#     index=index,
#     embedding=embeddings
# )


def create_index(chunks):
    index = pc.Index(
    PINECONE_SYMANTIC_INDEX
    # PINECONE_INDEX
    )

    vector_store = PineconeVectorStore(
        index=index,
        embedding=embeddings()
    )
    docs = [
        Document(page_content=chunk)
        for chunk in chunks
    ]

    vector_store.add_documents(docs)

    return len(docs)


def search(query, k=3):

    index = pc.Index(
    # PINECONE_INDEX
    PINECONE_SYMANTIC_INDEX
    )

    vector_store = PineconeVectorStore(
        index=index,
        embedding=embeddings()
    )
    
    return vector_store.similarity_search(
        query=query,
        k=k
    )


