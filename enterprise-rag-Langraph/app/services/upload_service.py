from datetime import datetime
from pydantic import ValidationError
from app.core.exceptions import ApplicationError
from app.core.logger import logger
from app.schemas.upload import UploadResponse
from app.rag.document_builder import DocumentBuilder

# from app.rag.cleaner import TextCleaner


class UploadService:

    def __init__(
        self,
        storage,
        extractor,
        cleaner,
        RecursiveSplitter,
        pineconeVectorStore,
        bm25Store,
    ):
        self.storage = storage
        self.extractor = extractor
        self.cleaner = cleaner
        self.recursiveSplitter = RecursiveSplitter
        self.pineconeVectorStore = pineconeVectorStore
        self.bm25_store = bm25Store

    def upload(self, upload_file):

        try:
            # 1. Save uploaded file
            saved_path = self.storage.save(upload_file)
            # 2. Extract text from PDF
            extracted_text = self.extractor.extract(saved_path)

            cleaned_data = self.cleaner.clean(extracted_text)

            splitted_data = self.recursiveSplitter.split(cleaned_data)

            document_builder = DocumentBuilder()
            documents = document_builder.build(
                splitted_data, saved_path, "document_123"
            )
            vectore_store = self.pineconeVectorStore.add_documents(documents)
            # print("extracted test ")
            bm25_store = self.bm25_store.create_index(splitted_data)

            logger.info("PDF text extracted successfully")
            return UploadResponse(
                status="success",
                message="File uploaded successfully",
                path=str(saved_path),
                uploaded_at=datetime.now(),
                # cleaned_data = cleaned_data,
                splitted_data=splitted_data,
                vectore_store=vectore_store,
                bm25_store=bm25_store,
            )

        except ValidationError as error:

            logger.warning("Response validation failed", exc_info=error)
            raise

        except ApplicationError as error:

            logger.exception("Application error")
            raise

        except Exception as error:

            logger.exception("Unexpected error")
            raise
