from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UploadResponse(BaseModel):
    """
    Response returned after a successful document upload.
    """

    status: str = Field(
        description="Processing status",
        examples=["success"]
    )

    message: str = Field(
        description="Human readable message",
        examples=["Document uploaded successfully"]
    )
    
    path :str
    cleaned_data :str | None = None
    splitted_data : list
    vectore_store :list 
    # file_name: str = Field(
    #     description="Original uploaded filename"
    # )

    # file_size: int = Field(
    #     description="Uploaded file size in bytes",
    #     ge=0
    # )

    # characters: int = Field(
    #     description="Number of extracted characters",
    #     ge=0
    # )

    # chunks_created: int = Field(
    #     description="Total chunks created",
    #     ge=0
    # )

    # pinecone_vectors: int = Field(
    #     description="Vectors stored in Pinecone",
    #     ge=0
    # )

    # bm25_documents: int = Field(
    #     description="Documents indexed in BM25",
    #     ge=0
    # )

    # processing_time_ms: float = Field(
    #     description="Total processing time in milliseconds",
    #     ge=0
    # )

    uploaded_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )