from typing import TypedDict, Any


class AgentState(TypedDict, total=False):

    # -------------------------
    # User request
    # -------------------------

    query: str

    conversation_id: str

    # -------------------------
    # Query analysis
    # -------------------------

    intent: str

    requires_retrieval: bool

    requires_multi_hop: bool

    rewritten_query: str

    sub_queries: list[str]

    # -------------------------
    # Retrieval
    # -------------------------

    retrieval_attempt: int

    retrieval_strategy: str

    semantic_results: list[dict[str, Any]]

    keyword_results: list[dict[str, Any]]

    fused_results: list[dict[str, Any]]

    # -------------------------
    # Ranking
    # -------------------------

    reranked_results: list[dict[str, Any]]

    # -------------------------
    # Compression
    # -------------------------

    compressed_results: list[dict[str, Any]]

    # -------------------------
    # Evidence
    # -------------------------

    evidence_sufficient: bool

    evidence_score: float

    evidence_reason: str

    # -------------------------
    # Generation
    # -------------------------

    answer: str

    # -------------------------
    # Citations
    # -------------------------

    citations: list[dict[str, Any]]

    # -------------------------
    # Validation
    # -------------------------

    grounded: bool

    grounding_score: float

    validation_reason: str

    # -------------------------
    # Control
    # -------------------------

    next_action: str

    error: str | None
