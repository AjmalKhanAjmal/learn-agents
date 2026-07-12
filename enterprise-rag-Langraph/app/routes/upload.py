from fastapi import APIRouter
from app.rag.extractor import extract_to_text
from langchain_text_splitters import RecursiveCharacterTextSplitter  



router = APIRouter()

import os

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


UPLOAD_DIR = "uploads"


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):
    # Validate file type
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )
        
    
    
    # Create uploads folder if missing
    # os.makedirs(
    #     UPLOAD_DIR,
    #     exist_ok=True
    # )

    # Build final file path
    # file_path = os.path.join(
    #     UPLOAD_DIR,
    #     file.filename
    # )

    try:
        # Read uploaded file
        file_content = await file.read()
        
        text_content = extract_to_text(file.file)
        # Save file locally
        # with open(
        #     file_path,
        #     "wb"
        # ) as output_file:
        #     output_file.write(
        #         file_content
        #     )

        return {
            "status": "success",
            "message": "PDF uploaded successfully",
            "file_name": file.filename,
            "file_path": text_content
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=(
                "File upload failed: "
                f"{str(error)}"
            )
        )

    finally:
        await file.close()