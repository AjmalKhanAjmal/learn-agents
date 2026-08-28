from app.core.logger import logger
from app.rerankers.base import BaseReranker


class CrossEncoderReranker(BaseReranker):
    def __init__(self, model: str, batch_size: int = 16, max_length: int = 512):
        self.model = model
        self.batch_size = batch_size
        self.max_length = max_length
        try:
            pass
        except Exception as error:
            logger.error()
            raise error
