from app.graph.nodes import analyze_query, retrieve_documents
from langgraph.graph import START, StateGraph
from app.graph.state import AgentState


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("analyze_query", analyze_query)
    graph.add_node("retrieve_documents", retrieve_documents)
    graph.add_edge(START, "analyze_query")
    graph.add_edge("analyze_query", "retrieve_documents")

    return graph.compile()
    # return graph


# from langgraph.graph import (
#     StateGraph,
#     START,
#     END,
# )

# from app.graph.state import AgentState
# from app.graph.nodes import (
#     analyze_query,
#     retrieve_documents,
#     evaluate_evidence,
#     rewrite_query,
#     generate_answer,
#     validate_answer,
# )


# def build_graph():

#     graph = StateGraph(AgentState)

#     graph.add_node("analyze_query", analyze_query)

#     graph.add_node("retrieve_documents", retrieve_documents)

#     graph.add_node("evaluate_evidence", evaluate_evidence)

#     graph.add_node("rewrite_query", rewrite_query)

#     graph.add_node("generate_answer", generate_answer)

#     graph.add_node("validate_answer", validate_answer)

#     graph.add_edge(START, "analyze_query")

#     graph.add_conditional_edges(
#         "analyze_query",
#         route_after_analysis,
#         {
#             "retrieve": "retrieve_documents",
#             "generate": "generate_answer",
#         },
#     )

#     graph.add_edge("retrieve_documents", "evaluate_evidence")

#     graph.add_conditional_edges(
#         "evaluate_evidence",
#         route_after_evidence,
#         {
#             "rewrite": "rewrite_query",
#             "generate": "generate_answer",
#         },
#     )

#     graph.add_edge("rewrite_query", "retrieve_documents")

#     graph.add_edge("generate_answer", "validate_answer")

#     graph.add_conditional_edges(
#         "validate_answer",
#         route_after_validation,
#         {
#             "answer": END,
#             "retry": "rewrite_query",
#         },
#     )

#     return graph
