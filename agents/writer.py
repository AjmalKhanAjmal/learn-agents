from langchain.agents import create_agent
from langchain_groq import ChatGroq


def build_writer(tools):

    model = ChatGroq(
        model="llama-3.1-8b-instant"
    )

    writer = create_agent(
        model=model,
        tools=tools,
        system_prompt="""
You are a writer agent.

Responsibilities:
- summarize information
- write articles
- generate reports
"""
    )

    return writer