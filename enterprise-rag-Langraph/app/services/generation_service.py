from app.llm.base import LLMProvider
from app.prompts.rag_prompt import USER_PROMPT_TEMPLATE,SYSTEM_PROMPT
from app.schemas.retrieval import RetrievedChunk
from app.services.context_builder import contextBuilder
from app.services.conversation_builder import ConversationBuilder



class GenerationService:
    def __init__(self,LLMProvider:str):
        self.llm = LLMProvider
        self.context_builder = contextBuilder()
        self.conversation_builder = ConversationBuilder()
        # self.system_prompt =system_prompt
        # self.user_prompt =user_prompt
        # self.max_output_tokens =max_output_tokens
        # self.temperature =temperature
        # self.metadata =metadata
        
    async def generation_service(self,max_output_tokens,temperature,conversation_history:list[dict['str',str]] | None = None,documents:list[RetrievedChunk]=[]):
        query = "Explain what FastAPI is in " "three sentences."
        context = self.context_builder.build(documents)
        conversation = self.conversation_builder.build(conversation_history)
        
        user_prompt = USER_PROMPT_TEMPLATE.format(
            query=query,        
            context=context,
            conversation_history=conversation
        )
        
        # print("user prompt", user_prompt)
        #  user_prompt = USER_PROMPT_TEMPLATE.format(
#             query=query,
#             context=context,
#             conversation_history=conversation,
#         )
        
        result = await self.llm.generate(
                    system_prompt = SYSTEM_PROMPT,
                    user_prompt = user_prompt,
                    max_output_tokens = max_output_tokens,
                    temperature = temperature,
                    metadata={
                        "component": "rag_generation",
                    },
                )
        return result




#     16.1  LLM Base Interface
#         ↓
# 16.2  OpenAI LLM Provider
#         ↓
# 16.3  Configuration
#         ↓
# 16.4  Prompt Builder
#         ↓
# 16.5  Context Builder
#         ↓
# 16.6  Generation Service
#         ↓
# 16.7  Citation Handling
#         ↓
# 16.8  Token Budget Manager

# from typing import Any

# from app.llm.base import LLMProvider
# from app.prompts.rag_prompt import (
#     SYSTEM_PROMPT,
#     USER_PROMPT_TEMPLATE,
# )
# from app.schemas.generation import (
#     GenerationResponse,
# )
# from app.schemas.retrieval import RetrievedChunk
# from app.services.citation_service import (
#     CitationService,
# )
# from app.services.context_builder import (
#     ContextBuilder,
# )
# from app.services.conversation_builder import (
#     ConversationBuilder,
# )


# class GenerationService:

#     def __init__(
#         self,
#         llm: LLMProvider,
#         context_builder: ContextBuilder,
#         conversation_builder: ConversationBuilder,
#         citation_service: CitationService,
#     ):
#         self.llm = llm

#         self.context_builder = context_builder

#         self.conversation_builder = (
#             conversation_builder
#         )

#         self.citation_service = (
#             citation_service
#         )

#     async def generate(
#         self, 
#         *,
#         query: str,
#         documents: list[RetrievedChunk],
#         conversation_history: list[dict[str, str]] | None = None,
#         max_output_tokens: int = 800,
#         temperature: float | None = 0.0,
#     ) -> GenerationResponse:

#         conversation_history = (
#             conversation_history or []
#         )

#         context = self.context_builder.build(
#             documents
#         )

#         conversation = (
#             self.conversation_builder.build(
#                 conversation_history
#             )
#         )

#         user_prompt = USER_PROMPT_TEMPLATE.format(
#             query=query,
#             context=context,
#             conversation_history=conversation,
#         )

#         result = await self.llm.generate(
#             system_prompt=SYSTEM_PROMPT,
#             user_prompt=user_prompt,
#             max_output_tokens=max_output_tokens,
#             temperature=temperature,
#             metadata={
#                 "component": "rag_generation",
#             },
#         )

#         answer = result["text"]

#         citations = self.citation_service.extract(
#             answer,
#             documents,
#         )

#         return GenerationResponse(
#             answer=answer,
#             citations=citations,
#             model=result["model"],
#             usage=result.get(
#                 "usage",
#                 {},
#             ),
#             metadata={
#                 "response_id": result.get(
#                     "response_id"
#                 ),
#                 "retrieved_documents": len(
#                     documents
#                 ),
#                 "citations": len(
#                     citations
#                 ),
#             },
#         )

    # async def stream(
    #     self,
    #     *,
    #     query: str,
    #     documents: list[RetrievedChunk],
    #     conversation_history: list[dict[str, str]] | None = None,
    #     max_output_tokens: int = 800,
    #     temperature: float | None = 0.0,
    # ):

    #     conversation_history = (
    #         conversation_history or []
    #     )

    #     context = self.context_builder.build(
    #         documents
    #     )

    #     conversation = (
    #         self.conversation_builder.build(
    #             conversation_history
    #         )
    #     )

    #     user_prompt = USER_PROMPT_TEMPLATE.format(
    #         query=query,
    #         context=context,
    #         conversation_history=conversation,
    #     )

    #     async for chunk in self.llm.stream(
    #         system_prompt=SYSTEM_PROMPT,
    #         user_prompt=user_prompt,
    #         max_output_tokens=max_output_tokens,
    #         temperature=temperature,
    #         metadata={
    #             "component": "rag_generation",
    #         },
    #     ):

    #         yield chunk