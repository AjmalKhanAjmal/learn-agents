# pytest -s .\app\tests\test_extractor.py
from app.schemas.retrieval import RetrievedChunk
from app.rerankers.cross_encoder import CrossEncoderReranker

# def test_reranking():
#     reranker_obj = CrossEncoderReranker("medel_reramker",512,16)

#     print(reranker_obj)
    
    
def test_reranking():

    reranker_obj = CrossEncoderReranker(
        model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"
        # batch_size=16,
        # max_length=512
    )

    print(reranker_obj)
