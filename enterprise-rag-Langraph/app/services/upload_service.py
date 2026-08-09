from datetime import datetime
from pydantic import ValidationError
from app.core.exceptions import ApplicationError
from app.core.logger import logger
from app.schemas.upload import UploadResponse

# from app.rag.cleaner import TextCleaner


class UploadService:

    def __init__(self, storage,extractor,cleaner,RecursiveSplitter):
        self.storage = storage
        self.extractor = extractor
        self.cleaner = cleaner
        self.recursiveSplitter = RecursiveSplitter

    def upload(self, upload_file):

        try:
            # 1. Save uploaded file
            saved_path = self.storage.save(upload_file)
             # 2. Extract text from PDF
             
            extracted_text = self.extractor.extract(saved_path)
            
            cleaned_data = self.cleaner.clean(extracted_text)
            
            splitted_data = self.recursiveSplitter.split(cleaned_data)
            
            # print("extracted test ")
            
            logger.info(
                "PDF text extracted successfully"
            )
            return UploadResponse(
                status="success",
                message="File uploaded successfully",
                path=str(saved_path),
                uploaded_at=datetime.now(),
                # cleaned_data = cleaned_data,
                splitted_data = splitted_data
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