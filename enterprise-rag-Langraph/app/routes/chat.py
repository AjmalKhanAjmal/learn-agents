from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.graph_service import run_graph

router = APIRouter(prefix="/chat", tags=["Chat"])


class GraphChatRequest(BaseModel):
    query: str


@router.post("/graph")
async def graph_chat(request: GraphChatRequest):
    try:
        result = await run_graph(request.query)
        return result

    except Exception as exc:
        # Log the exception in production.
        raise HTTPException(
            status_code=500,
            detail="Failed to execute RAG graph",
        ) from exc