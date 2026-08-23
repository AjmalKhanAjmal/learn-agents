from abc import ABC, abstractmethod

from rank_bm25 import BM25Okapi
from langchain_core.documents import Document
from app.core.exceptions import BM25Error
from app.core.logger import logger
from app.schemas.retrieval import RetrievedChunk


class BaseKeywordStore(ABC):

    @abstractmethod
    def create_index(
        self,
        documents: list[Document]
    ) -> int:
        pass

    @abstractmethod
    def search(
        self,
        query: str,
        top_k: int = 5
    ) -> list[Document]:
        pass


class BM25Store(BaseKeywordStore):

    def __init__(self):

        self._index = None

        self._documents: list[Document] = []

    def create_index(
        self,
        documents: list[Document]
    ) -> int:
        global _documents_global
        global _bm25
        _documents_global = documents
        try:

            logger.info(
                "Creating BM25 index."
            )

            tokenized = [
                document.page_content.lower().split()
                for document in documents
            ]
            
            
# chunk - 1 ['novatech', 'enterprise', 'knowledge', ]
# chunk - 2
# ['for', 'example,', 'backend', 'engineers',]
# chunk - 3
# ['responsibility']  all in one array

            
            self._index = BM25Okapi(
                tokenized
            )
            _bm25 = self._index

            # self._documents = documents

            logger.info(
                "BM25 indexed %d chunks.",
                len(documents)
            )

            return len(documents)

        except Exception as error:

            logger.exception(
                "BM25 indexing failed."
            )

            raise BM25Error(
                str(error)
            ) from error

    def search(
        self,
        query: str,
        top_k: int = 5
    ) -> list[RetrievedChunk]:

        # if self._index is None:

        #     raise BM25Error(
        #         "BM25 index is empty."
        #     )

        try:
                       
            tokenized_query = query.lower().split()

            # scores = self._index.get_scores(   //old
            #     tokenized_query
            # )
         
            
            # ranked = sorted( //old
            #     zip(
            #         scores,
            #         self._documents
            #     ),
            #     key=lambda item: item[0],
            #     reverse=True
            # )
            _documents_global=[{
      "unique_chunk_id": "document_123_chunk_0",
      "metadata": {
        "chunk_id": "document_123_chunk_0",
        "document_id": "document_123",
        "tenant_id": 122334445,
        "source": "uploads\\ab0f546b-b851-4da0-83b1-913ed0bc1a8a.pdf",
        "chunk_index": 0,
        "text": "NovaTech Enterprise Knowledge Base \nSection 1: Company Background \nNovaTech Solutions was founded in 2021 as a software engineering and research company. \nThe\n \norganization\n \ndevelops\n \nenterprise\n \napplications,\n \ncloud\n \nplatforms,\n \nartificial\n \nintelligence\n \nsystems,\n \nand\n \ndata-processing\n \ntools.\n \nDuring its first year, the company relied heavily on traditional keyword search for internal \ndocuments.\n \nEmployees\n \nsearched\n \ntechnical\n \nmanuals,\n \nproject\n \nreports,\n \nincident\n \nrecords,\n \nand\n \ncustomer-support\n \ndocuments\n \nby\n \ntyping\n \nexact\n \nwords.\n \nThe company later discovered that exact keyword matching was not sufficient for many \nnatural-language\n \nquestions.\n \nDifferent\n \nteams\n \noften\n \nused\n \ndifferent\n \nwords\n \nto\n \ndescribe\n \nthe\n \nsame\n \ntechnical\n \nconcept.\n \nFor example, backend engineers used the phrase \"REST APIs,\" while product managers often \ncalled\n \nthe\n \nsame\n \ncomponents\n \n\"backend\n \nservices.\"\n \nSupport\n \nengineers\n \nsometimes\n \nreferred\n \nto"
      },
      "page_content": "NovaTech Enterprise Knowledge Base \nSection 1: Company Background \nNovaTech Solutions was founded in 2021 as a software engineering and research company. \nThe\n \norganization\n \ndevelops\n \nenterprise\n \napplications,\n \ncloud\n \nplatforms,\n \nartificial\n \nintelligence\n \nsystems,\n \nand\n \ndata-processing\n \ntools.\n \nDuring its first year, the company relied heavily on traditional keyword search for internal \ndocuments.\n \nEmployees\n \nsearched\n \ntechnical\n \nmanuals,\n \nproject\n \nreports,\n \nincident\n \nrecords,\n \nand\n \ncustomer-support\n \ndocuments\n \nby\n \ntyping\n \nexact\n \nwords.\n \nThe company later discovered that exact keyword matching was not sufficient for many \nnatural-language\n \nquestions.\n \nDifferent\n \nteams\n \noften\n \nused\n \ndifferent\n \nwords\n \nto\n \ndescribe\n \nthe\n \nsame\n \ntechnical\n \nconcept.\n \nFor example, backend engineers used the phrase \"REST APIs,\" while product managers often \ncalled\n \nthe\n \nsame\n \ncomponents\n \n\"backend\n \nservices.\"\n \nSupport\n \nengineers\n \nsometimes\n \nreferred\n \nto",
      "type": "Document"
    },
    {
      "id": "document_123_chunk_1",
      "metadata": {
        "chunk_id": "document_123_chunk_1",
        "document_id": "document_123",
        "tenant_id": 122334445,
        "source": "uploads\\ab0f546b-b851-4da0-83b1-913ed0bc1a8a.pdf",
        "chunk_index": 1,
        "text": "For example, backend engineers used the phrase \"REST APIs,\" while product managers often \ncalled\n \nthe\n \nsame\n \ncomponents\n \n\"backend\n \nservices.\"\n \nSupport\n \nengineers\n \nsometimes\n \nreferred\n \nto\n \nthem\n \nas\n \n\"server\n \nendpoints.\"\n \nBecause these expressions used different words, traditional keyword search sometimes failed to \nretrieve\n \nthe\n \ncorrect\n \ndocuments.\n \n \nSection 2: Employee Engineering Profile \nAziz Khan joined NovaTech as a backend software engineer. He worked primarily with Python, \nFastAPI,\n \nMySQL,\n \nRedis,\n \nand\n \nREST\n \nAPIs.\n \nHis responsibilities included developing product-management endpoints, implementing \nauthentication,\n \ncreating\n \nauthorization\n \nrules,\n \nintegrating\n \npayment\n \ngateways,\n \nand\n \nimproving\n \ndatabase\n \nqueries.\n \nAziz also contributed to frontend applications using React and Redux, although his primary \nresponsibility\n \nremained\n \nbackend\n \ndevelopment.\n \nThe e-commerce platform supported more than 10,000 daily users."
      },
      "page_content": "For example, backend engineers used the phrase \"REST APIs,\" while product managers often \ncalled\n \nthe\n \nsame\n \ncomponents\n \n\"backend\n \nservices.\"\n \nSupport\n \nengineers\n \nsometimes\n \nreferred\n \nto\n \nthem\n \nas\n \n\"server\n \nendpoints.\"\n \nBecause these expressions used different words, traditional keyword search sometimes failed to \nretrieve\n \nthe\n \ncorrect\n \ndocuments.\n \n \nSection 2: Employee Engineering Profile \nAziz Khan joined NovaTech as a backend software engineer. He worked primarily with Python, \nFastAPI,\n \nMySQL,\n \nRedis,\n \nand\n \nREST\n \nAPIs.\n \nHis responsibilities included developing product-management endpoints, implementing \nauthentication,\n \ncreating\n \nauthorization\n \nrules,\n \nintegrating\n \npayment\n \ngateways,\n \nand\n \nimproving\n \ndatabase\n \nqueries.\n \nAziz also contributed to frontend applications using React and Redux, although his primary \nresponsibility\n \nremained\n \nbackend\n \ndevelopment.\n \nThe e-commerce platform supported more than 10,000 daily users.",
      "type": "Document"
    },
    {
      "id": "document_123_chunk_2",
      "metadata": {
        "chunk_id": "document_123_chunk_2",
        "document_id": "document_123",
        "tenant_id": 122334445,
        "source": "uploads\\ab0f546b-b851-4da0-83b1-913ed0bc1a8a.pdf",
        "chunk_index": 2,
        "text": "responsibility\n \nremained\n \nbackend\n \ndevelopment.\n \nThe e-commerce platform supported more than 10,000 daily users. \nDatabase indexing reduced the average response time of several product queries."
      },
      "page_content": "responsibility\n \nremained\n \nbackend\n \ndevelopment.\n \nThe e-commerce platform supported more than 10,000 daily users. \nDatabase indexing reduced the average response time of several product queries.",
      "type": "Document"
    },
    {
      "id": "document_123_chunk_3",
      "metadata": {
        "chunk_id": "document_123_chunk_3",
        "document_id": "document_123",
        "tenant_id": 122334445,
        "source": "uploads\\ab0f546b-b851-4da0-83b1-913ed0bc1a8a.pdf",
        "chunk_index": 3,
        "text": "Section 3: General API Performance Improvement \nThe engineering department investigated several methods for improving API performance. \nSome services were slow because database queries scanned large tables. Engineers created \nindexes\n \nfor\n \nfrequently\n \nsearched\n \ncolumns\n \nand\n \noptimized\n \nSQL\n \nqueries.\n \nOther services were slow because they repeatedly requested the same information from \nexternal\n \nsystems.\n \nThe\n \nteam\n \nintroduced\n \ncaching\n \nto\n \nreduce\n \nunnecessary\n \nnetwork\n \ncalls.\n \nThese general improvements reduced latency across several internal applications. \nHowever, this section does not describe the special incident involving the payment service. \n \nSection 4: Payment Service Incident INC-7742 \nOn March 14, the payment-processing service experienced severe latency during evening \ntraffic.\n \nThe internal incident identifier was INC-7742. \nInitial monitoring showed that CPU usage remained normal. Database utilization was also within \nacceptable\n \nlimits."
      },
      "page_content": "Section 3: General API Performance Improvement \nThe engineering department investigated several methods for improving API performance. \nSome services were slow because database queries scanned large tables. Engineers created \nindexes\n \nfor\n \nfrequently\n \nsearched\n \ncolumns\n \nand\n \noptimized\n \nSQL\n \nqueries.\n \nOther services were slow because they repeatedly requested the same information from \nexternal\n \nsystems.\n \nThe\n \nteam\n \nintroduced\n \ncaching\n \nto\n \nreduce\n \nunnecessary\n \nnetwork\n \ncalls.\n \nThese general improvements reduced latency across several internal applications. \nHowever, this section does not describe the special incident involving the payment service. \n \nSection 4: Payment Service Incident INC-7742 \nOn March 14, the payment-processing service experienced severe latency during evening \ntraffic.\n \nThe internal incident identifier was INC-7742. \nInitial monitoring showed that CPU usage remained normal. Database utilization was also within \nacceptable\n \nlimits.",
      "type": "Document"
    },
    {
      "id": "document_123_chunk_4",
      "metadata": {
        "chunk_id": "document_123_chunk_4",
        "document_id": "document_123",
        "tenant_id": 122334445,
        "source": "uploads\\ab0f546b-b851-4da0-83b1-913ed0bc1a8a.pdf",
        "chunk_index": 4,
        "text": "traffic.\n \nThe internal incident identifier was INC-7742. \nInitial monitoring showed that CPU usage remained normal. Database utilization was also within \nacceptable\n \nlimits.\n \nEngineers first suspected MySQL because several payment requests appeared slow. After \ninvestigation,\n \nthey\n \ndiscovered\n \nthat\n \nthe\n \ndatabase\n \nwas\n \nnot\n \nthe\n \nmain\n \ncause.\n \nThe actual problem was repeated calls to an external fraud-detection provider. \nEvery payment request triggered multiple identical fraud-check requests for the same customer \nsession.\n \nThe team solved the incident by storing short-lived fraud-check responses in Redis for ninety \nseconds.\n \nAfter the caching change, repeated external requests decreased significantly and payment \nlatency\n \nreturned\n \nto\n \nnormal.\n \n \nSection 5: Redis Usage in Shopping Cart \nNovaTech also used Redis in the shopping-cart system."
      },
      "page_content": "traffic.\n \nThe internal incident identifier was INC-7742. \nInitial monitoring showed that CPU usage remained normal. Database utilization was also within \nacceptable\n \nlimits.\n \nEngineers first suspected MySQL because several payment requests appeared slow. After \ninvestigation,\n \nthey\n \ndiscovered\n \nthat\n \nthe\n \ndatabase\n \nwas\n \nnot\n \nthe\n \nmain\n \ncause.\n \nThe actual problem was repeated calls to an external fraud-detection provider. \nEvery payment request triggered multiple identical fraud-check requests for the same customer \nsession.\n \nThe team solved the incident by storing short-lived fraud-check responses in Redis for ninety \nseconds.\n \nAfter the caching change, repeated external requests decreased significantly and payment \nlatency\n \nreturned\n \nto\n \nnormal.\n \n \nSection 5: Redis Usage in Shopping Cart \nNovaTech also used Redis in the shopping-cart system.",
      "type": "Document"
    },
    {
      "id": "document_123_chunk_5",
      "metadata": {
        "chunk_id": "document_123_chunk_5",
        "document_id": "document_123",
        "tenant_id": 122334445,
        "source": "uploads\\ab0f546b-b851-4da0-83b1-913ed0bc1a8a.pdf",
        "chunk_index": 5,
        "text": "Temporary cart information was stored in Redis so that customers could quickly add or remove \nproducts.\n \nCart records expired automatically after a configured period of inactivity. \nThis Redis implementation improved shopping-cart responsiveness. \nThe shopping-cart use case was unrelated to the payment incident described elsewhere in this \ndocument.\n \n \nSection 6: Redis Usage in User Sessions \nAnother engineering team used Redis for session management. \nAfter successful login, selected session information was temporarily stored for fast access. \nThis reduced repeated database lookups during authenticated requests. \nThe session-management implementation improved application performance. \nIt was not created to solve payment latency or external fraud-detection calls. \n \nSection 7: Redis Usage in Rate Limiting \nThe API gateway used Redis counters to implement rate limiting. \nFor each client, the gateway tracked the number of requests received during a configured time \nwindow."
      },
      "page_content": "Temporary cart information was stored in Redis so that customers could quickly add or remove \nproducts.\n \nCart records expired automatically after a configured period of inactivity. \nThis Redis implementation improved shopping-cart responsiveness. \nThe shopping-cart use case was unrelated to the payment incident described elsewhere in this \ndocument.\n \n \nSection 6: Redis Usage in User Sessions \nAnother engineering team used Redis for session management. \nAfter successful login, selected session information was temporarily stored for fast access. \nThis reduced repeated database lookups during authenticated requests. \nThe session-management implementation improved application performance. \nIt was not created to solve payment latency or external fraud-detection calls. \n \nSection 7: Redis Usage in Rate Limiting \nThe API gateway used Redis counters to implement rate limiting. \nFor each client, the gateway tracked the number of requests received during a configured time \nwindow.",
      "type": "Document"
    },
    {
      "id": "document_123_chunk_6",
      "metadata": {
        "chunk_id": "document_123_chunk_6",
        "document_id": "document_123",
        "tenant_id": 122334445,
        "source": "uploads\\ab0f546b-b851-4da0-83b1-913ed0bc1a8a.pdf",
        "chunk_index": 6,
        "text": "The API gateway used Redis counters to implement rate limiting. \nFor each client, the gateway tracked the number of requests received during a configured time \nwindow.\n \nWhen a client exceeded the allowed request count, the gateway temporarily rejected additional \nrequests.\n \nThis protected backend systems from excessive traffic. \nThe rate-limiting design was separate from shopping-cart caching, session management, and \npayment\n \nprocessing.\n \n \nSection 8: Authentication Project"
      },
      "page_content": "The API gateway used Redis counters to implement rate limiting. \nFor each client, the gateway tracked the number of requests received during a configured time \nwindow.\n \nWhen a client exceeded the allowed request count, the gateway temporarily rejected additional \nrequests.\n \nThis protected backend systems from excessive traffic. \nThe rate-limiting design was separate from shopping-cart caching, session management, and \npayment\n \nprocessing.\n \n \nSection 8: Authentication Project",
      "type": "Document"
    },
    {
      "id": "document_123_chunk_7",
      "metadata": {
        "chunk_id": "document_123_chunk_7",
        "document_id": "document_123",
        "tenant_id": 122334445,
        "source": "uploads\\ab0f546b-b851-4da0-83b1-913ed0bc1a8a.pdf",
        "chunk_index": 7,
        "text": "The security team implemented authentication using JSON Web Tokens. \nWhen users logged in successfully, the server generated access tokens. \nProtected API endpoints validated the tokens before processing requests. \nRefresh-token logic allowed clients to obtain new access tokens without forcing users to log in \nrepeatedly.\n \nAuthentication answered the question: \"Who is the user?\" \n \nSection 9: Authorization Project \nAuthorization was handled separately from authentication. \nAfter a user was authenticated, the application checked roles and permissions. \nAdministrators could manage products, while ordinary customers could browse products and \nplace\n \norders.\n \nAuthorization answered the question: \"What is this user allowed to do?\" \nAlthough authentication and authorization are related security concepts, they solve different \nproblems.\n \n \nSection 10: Customer Support Ticket TKT-8821 \nA customer reported that an order appeared as \"processing\" for several minutes after payment."
      },
      "page_content": "The security team implemented authentication using JSON Web Tokens. \nWhen users logged in successfully, the server generated access tokens. \nProtected API endpoints validated the tokens before processing requests. \nRefresh-token logic allowed clients to obtain new access tokens without forcing users to log in \nrepeatedly.\n \nAuthentication answered the question: \"Who is the user?\" \n \nSection 9: Authorization Project \nAuthorization was handled separately from authentication. \nAfter a user was authenticated, the application checked roles and permissions. \nAdministrators could manage products, while ordinary customers could browse products and \nplace\n \norders.\n \nAuthorization answered the question: \"What is this user allowed to do?\" \nAlthough authentication and authorization are related security concepts, they solve different \nproblems.\n \n \nSection 10: Customer Support Ticket TKT-8821 \nA customer reported that an order appeared as \"processing\" for several minutes after payment.",
      "type": "Document"
    },
    {
      "id": "document_123_chunk_8",
      "metadata": {
        "chunk_id": "document_123_chunk_8",
        "document_id": "document_123",
        "tenant_id": 122334445,
        "source": "uploads\\ab0f546b-b851-4da0-83b1-913ed0bc1a8a.pdf",
        "chunk_index": 8,
        "text": "problems.\n \n \nSection 10: Customer Support Ticket TKT-8821 \nA customer reported that an order appeared as \"processing\" for several minutes after payment. \nThe support ticket identifier was TKT-8821. \nThe support team initially suspected a payment failure. \nInvestigation showed that the payment had completed successfully. The delay occurred \nbecause\n \nan\n \nasynchronous\n \norder-status\n \nworker\n \nhad\n \ntemporarily\n \nstopped\n \nprocessing\n \nmessages.\n \nRestarting the worker restored normal status updates. \nThis issue was not caused by Redis caching, MySQL indexing, or the external fraud provider."
      },
      "page_content": "problems.\n \n \nSection 10: Customer Support Ticket TKT-8821 \nA customer reported that an order appeared as \"processing\" for several minutes after payment. \nThe support ticket identifier was TKT-8821. \nThe support team initially suspected a payment failure. \nInvestigation showed that the payment had completed successfully. The delay occurred \nbecause\n \nan\n \nasynchronous\n \norder-status\n \nworker\n \nhad\n \ntemporarily\n \nstopped\n \nprocessing\n \nmessages.\n \nRestarting the worker restored normal status updates. \nThis issue was not caused by Redis caching, MySQL indexing, or the external fraud provider.",
      "type": "Document"
    },
    {
      "id": "document_123_chunk_9",
      "metadata": {
        "chunk_id": "document_123_chunk_9",
        "document_id": "document_123",
        "tenant_id": 122334445,
        "source": "uploads\\ab0f546b-b851-4da0-83b1-913ed0bc1a8a.pdf",
        "chunk_index": 9,
        "text": "Section 11: Customer Support Ticket TKT-8822 \nAnother customer reported receiving duplicate email notifications after placing an order. \nThe support ticket identifier was TKT-8822. \nEngineers discovered that a retry mechanism submitted the same notification job more than \nonce.\n \nThe team added idempotency checks before sending emails. \nAfter the change, duplicate notifications stopped. \nThis ticket was unrelated to the order-status worker problem. \n \nSection 12: Customer Support Ticket TKT-8823 \nA third customer reported that the shopping cart became empty after a long period of inactivity. \nThe ticket identifier was TKT-8823. \nInvestigation showed that the behavior was expected because temporary cart records had \nreached\n \ntheir\n \nconfigured\n \nexpiration\n \ntime.\n \nThe engineering team updated the user interface to explain that inactive carts could expire. \nNo payment-service failure occurred in this case. \n \nSection 13: Semantic Search Research"
      },
      "page_content": "Section 11: Customer Support Ticket TKT-8822 \nAnother customer reported receiving duplicate email notifications after placing an order. \nThe support ticket identifier was TKT-8822. \nEngineers discovered that a retry mechanism submitted the same notification job more than \nonce.\n \nThe team added idempotency checks before sending emails. \nAfter the change, duplicate notifications stopped. \nThis ticket was unrelated to the order-status worker problem. \n \nSection 12: Customer Support Ticket TKT-8823 \nA third customer reported that the shopping cart became empty after a long period of inactivity. \nThe ticket identifier was TKT-8823. \nInvestigation showed that the behavior was expected because temporary cart records had \nreached\n \ntheir\n \nconfigured\n \nexpiration\n \ntime.\n \nThe engineering team updated the user interface to explain that inactive carts could expire. \nNo payment-service failure occurred in this case. \n \nSection 13: Semantic Search Research",
      "type": "Document"
    },
    {
      "id": "document_123_chunk_10",
      "metadata": {
        "chunk_id": "document_123_chunk_10",
        "document_id": "document_123",
        "tenant_id": 122334445,
        "source": "uploads\\ab0f546b-b851-4da0-83b1-913ed0bc1a8a.pdf",
        "chunk_index": 10,
        "text": "time.\n \nThe engineering team updated the user interface to explain that inactive carts could expire. \nNo payment-service failure occurred in this case. \n \nSection 13: Semantic Search Research \nThe artificial intelligence team investigated semantic search. \nSemantic search converts text into embeddings and compares vector similarity. \nThis allows a query such as \" What backend components did Aziz build?\" to retrieve a passage \ncontaining\n \n\"Aziz\n \ndeveloped\n \nREST\n \nAPIs,\"\n \neven\n \nthough\n \nthe\n \nexact\n \nwords\n \nare\n \ndifferent.\n \nThe team used vector databases to store embeddings and retrieve semantically related chunks. \nSemantic search performed well for natural-language questions and paraphrased queries."
      },
      "page_content": "time.\n \nThe engineering team updated the user interface to explain that inactive carts could expire. \nNo payment-service failure occurred in this case. \n \nSection 13: Semantic Search Research \nThe artificial intelligence team investigated semantic search. \nSemantic search converts text into embeddings and compares vector similarity. \nThis allows a query such as \" What backend components did Aziz build?\" to retrieve a passage \ncontaining\n \n\"Aziz\n \ndeveloped\n \nREST\n \nAPIs,\"\n \neven\n \nthough\n \nthe\n \nexact\n \nwords\n \nare\n \ndifferent.\n \nThe team used vector databases to store embeddings and retrieve semantically related chunks. \nSemantic search performed well for natural-language questions and paraphrased queries.",
      "type": "Document"
    },
    {
      "id": "document_123_chunk_11",
      "metadata": {
        "chunk_id": "document_123_chunk_11",
        "document_id": "document_123",
        "tenant_id": 122334445,
        "source": "uploads\\ab0f546b-b851-4da0-83b1-913ed0bc1a8a.pdf",
        "chunk_index": 11,
        "text": "Section 14: Keyword Search Research \nThe research team also evaluated keyword retrieval. \nKeyword search performed especially well when users entered exact identifiers, technical \ncodes,\n \nproduct\n \nnames,\n \ninvoice\n \nnumbers,\n \nor\n \nerror\n \nmessages.\n \nFor example, a query containing INC-7742 could directly match a document containing the \nsame\n \nincident\n \nidentifier.\n \nKeyword retrieval was less effective when the query and document used different words with \nsimilar\n \nmeanings.\n \n \nSection 15: Hybrid Search Research \nNovaTech combined semantic retrieval with keyword retrieval. \nThe system executed both retrieval methods and merged their candidate results. \nThis approach was called Hybrid Search. \nSemantic retrieval helped with meaning-based questions. \nKeyword retrieval helped with exact terms such as ticket IDs, incident numbers, framework \nnames,\n \nand\n \nerror\n \ncodes.\n \nHybrid Search improved candidate recall, but the team discovered another problem: the first \nretrieved"
      },
      "page_content": "Section 14: Keyword Search Research \nThe research team also evaluated keyword retrieval. \nKeyword search performed especially well when users entered exact identifiers, technical \ncodes,\n \nproduct\n \nnames,\n \ninvoice\n \nnumbers,\n \nor\n \nerror\n \nmessages.\n \nFor example, a query containing INC-7742 could directly match a document containing the \nsame\n \nincident\n \nidentifier.\n \nKeyword retrieval was less effective when the query and document used different words with \nsimilar\n \nmeanings.\n \n \nSection 15: Hybrid Search Research \nNovaTech combined semantic retrieval with keyword retrieval. \nThe system executed both retrieval methods and merged their candidate results. \nThis approach was called Hybrid Search. \nSemantic retrieval helped with meaning-based questions. \nKeyword retrieval helped with exact terms such as ticket IDs, incident numbers, framework \nnames,\n \nand\n \nerror\n \ncodes.\n \nHybrid Search improved candidate recall, but the team discovered another problem: the first \nretrieved",
      "type": "Document"
    },
    {
      "id": "document_123_chunk_12",
      "metadata": {
        "chunk_id": "document_123_chunk_12",
        "document_id": "document_123",
        "tenant_id": 122334445,
        "source": "uploads\\ab0f546b-b851-4da0-83b1-913ed0bc1a8a.pdf",
        "chunk_index": 12,
        "text": "names,\n \nand\n \nerror\n \ncodes.\n \nHybrid Search improved candidate recall, but the team discovered another problem: the first \nretrieved\n \ncandidates\n \nwere\n \nnot\n \nalways\n \nordered\n \nperfectly.\n \n \nSection 16: Candidate Ranking Problem \nDuring testing, the system retrieved twenty candidate chunks. \nMany candidates contained overlapping words. \nFor example, a question about the payment incident retrieved: \n● the actual payment incident report, ● the general API performance section,"
      },
      "page_content": "names,\n \nand\n \nerror\n \ncodes.\n \nHybrid Search improved candidate recall, but the team discovered another problem: the first \nretrieved\n \ncandidates\n \nwere\n \nnot\n \nalways\n \nordered\n \nperfectly.\n \n \nSection 16: Candidate Ranking Problem \nDuring testing, the system retrieved twenty candidate chunks. \nMany candidates contained overlapping words. \nFor example, a question about the payment incident retrieved: \n● the actual payment incident report, ● the general API performance section,",
      "type": "Document"
    },
    {
      "id": "document_123_chunk_13",
      "metadata": {
        "chunk_id": "document_123_chunk_13",
        "document_id": "document_123",
        "tenant_id": 122334445,
        "source": "uploads\\ab0f546b-b851-4da0-83b1-913ed0bc1a8a.pdf",
        "chunk_index": 13,
        "text": "● the shopping-cart Redis section, ● the session-management Redis section, ● and the rate-limiting Redis section. \nAll these passages contained technical words related to performance, services, caching, or \nRedis.\n \nHowever, only one passage directly explained why the payment service became slow and how \nthe\n \nproblem\n \nwas\n \nfixed.\n \nThe research team concluded that retrieval and ranking were different problems. \n \nSection 17: Re-ranking Research \nTo improve final context quality, NovaTech added a cross-encoder re-ranker. \nThe retrieval system first collected a broad candidate set. \nThe re-ranker then examined each query-document pair more carefully. \nUnlike basic vector similarity, the cross-encoder considered the question and candidate passage \ntogether.\n \nThe system retrieved twenty candidate chunks and then selected the five most relevant chunks \nafter\n \nre-ranking.\n \nThis architecture improved the ordering of confusing, similar-looking passages."
      },
      "page_content": "● the shopping-cart Redis section, ● the session-management Redis section, ● and the rate-limiting Redis section. \nAll these passages contained technical words related to performance, services, caching, or \nRedis.\n \nHowever, only one passage directly explained why the payment service became slow and how \nthe\n \nproblem\n \nwas\n \nfixed.\n \nThe research team concluded that retrieval and ranking were different problems. \n \nSection 17: Re-ranking Research \nTo improve final context quality, NovaTech added a cross-encoder re-ranker. \nThe retrieval system first collected a broad candidate set. \nThe re-ranker then examined each query-document pair more carefully. \nUnlike basic vector similarity, the cross-encoder considered the question and candidate passage \ntogether.\n \nThe system retrieved twenty candidate chunks and then selected the five most relevant chunks \nafter\n \nre-ranking.\n \nThis architecture improved the ordering of confusing, similar-looking passages.",
      "type": "Document"
    },
    {
      "id": "document_123_chunk_14",
      "metadata": {
        "chunk_id": "document_123_chunk_14",
        "document_id": "document_123",
        "tenant_id": 122334445,
        "source": "uploads\\ab0f546b-b851-4da0-83b1-913ed0bc1a8a.pdf",
        "chunk_index": 14,
        "text": "The system retrieved twenty candidate chunks and then selected the five most relevant chunks \nafter\n \nre-ranking.\n \nThis architecture improved the ordering of confusing, similar-looking passages. \n \nSection 18: Machine Learning Model Training \nNovaTech's machine learning team trained a forecasting model to estimate future product \ndemand.\n \nHistorical sales records, seasonal patterns, promotions, and product categories were used as \ntraining\n \nfeatures.\n \nThe forecasting model helped inventory teams estimate future stock requirements. \nThis model-training project was separate from embedding generation and semantic search."
      },
      "page_content": "The system retrieved twenty candidate chunks and then selected the five most relevant chunks \nafter\n \nre-ranking.\n \nThis architecture improved the ordering of confusing, similar-looking passages. \n \nSection 18: Machine Learning Model Training \nNovaTech's machine learning team trained a forecasting model to estimate future product \ndemand.\n \nHistorical sales records, seasonal patterns, promotions, and product categories were used as \ntraining\n \nfeatures.\n \nThe forecasting model helped inventory teams estimate future stock requirements. \nThis model-training project was separate from embedding generation and semantic search.",
      "type": "Document"
    },
    {
      "id": "document_123_chunk_15",
      "metadata": {
        "chunk_id": "document_123_chunk_15",
        "document_id": "document_123",
        "tenant_id": 122334445,
        "source": "uploads\\ab0f546b-b851-4da0-83b1-913ed0bc1a8a.pdf",
        "chunk_index": 15,
        "text": "Section 19: Embedding Model Usage \nThe RAG system used an embedding model to convert text into numerical vectors. \nChunks with related meanings were expected to have nearby vector representations. \nThe embedding model was already trained before NovaTech used it for document indexing. \nUploading a PDF did not retrain the embedding model. \nInstead, the existing model generated vectors for document chunks and user queries. \n \nSection 20: Vector Database Storage \nDocument chunks were converted into embeddings and stored in a vector database. \nWhen a user submitted a question, the same embedding model converted the question into a \nquery\n \nvector.\n \nThe vector database compared the query vector with stored document vectors. \nThe most similar candidates were returned to the retrieval pipeline. \nThe vector database did not generate the final natural-language answer. \n \nSection 21: Large Language Model Role"
      },
      "page_content": "Section 19: Embedding Model Usage \nThe RAG system used an embedding model to convert text into numerical vectors. \nChunks with related meanings were expected to have nearby vector representations. \nThe embedding model was already trained before NovaTech used it for document indexing. \nUploading a PDF did not retrain the embedding model. \nInstead, the existing model generated vectors for document chunks and user queries. \n \nSection 20: Vector Database Storage \nDocument chunks were converted into embeddings and stored in a vector database. \nWhen a user submitted a question, the same embedding model converted the question into a \nquery\n \nvector.\n \nThe vector database compared the query vector with stored document vectors. \nThe most similar candidates were returned to the retrieval pipeline. \nThe vector database did not generate the final natural-language answer. \n \nSection 21: Large Language Model Role",
      "type": "Document"
    },
    {
      "id": "document_123_chunk_16",
      "metadata": {
        "chunk_id": "document_123_chunk_16",
        "document_id": "document_123",
        "tenant_id": 122334445,
        "source": "uploads\\ab0f546b-b851-4da0-83b1-913ed0bc1a8a.pdf",
        "chunk_index": 16,
        "text": "The most similar candidates were returned to the retrieval pipeline. \nThe vector database did not generate the final natural-language answer. \n \nSection 21: Large Language Model Role \nAfter retrieval and re-ranking, the selected chunks were placed into the prompt context. \nThe large language model used that context to generate the final answer. \nThe language model was responsible for answer generation. \nThe embedding model was responsible for vector representation. \nThe vector database was responsible for similarity retrieval. \nThe re-ranker was responsible for improving candidate order. \nThese components had different responsibilities."
      },
      "page_content": "The most similar candidates were returned to the retrieval pipeline. \nThe vector database did not generate the final natural-language answer. \n \nSection 21: Large Language Model Role \nAfter retrieval and re-ranking, the selected chunks were placed into the prompt context. \nThe large language model used that context to generate the final answer. \nThe language model was responsible for answer generation. \nThe embedding model was responsible for vector representation. \nThe vector database was responsible for similarity retrieval. \nThe re-ranker was responsible for improving candidate order. \nThese components had different responsibilities.",
      "type": "Document"
    },
    {
      "id": "document_123_chunk_17",
      "metadata": {
        "chunk_id": "document_123_chunk_17",
        "document_id": "document_123",
        "tenant_id": 122334445,
        "source": "uploads\\ab0f546b-b851-4da0-83b1-913ed0bc1a8a.pdf",
        "chunk_index": 17,
        "text": "Section 22: Agriculture Sensor Project \nA separate NovaTech research division developed smart irrigation systems. \nSensors measured soil moisture in agricultural fields. \nWhen moisture levels dropped below configured thresholds, the system could recommend \nirrigation.\n \nResearchers expected the project to reduce unnecessary water consumption. \nThis project was unrelated to enterprise search and payment processing. \n \nSection 23: Tourism Analytics Project \nNovaTech analysts studied winter tourism patterns. \nPopular destinations included mountain regions, lakes, and forest areas. \nHotels reported higher occupancy during December and January. \nVisitors participating in both mountain and lake activities generally spent more money than \nvisitors\n \nwho\n \nstayed\n \nin\n \none\n \nlocation.\n \nThis analytics project was unrelated to software incident management. \n \nSection 24: Food Preference Survey \nResearchers surveyed visitors about food preferences."
      },
      "page_content": "Section 22: Agriculture Sensor Project \nA separate NovaTech research division developed smart irrigation systems. \nSensors measured soil moisture in agricultural fields. \nWhen moisture levels dropped below configured thresholds, the system could recommend \nirrigation.\n \nResearchers expected the project to reduce unnecessary water consumption. \nThis project was unrelated to enterprise search and payment processing. \n \nSection 23: Tourism Analytics Project \nNovaTech analysts studied winter tourism patterns. \nPopular destinations included mountain regions, lakes, and forest areas. \nHotels reported higher occupancy during December and January. \nVisitors participating in both mountain and lake activities generally spent more money than \nvisitors\n \nwho\n \nstayed\n \nin\n \none\n \nlocation.\n \nThis analytics project was unrelated to software incident management. \n \nSection 24: Food Preference Survey \nResearchers surveyed visitors about food preferences.",
      "type": "Document"
    },
    {
      "id": "document_123_chunk_18",
      "metadata": {
        "chunk_id": "document_123_chunk_18",
        "document_id": "document_123",
        "tenant_id": 122334445,
        "source": "uploads\\ab0f546b-b851-4da0-83b1-913ed0bc1a8a.pdf",
        "chunk_index": 18,
        "text": "stayed\n \nin\n \none\n \nlocation.\n \nThis analytics project was unrelated to software incident management. \n \nSection 24: Food Preference Survey \nResearchers surveyed visitors about food preferences. \nPopular dishes included chicken biryani, fish curry, grilled seafood, and vegetable curry. \nMany participants preferred spicy food during winter. \nRestaurants used the survey when planning seasonal menus. \n \nSection 25: Final Architecture"
      },
      "page_content": "stayed\n \nin\n \none\n \nlocation.\n \nThis analytics project was unrelated to software incident management. \n \nSection 24: Food Preference Survey \nResearchers surveyed visitors about food preferences. \nPopular dishes included chicken biryani, fish curry, grilled seafood, and vegetable curry. \nMany participants preferred spicy food during winter. \nRestaurants used the survey when planning seasonal menus. \n \nSection 25: Final Architecture",
      "type": "Document"
    },
    {
      "id": "document_123_chunk_19",
      "metadata": {
        "chunk_id": "document_123_chunk_19",
        "document_id": "document_123",
        "tenant_id": 122334445,
        "source": "uploads\\ab0f546b-b851-4da0-83b1-913ed0bc1a8a.pdf",
        "chunk_index": 19,
        "text": "NovaTech's production RAG pipeline used multiple stages. \nFirst, documents were divided into chunks. \nSecond, an embedding model generated vector representations. \nThird, dense vectors were stored in a vector database. \nA keyword retrieval system maintained information needed for exact-term matching. \nWhen a user asked a question, semantic retrieval and keyword retrieval produced candidate \npassages.\n \nThe results were combined through the hybrid retrieval process. \nThe system collected a broad set of up to twenty candidate chunks. \nA cross-encoder re-ranker evaluated the candidates against the original question. \nThe five strongest passages were selected. \nThose passages were sent to the large language model as context. \nThe language model then generated the final answer. \nThe company found that broad retrieval improved recall, while re-ranking improved precision in \nthe\n \nfinal\n \ncontext."
      },
      "page_content": "NovaTech's production RAG pipeline used multiple stages. \nFirst, documents were divided into chunks. \nSecond, an embedding model generated vector representations. \nThird, dense vectors were stored in a vector database. \nA keyword retrieval system maintained information needed for exact-term matching. \nWhen a user asked a question, semantic retrieval and keyword retrieval produced candidate \npassages.\n \nThe results were combined through the hybrid retrieval process. \nThe system collected a broad set of up to twenty candidate chunks. \nA cross-encoder re-ranker evaluated the candidates against the original question. \nThe five strongest passages were selected. \nThose passages were sent to the large language model as context. \nThe language model then generated the final answer. \nThe company found that broad retrieval improved recall, while re-ranking improved precision in \nthe\n \nfinal\n \ncontext.",
      "type": "Document"
    }]
            
            
            tokenized = [  #new
                                                    document['page_content'].lower().split()
                                                    for document in _documents_global
                                                ]
            _bm25 = BM25Okapi(  #new
                                     tokenized
                                    )
            
            scores = _bm25.get_scores( #new
                                        tokenized_query
                                    )
            ranked = sorted(
                        zip(
                            scores,
                            _documents_global
                        ),
                        key=lambda item: item[0],
                        reverse=True
                        )

            results = []

            for score, document in ranked[:top_k]:

                results.append(
                    RetrievedChunk(
                        chunk_id=document['metadata']['chunk_id'],
                        content=document['page_content'],
                        score=float(score),
                        metadata=document['metadata']
                    )
                )

            return results

        except Exception as error:

            logger.exception(
                "BM25 search failed."
            )

            raise BM25Error(
                str(error)
            ) from error
            
            
            
            
            
            
