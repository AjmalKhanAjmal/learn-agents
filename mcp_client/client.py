from langchain_mcp_adapters.client import MultiServerMCPClient


async def get_tools():

    client = MultiServerMCPClient(
        {
            "search": {
                "transport": "streamable_http",
                "url": "http://127.0.0.1:8000/mcp",
            }
        }
    )

    tools = await client.get_tools()

    return tools



    #    "content": {
    #             "transport": "streamable_http",
    #             "url": "http://127.0.0.1:8001/mcp",
    #         }