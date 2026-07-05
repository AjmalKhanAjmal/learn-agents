from fastapi import APIRouter

router = APIRouter()

@router.post("/upload")
def upload():
    return {
        "status":"sucesss",
        "message":"API got hit"
    }

