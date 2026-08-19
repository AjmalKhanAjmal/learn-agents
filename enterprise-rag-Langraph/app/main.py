from fastapi import FastAPI, Request
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse

from app.routes.upload import router as upload_router
from app.routes.chat import router as chat_router
from app.routes.retrieval import router as search_router

app = FastAPI(title="Enterprise RAG API", version="1.0.0")


# @app.exception_handler(ResponseValidationError)
# async def response_validation_exception_handler(
#     request: Request,
#     exc: ResponseValidationError
# ):
#     return JSONResponse(
#         status_code=500,
#         content={
#             "status": "error",
#             "message": "Response validation failed",
#             "errors": exc.errors(),
#         },
#     )


app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(search_router)


@app.get("/health")
def health():
    return {"status": "healthy"}
