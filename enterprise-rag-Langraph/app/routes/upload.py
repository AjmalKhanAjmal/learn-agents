
from fastapi import APIRouter   
# from app.rag.extractor import extract_to_text
from langchain_text_splitters import RecursiveCharacterTextSplitter 
# from app.rag.splitter import split_text 
from fastapi import Depends 
from app.dependencies import get_upload_service 
from app.services.upload_service import UploadService
from app.schemas.upload import UploadResponse


router = APIRouter() 
import os 
from fastapi import APIRouter, UploadFile, File, HTTPException 
router = APIRouter(prefix="/documents", tags=["Documents"]) 
UPLOAD_DIR = "uploads" 

@router.post("/upload") 
async def upload( file: UploadFile, response_model = UploadResponse, service: UploadService = Depends(get_upload_service) ):
    try:
        return service.upload(file)
    except Exception as e :
        raise HTTPException(
            status_code=500, 
            detail=str(e)
        )