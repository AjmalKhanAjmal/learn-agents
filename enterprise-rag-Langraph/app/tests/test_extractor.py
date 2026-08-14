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


from app.rag.vector_store import PineconeVectorStoreService



def test_split():
    text =  [
    "NovaTech Enterprise Knowledge Base \nSection 1: Company Background \n"
  ]
    # texts = [doc.page_content for doc in text]
    
    print("test.length", len(text))
    
    data = PineconeVectorStoreService()
    result = data.post_documents(text)
    
    
    print("result.length", len(result))

    # assert result