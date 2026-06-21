# from langchain_text_splitters import RecursiveCharacterTextSplitter

# def split_text(text):
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=500,
#         chunk_overlap=50
#     )

#     return splitter.split_text(text)


# from langchain_text_splitters import RecursiveCharacterTextSplitter  

from langchain_experimental.text_splitter import SemanticChunker

# def split_text(text):

#     splitter = RecursiveCharacterTextSplitter(
#         # chunk_size=500,
#         # chunk_overlap=50
#         chunk_size = 100,
#         chunk_overlap = 0
#     )

#     return splitter.split_text(text)


from langchain_experimental.text_splitter import SemanticChunker
from app.rag.embedder import embeddings
 
def split_text(text):

    splitter = SemanticChunker(
        embeddings()
    )

    docs = splitter.create_documents([text])

    chunks = [
        doc.page_content
        for doc in docs
    ]

    print("Total Semantic Chunks:", len(chunks))

    # for i, chunk in enumerate(chunks):
    #     print(f"\n===== Chunk {i+1} =====")
    #     print(chunk)
#hello sdsd
    return chunks