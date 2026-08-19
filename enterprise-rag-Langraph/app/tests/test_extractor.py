# from app.rag import RecursiveTextSplitter
# from app.rag.extractor import PDFExtractor

# def test_extract():
#     splitter =  RecursiveTextSplitter()
#     # final_data = splitter.split()
#     final_data = splitter.split("Hello World")
#     return final_data
#     # extractor = PDFExtractor()

#     # text = extractor.extract("uploads/sample.pdf")

#     # assert len(text) > 0
#     # dataa = splitter    


# from app.rag.vector_store import PineconeVectorStoreService

from app.rag.vector_store import PineconeVectorStoreService
from app.rag.embedder import SentenceTransformerEmbedder



def test_split():
  
  query = "What is vector databases?"
  embedding_service = SentenceTransformerEmbedder()
  embeddings = embedding_service.get_embeddings()
  data = PineconeVectorStoreService(embeddings = embeddings)

  results = data.similarity_search(query,3,0.5)
  print("results : ", results)
  
  
  
  
  
  
  
  
  
  #   text =  [
  #   "NovaTech Enterprise Knowledge Base \nSection 1: Company Background \n"
  # ]
  #   # texts = [doc.page_content for doc in text]
    
  #   print("test.length", len(text))
    
  #   data = PineconeVectorStoreService()
  #   result = data.post_documents(text)
    
    
  #   print("result.length", len(result))

  #   # assert result