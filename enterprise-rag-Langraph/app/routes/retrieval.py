from fastapi import APIRouter, Depends, HTTPException, Body
from app.dependencies import get_retrieval_service
from app.schemas.retrieval import RetrievalRequest, RetrievalResponse, RetrievedChunk
from app.core.logger import logger

router = APIRouter(prefix="/retrieval", tags=["Retrieval"])


# Swagger documentation
# Assigning response_model to the route is especially useful when the service returns a dictionary or
# raw data instead of a RetrievalResponse model.
@router.post("/search", response_model=RetrievalResponse)
def search(
    # query: str = Body(),
    # top_k: int = Body(3),
    # score_threshold: float | None = Body(None),
    request: RetrievalRequest,
    service=Depends(get_retrieval_service),
):
    try:
        retrieved_data = service.retrieve(
            request.query, request.top_k, request.score_threshold
        )
        logger.info("started looping retrived documents")
        results = []

        for document, score in retrieved_data:
            results.append(
                RetrievedChunk(
                    chunk_id=document.id, content=document.page_content, score=score
                )
            )
        return RetrievalResponse(
            query=request.query, results=results, total_results=len(results)
        )
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
    # except Exception as e :
    #         raise HTTPException(
    #             status_code=500,
    #             detail=str(e)
    #         )
