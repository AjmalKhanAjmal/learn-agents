from rank_bm25 import BM25Okapi

_documents = []

_bm25 = None


def create_bm25_index(chunks):

    global _documents
    global _bm25

    _documents = chunks

    tokenized = [
        chunk.lower().split()
        for chunk in chunks
    ]

    _bm25 = BM25Okapi(tokenized)
    print("BM25 Ready")
    return _bm25
    


def search_bm25(query,k=3):

    global _bm25

    if _bm25 is None:
        return []

    tokens = query.lower().split()

    scores = _bm25.get_scores(tokens)
    
    print("_bm25 : ", _bm25)
    
    print("answeer : ", scores)
    ranked = sorted(
        zip(_documents,scores),
        key=lambda x:x[1],
        reverse=True
    )

    return ranked[:k]