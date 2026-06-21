from fastapi import APIRouter
from app.models.schemas import ChatRequest
from app.services.conversation_service import ConversationService
from app.memory.redis_memory import RedisMemory


router = APIRouter()

 
@router.post("/chat")
def chat(request: ChatRequest):

    response = ConversationService.chat(
        request.session_id,
        request.message
    )

    return {
        "response": response
    }


@router.get("/history/{session_id}")
def history(session_id: str):

    return {
        "history": RedisMemory.get_history(session_id)
    }