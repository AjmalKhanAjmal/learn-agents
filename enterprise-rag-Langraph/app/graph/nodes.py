from app.agents.query_analyzer import QueryAnalyzer
from app.dependencies import get_hybrid_retrieval_service

# from app.services.hybrid_retrieval_service import HybridRetrievalService
# from app.routes.hybrid_retrieval import hybrid_retrieval

# from app.services.hybrid_retrieval_service import HybridRetrievalService

query_analyzer = QueryAnalyzer()
# hybrid_retrieval_service = HybridRetrievalService()


def analyze_query(state):
    try:
        result = query_analyzer.analyze(state["query"])
        return {
            "intent": result.intent,
            "requires_retrieval": result.requires_retrieval,
            "requires_multi_hop": result.requires_multi_hop,
            "sub_queries": result.sub_queries,
            "rewritten_query": result.search_query,
            "retrieval_attempt": 0,
        }
    except Exception as error:
        print("error at analyze query", error)
        raise error


# async def retrieve_documents(state):
#     query = state.get("rewritten_query") or state["query"]
#     # results = hybrid_retrieval_service.hybrid_retrievel(query=query, top_k=5)
#     service = get_hybrid_retrieval_service()

#     results = await service.hybrid_retrievel(query=query, top_k=5)
#     return {"query": query, "reranked_results": results}


class RetrievalNode:
    try:

        def __init__(self, hybrid_retrieval_service):
            self.hybrid_retrieval_service = hybrid_retrieval_service
            print("passes")

    except Exception as error:
        print("error in retrtive constructor", error)
        raise error

    try:

        async def __call__(self, state):

            query = state.get("rewritten_query") or state["query"]

            retrievel_results = await self.hybrid_retrieval_service.hybrid_retrievel(
                query, top_k=5
            )

            return {"query": query, "fused_results": retrievel_results}

    except Exception as error:
        print("error in while caling Retrieval function ", error)
        raise error


# class RetrievalNode:

#     def __init__(self, hybrid_retrieval_service):

#         self.hybrid_retrieval_service = (
#             hybrid_retrieval_service
#         )

#     async def __call__(self, state: AgentState):

#         query = (
#             state.get("rewritten_query")
#             or state["query"]
#         )

#         results = await self.hybrid_retrieval_service.hybrid_retrievel(
#             query=query,
#             top_k=5
#         )

#         return {
#             "query": query,
#             "fused_results": results,
#         }


# def retrieve_documents(state):

#     query = state.get("rewritten_query") or state["query"]

#     results = retriever.search(query=query, k=5)

#     attempt = state.get("retrieval_attempt", 0) + 1

#     return {
#         "reranked_results": results,
#         "retrieval_attempt": attempt,
#     }


# from langchain_core.messages import HumanMessage

# from app.agents.query_analyzer import QueryAnalyzer
# from app.retrieval.retriever import HybridRetriever
# from app.generation.service import LLMService

# query_analyzer = QueryAnalyzer()
# retriever = HybridRetriever()
# llm_service = LLMService()


# def analyze_query(state):

#     result = query_analyzer.analyze(state["query"])

#     return {
#         "intent": result.intent,
#         "requires_retrieval": result.requires_retrieval,
#         "requires_multi_hop": result.requires_multi_hop,
#         "sub_queries": result.sub_queries,
#         "rewritten_query": result.search_query,
#         "retrieval_attempt": 0,
#     }


# def retrieve_documents(state):

#     query = state.get("rewritten_query") or state["query"]

#     results = retriever.search(query=query, k=5)

#     attempt = state.get("retrieval_attempt", 0) + 1

#     return {
#         "reranked_results": results,
#         "retrieval_attempt": attempt,
#     }


# def evaluate_evidence(state):

#     documents = state.get("reranked_results", [])

#     if not documents:

#         return {
#             "evidence_sufficient": False,
#             "evidence_score": 0.0,
#             "evidence_reason": "No relevant documents found.",
#         }

#     scores = [d.get("score", 0) for d in documents]

#     average_score = sum(scores) / len(scores) if scores else 0

#     sufficient = len(documents) >= 2 and average_score >= 0.35

#     return {
#         "evidence_sufficient": sufficient,
#         "evidence_score": average_score,
#         "evidence_reason": (
#             "Evidence sufficient."
#             if sufficient
#             else "Evidence quality is insufficient."
#         ),
#     }


# def rewrite_query(state):

#     prompt = f"""
# Rewrite the following enterprise RAG query
# to improve document retrieval.

# Original query:
# {state["query"]}

# Previous query:
# {state.get("rewritten_query", "")}

# Reason:
# {state.get("evidence_reason", "")}

# Return only the rewritten query.
# """

#     response = llm_service.invoke([HumanMessage(content=prompt)])

#     return {"rewritten_query": response.content.strip()}


# def generate_answer(state):

#     documents = state.get("reranked_results", [])

#     context = "\n\n".join(
#         f"[chunk:{d['chunk_id']}]\n" f"{d['content']}" for d in documents
#     )

#     prompt = f"""
# You are an enterprise knowledge assistant.

# Answer the user's question using ONLY
# the supplied context.

# If the context does not contain enough
# information, explicitly say that the
# knowledge base does not contain enough
# information.

# Every factual statement must be supported
# by a citation.

# Citation format:

# [chunk:CHUNK_ID]

# User question:
# {state["query"]}

# Context:
# {context}
# """

#     response = llm_service.invoke([HumanMessage(content=prompt)])

#     return {"answer": response.content}


# def validate_answer(state):

#     answer = state.get("answer", "")

#     documents = state.get("reranked_results", [])

#     if not answer or not documents:

#         return {
#             "grounded": False,
#             "grounding_score": 0.0,
#             "validation_reason": "Missing answer or evidence.",
#         }

#     valid_chunk_ids = {str(d["chunk_id"]) for d in documents}

#     import re

#     cited_ids = re.findall(r"\[chunk:([^\]]+)\]", answer)

#     if not cited_ids:

#         return {
#             "grounded": False,
#             "grounding_score": 0.0,
#             "validation_reason": "No citations found.",
#         }

#     valid = sum(1 for cid in cited_ids if cid in valid_chunk_ids)

#     score = valid / len(cited_ids) if cited_ids else 0

#     return {
#         "grounded": score >= 0.8,
#         "grounding_score": score,
#         "validation_reason": (
#             "Answer citations validated."
#             if score >= 0.8
#             else "Some citations are invalid."
#         ),
#     }
