from pydantic import BaseModel, ConfigDict


class RetrievalResponse(BaseModel):
    query: str
    data: list[str]
    model_config = ConfigDict(from_attributes=True)
