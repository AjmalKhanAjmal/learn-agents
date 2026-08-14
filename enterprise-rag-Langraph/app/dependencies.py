from app.rag.vector_store import PineconeVectorStoreService
from app.services.file_storage_service import FileStorageService
from app.services.upload_service import UploadService
from app.rag.extractor import PDFExtractor
from app.rag.cleaner import TextCleaner
from app.rag.splitter import RecursiveTextSplitter


# from app.rag.splitter import TextSplitter
# from app.rag.embedder import EmbeddingService
# from app.rag.vector_store import VectorStore
def get_upload_service():
    storage = FileStorageService()
    extractor = PDFExtractor()
    cleaner = TextCleaner()
    RecursiveSplitter = RecursiveTextSplitter()
    pineconeVectorStore = PineconeVectorStoreService()

    return UploadService(
        storage=storage,
        extractor=extractor,
        cleaner=cleaner,
        RecursiveSplitter=RecursiveSplitter,
        pineconeVectorStore=pineconeVectorStore
    )



