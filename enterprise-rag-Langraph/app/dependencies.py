from app.rag.bm25_store import BM25Store
from app.rag.vector_store import PineconeVectorStoreService
from app.services.file_storage_service import FileStorageService
from app.services.upload_service import UploadService
from app.rag.extractor import PDFExtractor
from app.rag.cleaner import TextCleaner
from app.rag.splitter import RecursiveTextSplitter
from app.rag.embedder import SentenceTransformerEmbedder
from fastapi import HTTPException 
# from app.rag.splitter import TextSplitter
# from app.rag.embedder import EmbeddingService
# from app.rag.vector_store import VectorStore
def get_upload_service():
    try:
            storage = FileStorageService()
            extractor = PDFExtractor()
            cleaner = TextCleaner()
            RecursiveSplitter = RecursiveTextSplitter()
            embedding_service = SentenceTransformerEmbedder()
            embeddings = embedding_service.get_embeddings()
            pineconeVectorStore = PineconeVectorStoreService(embeddings = embeddings)
            bm25Store = BM25Store()
            return UploadService(
                storage=storage,
                extractor=extractor,
                cleaner=cleaner,
                RecursiveSplitter=RecursiveSplitter,
                pineconeVectorStore=pineconeVectorStore,
                bm25Store = bm25Store        
            )
    except Exception as error:
        raise HTTPException( 
            status_code=500, # why this showing error for api response
            # detail="Failed to initialize upload service."
            detail=str(error)
        )
        # raise error // why this one not showing error for api response



