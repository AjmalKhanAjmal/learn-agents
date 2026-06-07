# from sentence_transformers import SentenceTransformer

# model = SentenceTransformer(
#     "sentence-transformers/all-MiniLM-L6-v2"
# )


# def embed(texts):
#     return model.encode(texts)

# app/rag/embedder.py

from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)