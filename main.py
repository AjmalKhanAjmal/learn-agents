import asyncio

from graph.workflow import graph

from dotenv import load_dotenv

load_dotenv()

async def main():

    result = await graph.ainvoke(
        {
            "query": "Latest AI trends in 2026"
        }
    )

    print("\nFINAL ARTICLE:\n")

    print(result["article"])


if __name__ == "__main__":
    asyncio.run(main())