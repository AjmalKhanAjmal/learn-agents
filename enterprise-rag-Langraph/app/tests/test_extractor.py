from app.rag.extractor import PDFExtractor

def test_extract():

    extractor = PDFExtractor()

    text = extractor.extract("uploads/sample.pdf")

    assert len(text) > 0