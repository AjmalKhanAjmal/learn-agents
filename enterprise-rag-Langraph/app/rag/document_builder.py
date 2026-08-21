from langchain_core.documents import Document
from app.core.logger import logger


class DocumentBuilder:
    @staticmethod
    def build(chunks: list[Document], file_path, document_id) -> list[Document]:
        try:
            logger.info("started document builder ")
            for index, document in enumerate(chunks):
                document.metadata = {
                    "document_id": document_id,
                    "tenant_id": 122334445,
                    "source": str(file_path),
                    "chunk_index": index,
                }
            logger.info("completed building documents")
            return chunks
        except Exception as error:
            logger.error("Failed to build document metadata.")
            raise error
        # documents.append({document.page_content :})

        # for document, score in retrieved_data:
        #     results.append(
        #         RetrievedChunk(
        #             chunk_id=document.id, content=document.page_content, score=score
        #         )
        #     )
