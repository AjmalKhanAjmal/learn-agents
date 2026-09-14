import re

from app.schemas.generation import Citation
from app.schemas.retrieval import RetrievedChunk


class CitationService:

    CITATION_PATTERN = re.compile(
        r"\[chunk:([^\]]+)\]"
    )

    def extract(
        self,
        answer: str,
        documents: list[RetrievedChunk],
    ) -> list[Citation]:

        document_map = {
            document.chunk_id: document
            for document in documents
        }

        matches = self.CITATION_PATTERN.findall(
            answer
        )

        citations: list[Citation] = []

        seen: set[str] = set()

        for chunk_id in matches:

            if chunk_id in seen:
                continue

            document = document_map.get(
                chunk_id
            )

            if document is None:
                continue

            metadata = document.metadata or {}

            citations.append(
                Citation(
                    citation_id=chunk_id,
                    chunk_id=chunk_id,
                    source=metadata.get(
                        "source"
                    ),
                    title=metadata.get(
                        "title"
                    ),
                )
            )

            seen.add(chunk_id)

        return citations