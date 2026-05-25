from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Content Server")


@mcp.tool()
def summarize(text: str) -> str:

    return f"""
Summary:

{text[:500]}
"""


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        port=8001
    )