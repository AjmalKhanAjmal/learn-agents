from langgraph.graph import StateGraph
from typing import TypedDict


class ChatState(TypedDict):
    message: str
    response: str


builder = StateGraph(ChatState)


def generate_response(state):

    response = f"AI Response: {state['message']}"

    return {
        "response": response
    }


builder.add_node("chatbot", generate_response)

builder.set_entry_point("chatbot")

builder.set_finish_point("chatbot")


graph = builder.compile()