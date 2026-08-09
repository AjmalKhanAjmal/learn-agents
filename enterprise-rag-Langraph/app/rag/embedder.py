from abc import ABC, abstractmethod
from app.core.config import settings
from sentence_transformers import SentenceTransformer

from app.core.logger import logger

class BaseEmbedder(ABC):
    @abstractmethod
    def embed_documents(self):
        pass
    
class SentenceTransformerEmbedder(BaseEmbedder):
    def __init__(self):
        logger.info("loading embedding model")
        self.model = SentenceTransformer(
            settings.EMBEDDING_MODEL
        )
        
    def embed_documents(self,chunks):
        try:
            vectors = self.model.encode(chunks)
            logger.info("Embedding generated")
            return vectors
        
        
        except Exception as error:
            logger.exception(
                "Embedding generation failed."
            )
            
            raise error