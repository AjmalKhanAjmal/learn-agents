from fastapi import APIRouter

router = APIRouter()

@router.get('/chat')
def chat():
    return{
        "status":"sucess",
        "message":"api got hitt"
    }
