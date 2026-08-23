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



from app.routes.retrieval import search
from app.schemas.retrieval import RetrievalRequest
from app.dependencies import get_retrieval_service

def test_search():

    request = RetrievalRequest(
        query="What is NovaTech Enterprise Knowledge Base",
        top_k=5,
        score_threshold = 0.0
    )

    service = get_retrieval_service()

    response = search(
        request=request,
        service=service
    )

    print(response)

    assert response is not None