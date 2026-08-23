# app/rag/result_fusion.py

from abc import ABC, abstractmethod

from app.core.logger import logger
from app.core.exceptions import RetrievalError


class BaseResultFusion(ABC):

    @abstractmethod
    def fuse(
        self,
        semantic_results,
        keyword_results,
        top_k: int = 5
    ):
        pass


class RRFFusion(BaseResultFusion):

    def __init__(self, rrf_k: int = 60):

        self.rrf_k = rrf_k

    def fuse(
        self,
        semantic_results,
        keyword_results,
        top_k: int = 5
    ):

        try:

            logger.info(
                "Starting RRF result fusion."
            )

            scores = {}
            documents = {}

            self._process_results(
                semantic_results,
                scores,
                documents
            )

            self._process_results(
                keyword_results,
                scores,
                documents
            )

            ranked_results = sorted(
                scores.items(),
                key=lambda item: item[1],
                reverse=True
            )

            results = []

            for document_key, fusion_score in ranked_results[:top_k]:

                result = documents[document_key].copy()

                result["fusion_score"] = fusion_score

                results.append(result)

            logger.info(
                "RRF fusion completed. %d results returned.",
                len(results)
            )

            return results

        except Exception as error:

            logger.exception(
                "RRF result fusion failed."
            )

            raise RetrievalError(
                str(error)
            ) from error

    def _process_results(
        self,
        results,
        scores,
        documents
    ):

        for rank, result in enumerate(results, start=1):

            document = self._normalize_result(
                result
            )

            document_key = self._get_document_key(
                document
            )

            rrf_score = 1 / (
                self.rrf_k + rank
            )

            scores[document_key] = (
                scores.get(document_key, 0)
                + rrf_score
            )

            if document_key not in documents:

                documents[document_key] = document

    def _normalize_result(self, result):

        if isinstance(result, dict):

            return {
                "document": result.get(
                    "document",
                    ""
                ),
                "score": result.get(
                    "score"
                ),
                "metadata": result.get(
                    "metadata",
                    {}
                )
            }

        return {
            "document": result,
            "score": None,
            "metadata": {}
        }

    def _get_document_key(self, document):

        return document["document"].strip()