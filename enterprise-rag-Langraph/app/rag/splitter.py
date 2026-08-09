from abc import abstractmethod
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.logger import logger
from app.core.config import settings

class BaseTextSplitter():
    @abstractmethod
    def split(self,text:str)-> list[str]:
        pass
    
class RecursiveTextSplitter(BaseTextSplitter):
    def __init__(self,chunk_size = settings.CHUNK_SIZE,chunk_overlap = settings.CHUNK_OVERLAP):
        self.splitterrrr = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    
    def split(self,text:str)->list[str]:
        try:   
           documents = self.splitterrrr.create_documents(
                [text]
            )
           chunks = [
                document.page_content
                for document in documents
            ]
           
           logger.info(
                "Generated %d chunks.",
                len(chunks)
            )
           
           return chunks
        except Exception as err:
            return err

