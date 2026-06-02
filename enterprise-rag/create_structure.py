from pathlib import Path

files = [
    "app/main.py",
    "app/api/routes/chat.py",
    "app/api/routes/upload.py",
    "app/core/config.py",
    "app/memory/redis_memory.py",
    "app/prompts/chat_prompt.py",
    "app/rag/extractor.py",
    "app/rag/splitter.py",
    "app/rag/embedder.py",
    "app/rag/vector_store.py",
    "app/rag/retriever.py",
    "app/chains/chat_chain.py",
    "app/chains/rag_chain.py",
    "app/graphs/conversation_graph.py",
]

for file in files:
    Path(file).parent.mkdir(parents=True, exist_ok=True)
    Path(file).touch(exist_ok=True)

print("Enterprise RAG structure created!")