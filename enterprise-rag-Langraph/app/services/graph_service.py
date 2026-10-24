from functools import lru_cache

from app.graph.builder import build_graph
from app.dependencies import get_hybrid_retrieval_service


@lru_cache(maxsize=1)
def get_graph():
    hybrid_retrieval_service = get_hybrid_retrieval_service()
    return build_graph(hybrid_retrieval_service)


async def run_graph(query: str) -> dict:
    graph = get_graph()

    result = await graph.ainvoke({
        "query": query,
    })

    return result