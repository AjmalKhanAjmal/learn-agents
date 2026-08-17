from abc import ABC, abstractmethod

from rank_bm25 import BM25Okapi

from app.core.logger import logger
# from app.core.exceptions import BM25Error


class BaseKeywordStore(ABC):
    """
    Interface for keyword search providers.
    """

    @abstractmethod
    def create_index(
        self,
        documents: list[str]
    ) -> int:
        pass

    @abstractmethod
    def search(
        self,
        query: str,
        top_k: int = 5
    ) -> list[str]:
        pass


class BM25Store(BaseKeywordStore):
    """
    BM25 keyword index.
    """

    def __init__(self):

        self._index = None

        self._documents = []

    def create_index(
        self,
        documents: list[str]
    ) -> int:

        try:

            logger.info(
                "Creating BM25 index."
            )

            tokenized = [
                doc.page_content.lower().split()
                for doc in documents
            ]
            

            self._index = BM25Okapi(
                tokenized
            )

            self._documents = documents

            logger.info(
                "BM25 indexed %d chunks.",
                len(documents)
            )

            return len(documents)

        except Exception as error:

            logger.exception(
                "BM25 indexing failed."
            )
            
            raise error
            # raise BM25Error(
            #     str(error)
            # ) from error

    def search(
        self,
        query: str,
        top_k: int = 5
    ) -> list[str]:

        if self._index is None:

            raise BM25Error(
                "BM25 index is empty."
            )

        try:

            logger.info(
                "Running BM25 search."
            )

            tokenized_query = query.lower().split()

            scores = self._index.get_scores(
                tokenized_query
            )

            ranked = sorted(
                zip(
                    scores,
                    self._documents
                ),
                reverse=True
            )

            return [
                document
                for _, document in ranked[:top_k]
            ]

        except Exception as error:

            logger.exception(
                "BM25 search failed."
            )

            raise BM25Error(
                str(error)
            ) from error