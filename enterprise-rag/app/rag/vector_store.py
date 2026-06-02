import faiss
import numpy as np

index = None
documents = []


def create_index(vectors, chunks):
    global index
    global documents

    dimension = len(vectors[0])

    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(vectors))

    documents = chunks


def search(query_vector, k=3):
    global index

    distances, indices = index.search(
        np.array([query_vector]),
        k
    )

    results = []

    for idx in indices[0]:
        results.append(documents[idx])

    return results