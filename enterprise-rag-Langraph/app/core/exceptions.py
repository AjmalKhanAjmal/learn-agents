"""
Application specific exceptions.

Every business layer should raise one of these
instead of generic Exception.
"""


class ApplicationError(Exception):
    """
    Base exception for the application.
    """

    default_message = "Application error"

    def __init__(self, message: str | None = None):

        self.message = message or self.default_message

        super().__init__(self.message)


class ValidationError(ApplicationError):

    default_message = "Validation failed"


class FileStorageError(ApplicationError):

    default_message = "Unable to store uploaded file"


class PDFExtractionError(ApplicationError):

    default_message = "Unable to extract PDF text"


# class TextCleaningError(ApplicationError):

#     default_message = "Unable to clean extracted text"


# class ChunkingError(ApplicationError):

#     default_message = "Unable to split document"


# class EmbeddingError(ApplicationError):

#     default_message = "Embedding generation failed"


# class PineconeError(ApplicationError):

#     default_message = "Unable to store vectors in Pinecone"


# class BM25Error(ApplicationError):

#     default_message = "Unable to build BM25 index"


class RetrievalServiceError(ApplicationError):
    default_message = "Unable to retrive data"
