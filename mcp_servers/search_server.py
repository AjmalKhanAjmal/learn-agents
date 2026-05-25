import os

from tavily import TavilyClient
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("Search Server")

tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


@mcp.tool()
def web_search(query: str) -> str:

    result = tavily.search(query=query)

    return str(result)



@mcp.tool()
def summarize(text: str) -> str:

    return f"""
Summary:

{text[:500]}
"""


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http"
    )