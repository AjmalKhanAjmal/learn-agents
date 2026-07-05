from fastapi import FastAPI
from app.routes.upload import router as upload_router
from app.routes.chat import router as chat_router

app = FastAPI(
    title="Enterprise RAG API",
    version="1.0.0"
)

app.include_router(upload_router)
app.include_router(chat_router)

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }