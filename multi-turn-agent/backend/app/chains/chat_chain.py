from langchain_groq import ChatGroq
# from langchain_core.prompts import ChatPromptTemplate
from app.config.settings import settings

def get_chain():
    print("Creating chain")

    llm = ChatGroq(
        groq_api_key=settings.GROQ_API_KEY,
        model_name=settings.MODEL_NAME,
        temperature=0.7
    )

    # prompt = ChatPromptTemplate.from_messages([
    #     ("system", "You are a helpful assistant"),
    #     ("human", "{input}")
    # ])

    prompt = [
        ("system", "You are a helpful assistant"),
        ("human", "{input}")
    ]
    return prompt | llm