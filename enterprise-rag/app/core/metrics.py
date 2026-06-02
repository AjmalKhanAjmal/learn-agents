"""
Prometheus metrics — collected across services and exposed at /metrics.
"""
from prometheus_client import Counter, Gauge, Histogram

# ── Document ingestion ─────────────────────────────────────────────────────────
DOCUMENTS_UPLOADED = Counter(
    "rag_documents_uploaded_total",
    "Total number of documents uploaded",
    ["file_type", "status"],
)
DOCUMENTS_INDEXED = Counter(
    "rag_documents_indexed_total",
    "Total number of documents successfully indexed",
    ["status"],
)
CHUNKS_CREATED = Counter(
    "rag_chunks_created_total",
    "Total text chunks created from documents",
)
INDEXING_DURATION = Histogram(
    "rag_indexing_duration_seconds",
    "Time to index a document end-to-end",
    buckets=[1, 5, 10, 30, 60, 120, 300],
)

# ── Retrieval ──────────────────────────────────────────────────────────────────
RETRIEVAL_DURATION = Histogram(
    "rag_retrieval_duration_seconds",
    "Time to retrieve and rerank chunks",
    buckets=[0.05, 0.1, 0.25, 0.5, 1, 2, 5],
)
QUERIES_TOTAL = Counter(
    "rag_queries_total",
    "Total number of questions asked",
    ["status"],
)

# ── Generation ─────────────────────────────────────────────────────────────────
GENERATION_DURATION = Histogram(
    "rag_generation_duration_seconds",
    "Time for LLM to generate an answer",
    buckets=[0.5, 1, 2, 5, 10, 20, 30],
)
LLM_TOKENS_USED = Counter(
    "rag_llm_tokens_total",
    "Total LLM tokens consumed",
    ["direction"],   # input | output
)

# ── Evaluation ─────────────────────────────────────────────────────────────────
EVAL_SCORES = Histogram(
    "rag_eval_scores",
    "Distribution of RAG evaluation metric scores",
    ["metric"],
    buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
)

# ── System ─────────────────────────────────────────────────────────────────────
ACTIVE_CONNECTIONS = Gauge(
    "rag_active_connections",
    "Number of currently active HTTP connections",
)