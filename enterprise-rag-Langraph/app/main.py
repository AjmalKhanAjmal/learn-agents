from fastapi import FastAPI, Request
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse

from app.routes.upload import router as upload_router
from app.routes.chat import router as chat_router
from app.routes.retrieval import router as search_router
from app.routes.hybrid_retrieval import router as hybrid_search_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Enterprise RAG API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
app.include_router(hybrid_search_router)


@app.get("/health")
def health():
    return {"status": "healthy"}
