from typing import TypedDict

from langgraph.graph import END, StateGraph

from agents.researcher import build_researcher
from agents.writer import build_writer
from mcp_client.client import get_tools


class AgentState(TypedDict):
    query: str
    research: str
    article: str


async def researcher_node(state):

    tools = await get_tools()

    researcher = build_researcher(tools)

    result = await researcher.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": state["query"]
                }
            ]
        }
    )

    return {
        "research": str(result)
    }


async def writer_node(state):

    tools = await get_tools()

    writer = build_writer(tools)

    result = await writer.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"""
Research:

{state['research']}

Write article.
"""
                }
            ]
        }
    )

    return {
        "article": str(result)
    }


workflow = StateGraph(AgentState)

workflow.add_node("researcher", researcher_node)
workflow.add_node("writer", writer_node)

workflow.set_entry_point("researcher")

workflow.add_edge("researcher", "writer")
workflow.add_edge("writer", END)

graph = workflow.compile()