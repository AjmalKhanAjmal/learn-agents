from fastapi import APIRouter, Depends, HTTPException, Body
from app.dependencies import get_retrieval_service

router = APIRouter(prefix="/retrieval", tags=["Retrieval"])


@router.post("/search")
def search(
    query: str = Body(),
    top_k: int = Body(3),
    score_threshold: float | None = Body(None),
    service=Depends(get_retrieval_service),
):
    try:
        results = service.retrieve(query, top_k, score_threshold)
        return results
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
    # except Exception as e :
    #         raise HTTPException(
    #             status_code=500,
    #             detail=str(e)
    #         )
