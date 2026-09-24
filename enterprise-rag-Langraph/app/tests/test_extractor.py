# pytest -s .\app\tests\test_extractor.py
from app.agents.query_analyzer import QueryAnalyzer

import pytest

from app.dependencies import get_hybrid_retrieval_service
from app.graph.builder import build_graph


@pytest.mark.asyncio
async def test_reranking():

    try:
        raw_documents = [
            {
                "chunk_id": "document_123_chunk_0",
                "metadata": {
                    "chunk_id": "document_123_chunk_0",
                    "document_id": "document_123",
                    "tenant_id": 122334445,
                    "source": "uploads\\ab0f546b-b851-4da0-83b1-913ed0bc1a8a.pdf",
                    "chunk_index": 0,
                    "text": 'NovaTech Enterprise Knowledge Base \nSection 1: Company Background \nNovaTech Solutions was founded in 2021 as a software engineering and research company. \nThe\n \norganization\n \ndevelops\n \nenterprise\n \napplications,\n \ncloud\n \nplatforms,\n \nartificial\n \nintelligence\n \nsystems,\n \nand\n \ndata-processing\n \ntools.\n \nDuring its first year, the company relied heavily on traditional keyword search for internal \ndocuments.\n \nEmployees\n \nsearched\n \ntechnical\n \nmanuals,\n \nproject\n \nreports,\n \nincident\n \nrecords,\n \nand\n \ncustomer-support\n \ndocuments\n \nby\n \ntyping\n \nexact\n \nwords.\n \nThe company later discovered that exact keyword matching was not sufficient for many \nnatural-language\n \nquestions.\n \nDifferent\n \nteams\n \noften\n \nused\n \ndifferent\n \nwords\n \nto\n \ndescribe\n \nthe\n \nsame\n \ntechnical\n \nconcept.\n \nFor example, backend engineers used the phrase "REST APIs," while product managers often \ncalled\n \nthe\n \nsame\n \ncomponents\n \n"backend\n \nservices."\n \nSupport\n \nengineers\n \nsometimes\n \nreferred\n \nto',
                },
                "content": 'NovaTech Enterprise Knowledge Base \nSection 1: Company Background \nNovaTech Solutions was founded in 2021 as a software engineering and research company. \nThe\n \norganization\n \ndevelops\n \nenterprise\n \napplications,\n \ncloud\n \nplatforms,\n \nartificial\n \nintelligence\n \nsystems,\n \nand\n \ndata-processing\n \ntools.\n \nDuring its first year, the company relied heavily on traditional keyword search for internal \ndocuments.\n \nEmployees\n \nsearched\n \ntechnical\n \nmanuals,\n \nproject\n \nreports,\n \nincident\n \nrecords,\n \nand\n \ncustomer-support\n \ndocuments\n \nby\n \ntyping\n \nexact\n \nwords.\n \nThe company later discovered that exact keyword matching was not sufficient for many \nnatural-language\n \nquestions.\n \nDifferent\n \nteams\n \noften\n \nused\n \ndifferent\n \nwords\n \nto\n \ndescribe\n \nthe\n \nsame\n \ntechnical\n \nconcept.\n \nFor example, backend engineers used the phrase "REST APIs," while product managers often \ncalled\n \nthe\n \nsame\n \ncomponents\n \n"backend\n \nservices."\n \nSupport\n \nengineers\n \nsometimes\n \nreferred\n \nto',
                "score": 0.6383292,
            },
            {
                "chunk_id": "document_123_chunk_1",
                "metadata": {
                    "chunk_id": "document_123_chunk_1",
                    "document_id": "document_123",
                    "tenant_id": 122334445,
                    "source": "uploads\\ab0f546b-b851-4da0-83b1-913ed0bc1a8a.pdf",
                    "chunk_index": 1,
                    "text": 'For example, backend engineers used the phrase "REST APIs," while product managers often \ncalled\n \nthe\n \nsame\n \ncomponents\n \n"backend\n \nservices."\n \nSupport\n \nengineers\n \nsometimes\n \nreferred\n \nto\n \nthem\n \nas\n \n"server\n \nendpoints."\n \nBecause these expressions used different words, traditional keyword search sometimes failed to \nretrieve\n \nthe\n \ncorrect\n \ndocuments.\n \n \nSection 2: Employee Engineering Profile \nAziz Khan joined NovaTech as a backend software engineer. He worked primarily with Python, \nFastAPI,\n \nMySQL,\n \nRedis,\n \nand\n \nREST\n \nAPIs.\n \nHis responsibilities included developing product-management endpoints, implementing \nauthentication,\n \ncreating\n \nauthorization\n \nrules,\n \nintegrating\n \npayment\n \ngateways,\n \nand\n \nimproving\n \ndatabase\n \nqueries.\n \nAziz also contributed to frontend applications using React and Redux, although his primary \nresponsibility\n \nremained\n \nbackend\n \ndevelopment.\n \nThe e-commerce platform supported more than 10,000 daily users.',
                },
                "content": 'For example, backend engineers used the phrase "REST APIs," while product managers often \ncalled\n \nthe\n \nsame\n \ncomponents\n \n"backend\n \nservices."\n \nSupport\n \nengineers\n \nsometimes\n \nreferred\n \nto\n \nthem\n \nas\n \n"server\n \nendpoints."\n \nBecause these expressions used different words, traditional keyword search sometimes failed to \nretrieve\n \nthe\n \ncorrect\n \ndocuments.\n \n \nSection 2: Employee Engineering Profile \nAziz Khan joined NovaTech as a backend software engineer. He worked primarily with Python, \nFastAPI,\n \nMySQL,\n \nRedis,\n \nand\n \nREST\n \nAPIs.\n \nHis responsibilities included developing product-management endpoints, implementing \nauthentication,\n \ncreating\n \nauthorization\n \nrules,\n \nintegrating\n \npayment\n \ngateways,\n \nand\n \nimproving\n \ndatabase\n \nqueries.\n \nAziz also contributed to frontend applications using React and Redux, although his primary \nresponsibility\n \nremained\n \nbackend\n \ndevelopment.\n \nThe e-commerce platform supported more than 10,000 daily users.',
                "score": 0.1383292,
            },
            {
                "chunk_id": "document_123_chunk_2",
                "metadata": {
                    "chunk_id": "document_123_chunk_2",
                    "document_id": "document_123",
                    "tenant_id": 122334445,
                    "source": "uploads\\ab0f546b-b851-4da0-83b1-913ed0bc1a8a.pdf",
                    "chunk_index": 2,
                    "text": "responsibility\n \nremained\n \nbackend\n \ndevelopment.\n \nThe e-commerce platform supported more than 10,000 daily users. \nDatabase indexing reduced the average response time of several product queries.",
                },
                "content": "responsibility\n \nremained\n \nbackend\n \ndevelopment.\n \nThe e-commerce platform supported more than 10,000 daily users. \nDatabase indexing reduced the average response time of several product queries.",
                "score": 0.383292,
            },
        ]

        # llm_provider = GenericLLMProvider()

        # query_analyzer = QueryAnalyzer()
        # response = query_analyzer.analyze("What is ai?")
        # response = query_analyzer.analyze("What is 10 + 20?")
        # response = query_analyzer.analyze(
        #     "Compare the authentication and database technology used by the payment service and order service."
        # )
        
        hybrid_retrieval_service = get_hybrid_retrieval_service()
        graph = build_graph(hybrid_retrieval_service)

        # response = graph.invoke(
        #     {"query": "What authentication mechanism does the payment service use?"}
        # )

        response = await graph.ainvoke({"query": "What is Nova tech company"})
        print("final results:", response)

    except Exception as error:
        print(error)
