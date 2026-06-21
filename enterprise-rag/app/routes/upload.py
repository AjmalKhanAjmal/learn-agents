# from fastapi import APIRouter, UploadFile, File
# import os

# from app.rag.extractor import extract_pdf_text
# from app.rag.splitter import split_text
# from app.rag.embedder import embed
# from app.rag.vector_store import create_index

# router = APIRouter()


# @router.post("/upload")
# async def upload(file: UploadFile = File(...)):

#     os.makedirs("uploads", exist_ok=True)

#     path = f"uploads/{file.filename}"

#     with open(path, "wb") as f:
#         f.write(await file.read())

#     text = extract_pdf_text(path)

#     chunks = split_text(text)

#     vectors = embed(chunks)

#     create_index(vectors, chunks)

#     return {
#         "message": "Document indexed",
#         "chunks": len(chunks)
#     }

from fastapi import APIRouter, UploadFile, File
import os

from app.rag.extractor import extract_pdf_text
from app.rag.splitter import split_text 
from app.rag.vector_store import create_index

router = APIRouter()


# @router.post("/upload")
# async def upload(file: UploadFile = File(...)):

#     os.makedirs("uploads", exist_ok=True)

#     path = f"uploads/{file.filename}"

#     with open(path, "wb") as f:
#         f.write(await file.read())                     

#     text = extract_pdf_text(path)

#     chunks = split_text(text)

#     create_index(chunks)

#     return {
#         "message": "Document indexed successfully",
#         "chunks":"len(chunks)"
#     }


 
@router.post("/upload")
 
async def upload(file:UploadFile):
    os.makedirs("uploads", exist_ok=True)

    path = f"uploads/{file.filename}"

    with open(path, "wb") as f:
        print("HHFK",f)
        f.write(await file.read())   
    
    text = extract_pdf_text(path)
    chunks = split_text(text)
    dataaa = create_index(chunks)

    return {
        "status":"success",
        "message":"got it",
        "data":text,
        "file_name":file.filename,
        "chunks":chunks,
        "index":dataaa
    }

