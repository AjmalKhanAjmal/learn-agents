from fastapi import APIRouter, Depends, HTTPException, Body
from app.dependencies import get_hybrid_retrieval_service

router = APIRouter(prefix="/retrieval", tags=["Retrieval"])


@router.post("/hybrid_retrieval")
async def hybrid_retrieval(
    query: str = Body(),
    top_k: int = Body(3),
    service=Depends(get_hybrid_retrieval_service),
):
    try:
        data = await service.hybrid_retrievel(query=query, top_k=top_k)
        return data

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
