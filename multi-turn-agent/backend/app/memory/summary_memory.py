from langchain.memory import ConversationSummaryMemory
from langchain_groq import ChatGroq


llm = ChatGroq(
    model_name="llama3-8b-8192"
)


summary_memory = ConversationSummaryMemory(
    llm=llm,
    return_messages=True
)