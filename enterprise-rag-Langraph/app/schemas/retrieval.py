from pydantic import BaseModel, ConfigDict


class RetrievalRequest(BaseModel):
    query: str
    top_k: int
    score_threshold: float
    tenant_id: int | None = None
    document_id: str | None = None
    model_config = ConfigDict(from_attributes=True)


# class RetrievalResponse(BaseModel):
#     query: str
#     data: list
#     # model_config = ConfigDict(from_attributes=True)


class RetrievedChunk(BaseModel):

    chunk_id: str
    content: str
    score: float
    metadata: dict
    # model_config = ConfigDict(from_attributes=True)


class RetrievalResponse(BaseModel):

    query: str
    results: list[RetrievedChunk]
    total_results: int
    # model_config = ConfigDict(from_attributes=True)
