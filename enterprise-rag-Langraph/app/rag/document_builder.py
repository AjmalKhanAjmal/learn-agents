from langchain_core.documents import Document
from app.core.logger import logger

from langchain_core.documents import Document

from app.core.logger import logger


class DocumentBuilder:

    @staticmethod
    def build(
        chunks: list[Document],
        file_path,
        document_id
    ) -> list[Document]:

        try:

            logger.info(
                "Started document builder."
            )

            for index, document in enumerate(chunks):

                chunk_id = (
                    f"{document_id}_chunk_{index}"
                )

                document.id = chunk_id

                document.metadata = {
                    "chunk_id": chunk_id,
                    "document_id": document_id,
                    "tenant_id": 122334445,
                    "source": str(file_path),
                    "chunk_index": index,
                }

            logger.info(
                "Completed building documents."
            )

            return chunks

        except Exception as error:

            logger.exception(
                "Failed to build document metadata."
            )

            raise
        # documents.append({document.page_content :})

        # for document, score in retrieved_data:
        #     results.append(
        #         RetrievedChunk(
        #             chunk_id=document.id, content=document.page_content, score=score
        #         )
        #     )
