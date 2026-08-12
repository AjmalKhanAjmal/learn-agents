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


from app.rag.embedder import SentenceTransformerEmbedder



def test_split():
    text =  [
    "NovaTech Enterprise Knowledge Base \nSection 1: Company Background \nNovaTech Solutions was founded in 2021 as a software engineering and research company. \nThe\n \norganization\n \ndevelops\n \nenterprise\n \napplications,\n \ncloud\n \nplatforms,\n \nartificial\n \nintelligence\n \nsystems,\n \nand\n \ndata-processing\n \ntools.\n \nDuring its first year, the company relied heavily on traditional keyword search for internal \ndocuments.\n \nEmployees\n \nsearched\n \ntechnical\n \nmanuals,\n \nproject\n \nreports,\n \nincident\n \nrecords,\n \nand\n \ncustomer-support\n \ndocuments\n \nby\n \ntyping\n \nexact\n \nwords.\n \nThe company later discovered that exact keyword matching was not sufficient for many \nnatural-language\n \nquestions.\n \nDifferent\n \nteams\n \noften\n \nused\n \ndifferent\n \nwords\n \nto\n \ndescribe\n \nthe\n \nsame\n \ntechnical\n \nconcept.\n \nFor example, backend engineers used the phrase \"REST APIs,\" while product managers often \ncalled\n \nthe\n \nsame\n \ncomponents\n \n\"backend\n \nservices.\"\n \nSupport\n \nengineers\n \nsometimes\n \nreferred\n \nto"
  ]
    print("test.length", len(text))
    
    data = SentenceTransformerEmbedder()
    result = data.embed_documents(text)
    
    print("result.length", len(result))

    # assert result