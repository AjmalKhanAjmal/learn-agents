from langchain.agents import create_agent
from langchain_groq import ChatGroq


def build_researcher(tools):

    model = ChatGroq(
        model="llama-3.1-8b-instant"
    )

    researcher = create_agent(
        model=model,
        tools=tools,
        system_prompt="""
You are a research agent.

Your responsibilities:
- search information
- gather facts
- provide detailed research
"""
    )

    return researcher