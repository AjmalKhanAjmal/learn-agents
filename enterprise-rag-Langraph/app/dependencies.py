from app.llm.groq_provider import GroqProvider
from app.rag.bm25_store import BM25Store
from app.rag.result_fusion import ResultFusionService
from app.rag.vector_store import PineconeVectorStoreService
from app.rerankers.cross_encoder import CrossEncoderReranker
from app.services.file_storage_service import FileStorageService
from app.services.generation_service import GenerationService
from app.services.reranking_service import RerankerService
from app.services.upload_service import UploadService
from app.rag.extractor import PDFExtractor
from app.rag.cleaner import TextCleaner
from app.rag.splitter import RecursiveTextSplitter
from app.rag.embedder import SentenceTransformerEmbedder
from fastapi import HTTPException
from app.services.retrieval_service import RetrievalService
from app.services.hybrid_retrieval_service import HybridRetrievalService


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
        pineconeVectorStore = PineconeVectorStoreService(embeddings=embeddings)
        bm25Store = BM25Store()
        return UploadService(
            storage=storage,
            extractor=extractor,
            cleaner=cleaner,
            RecursiveSplitter=RecursiveSplitter,
            pineconeVectorStore=pineconeVectorStore,
            bm25Store=bm25Store,
        )
    except Exception as error:
        raise HTTPException(
            status_code=500,  # why this showing error for api response
            # detail="Failed to initialize upload service."
            detail=str(error),
        )
        # raise error // why this one not showing error for api response


def get_retrieval_service():
    try:
        embedding_service = SentenceTransformerEmbedder()
        embeddings = embedding_service.get_embeddings()
        pincone_vectore = PineconeVectorStoreService(embeddings=embeddings)
        return RetrievalService(vector_store=pincone_vectore)
        # get_embeddings
    except Exception as error:
        raise HTTPException(
            status_code=500,  # why this showing error for api response
            # detail="Failed to initialize upload service."
            detail=str(error),
        )


def get_hybrid_retrieval_service():
    try:
        embedding_service = SentenceTransformerEmbedder()
        embeddings = embedding_service.get_embeddings()

        pineconeVectorStore = PineconeVectorStoreService(embeddings=embeddings)
        bm25Store = BM25Store()
        fusion_service = ResultFusionService(rrf_constant=60)
        reranker_obj = CrossEncoderReranker(
            model_name="cross-encoder/ms-marco-MiniLM-L-6-v2",
            batch_size=16,
            max_length=512,
        )
        rerank_service_obj = RerankerService(reranker=reranker_obj)

        # reranking = reranker_obj = CrossEncoderReranker(
        #         model_name="cross-encoder/ms-marco-MiniLM-L-6-v2", batch_size=16, max_length=512
        #     )

        # gro_api_key = ""
        # model_name = "openai/gpt-oss-20b"

        # provider = GroqProvider(api_key=gro_api_key, model=model_name)
        provider = GroqProvider()

        llm_service = GenerationService(provider)
        return HybridRetrievalService(
            vector_store=pineconeVectorStore,
            keyword_store=bm25Store,
            fusion_service=fusion_service,
            rerank_service_obj=rerank_service_obj,
            llm_service=llm_service,
        )
    except Exception as error:
        raise HTTPException(
            status_code=500,  # why this showing error for api response
            # detail="Failed to initialize upload service."
            detail=str(error),
        )
