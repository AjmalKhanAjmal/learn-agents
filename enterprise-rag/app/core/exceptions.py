"""
Domain-specific exception hierarchy.
All custom exceptions should inherit from RAGException.
"""
from http import HTTPStatus


class RAGException(Exception):
    """Base exception for all RAG application errors."""

    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR
    error_code: str = "INTERNAL_ERROR"

    def __init__(self, message: str, details: dict | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}


# ── Document Processing ────────────────────────────────────────────────────────

class DocumentProcessingError(RAGException):
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY
    error_code = "DOCUMENT_PROCESSING_ERROR"


class UnsupportedFileTypeError(RAGException):
    status_code = HTTPStatus.UNSUPPORTED_MEDIA_TYPE
    error_code = "UNSUPPORTED_FILE_TYPE"


class FileTooLargeError(RAGException):
    status_code = HTTPStatus.REQUEST_ENTITY_TOO_LARGE
    error_code = "FILE_TOO_LARGE"


class EmptyDocumentError(RAGException):
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY
    error_code = "EMPTY_DOCUMENT"


# ── Embedding ──────────────────────────────────────────────────────────────────

class EmbeddingError(RAGException):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    error_code = "EMBEDDING_ERROR"


# ── Vector Store ───────────────────────────────────────────────────────────────

class VectorStoreError(RAGException):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    error_code = "VECTOR_STORE_ERROR"


class IndexNotFoundError(RAGException):
    status_code = HTTPStatus.NOT_FOUND
    error_code = "INDEX_NOT_FOUND"


# ── Retrieval ──────────────────────────────────────────────────────────────────

class RetrievalError(RAGException):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    error_code = "RETRIEVAL_ERROR"


class NoResultsFoundError(RAGException):
    status_code = HTTPStatus.NOT_FOUND
    error_code = "NO_RESULTS_FOUND"


# ── Generation ─────────────────────────────────────────────────────────────────

class GenerationError(RAGException):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    error_code = "GENERATION_ERROR"


class LLMRateLimitError(RAGException):
    status_code = HTTPStatus.TOO_MANY_REQUESTS
    error_code = "LLM_RATE_LIMIT"


# ── Evaluation ─────────────────────────────────────────────────────────────────

class EvaluationError(RAGException):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    error_code = "EVALUATION_ERROR"