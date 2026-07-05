from sentence_transformers import CrossEncoder


# Load model only once when server starts
_reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank_documents(query, documents, top_k=5):

    if not documents:
        return []

    # Create query-document pairs
    pairs = [
        [query, document]
        for document in documents
    ]

    # Calculate relevance scores
    scores = _reranker.predict(pairs)

    # Combine document with score
    scored_documents = list(
        zip(documents, scores)
    )

    # Sort highest score first
    scored_documents.sort(
        key=lambda x: float(x[1]),
        reverse=True
    )

    # Return best documents
    return scored_documents[:top_k]