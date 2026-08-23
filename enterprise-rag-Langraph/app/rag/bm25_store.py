from abc import ABC, abstractmethod

from rank_bm25 import BM25Okapi
from langchain_core.documents import Document
from app.core.exceptions import BM25Error
from app.core.logger import logger
from app.schemas.retrieval import RetrievedChunk


class BaseKeywordStore(ABC):

    @abstractmethod
    def create_index(
        self,
        documents: list[Document]
    ) -> int:
        pass

    @abstractmethod
    def search(
        self,
        query: str,
        top_k: int = 5
    ) -> list[Document]:
        pass


class BM25Store(BaseKeywordStore):

    def __init__(self):

        self._index = None

        self._documents: list[Document] = []

    def create_index(
        self,
        documents: list[Document]
    ) -> int:
        global _documents_global
        global _bm25
        _documents_global = self._documents
        try:

            logger.info(
                "Creating BM25 index."
            )

            tokenized = [
                document.page_content.lower().split()
                for document in documents
            ]
            
            
# chunk - 1 ['novatech', 'enterprise', 'knowledge', ]
# chunk - 2
# ['for', 'example,', 'backend', 'engineers',]
# chunk - 3
# ['responsibility']  all in one array

            self._index = BM25Okapi(
                tokenized
            )
            _bm25 = self._index

            # self._documents = documents

            logger.info(
                "BM25 indexed %d chunks.",
                len(documents)
            )

            return len(documents)

        except Exception as error:

            logger.exception(
                "BM25 indexing failed."
            )

            raise BM25Error(
                str(error)
            ) from error

    def search(
        self,
        query: str,
        top_k: int = 5
    ) -> list[RetrievedChunk]:

        if self._index is None:

            raise BM25Error(
                "BM25 index is empty."
            )

        try:

            logger.info(
                "Running BM25 search."
            )

            tokenized_query = query.lower().split()

            # scores = self._index.get_scores(
            #     tokenized_query
            # )
            
            scores = _bm25.get_scores(
                            tokenized_query
                        )

            # ranked = sorted(
            #     zip(
            #         scores,
            #         self._documents
            #     ),
            #     key=lambda item: item[0],
            #     reverse=True
            # )
            
            ranked = sorted(
                            zip(
                                scores,
                                _documents_global
                            ),
                            key=lambda item: item[0],
                            reverse=True
                        )

            results = []

            for score, document in ranked[:top_k]:

                results.append(
                    RetrievedChunk(
                        chunk_id=document.id,
                        content=document.page_content,
                        score=float(score),
                        metadata=document.metadata
                    )
                )

            return results

        except Exception as error:

            logger.exception(
                "BM25 search failed."
            )

            raise BM25Error(
                str(error)
            ) from error