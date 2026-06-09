# from fastapi import APIRouter

# from langchain_groq import ChatGroq
# from langchain_core.prompts import ChatPromptTemplate

# from app.core.config import GROQ_API_KEY
# from app.rag.retriever import retrieve
# from app.schemas import ChatRequest

# router = APIRouter()

# llm = ChatGroq(
#     groq_api_key=GROQ_API_KEY,
#     model_name="llama-3.3-70b-versatile"
# )


# @router.post("/chat")
# def chat(request: ChatRequest):

#     docs = retrieve(request.question)

#     context = "\n".join(docs)

#     prompt = ChatPromptTemplate.from_template(
#         """
#         Answer only from context.

#         Context:
#         {context}

#         Question:   
#         {question}
#         """
#     )

#     chain = prompt | llm

#     response = chain.invoke({
#         "context": context,
#         "question": request.question
#     })

#     return {
#         "answer": response.content
#     }



from fastapi import APIRouter

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from app.core.config import GROQ_API_KEY
from app.rag.retriever import retrieve
from app.schemas import ChatRequest

router = APIRouter()

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile"
)


@router.post("/chat")
def chat(request: ChatRequest):

    docs = retrieve(request.question)

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    prompt = ChatPromptTemplate.from_template(
        """
        Answer only from the provided context.

        If the answer is not present in the context,
        say "I could not find that information."

        Context:
        {context}

        Question:
        {question}
        """
    )

    chain = prompt | llm

    response = chain.invoke({
        "context": context,
        "question": request.question
    })

    return {
        "answer": response.content
    }