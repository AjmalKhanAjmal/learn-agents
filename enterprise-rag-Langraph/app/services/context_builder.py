from app.schemas.retrieval import RetrievedChunk


class contextBuilder:
    def __init__(self,max_chunks: int = 8):
        self.max_chunks = max_chunks
    
    def build(self,documents:list[RetrievedChunk])->str:
        try:
            
            documents = documents[:self.max_chunks]
            # return documents
            sections: list[str] = []
            if not documents:
                return "No relevant context was retrieved."
            
            for index, document in enumerate(documents,start = 1):
                # chunk_id = document.chunk_id
                # source = document.source
                # title = document.title 
                chunk_id = document["chunk_id"]
                source =document["content"]
                title = document["score"]
                
                sections.append(
                                    f"""
                    --- DOCUMENT {index} ---
                    chunk_id: {chunk_id}
                    source: {source}
                    title: {title}
    
                    content:
                    {document['content']}
                    --- END DOCUMENT {index} ---
                    """.strip()
                                )
    
            return "\n\n".join(sections)
        except Exception as error:
            raise error

        