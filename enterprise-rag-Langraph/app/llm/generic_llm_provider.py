from app.core.config import settings
from langchain.chat_models import init_chat_model


class GenericLLMProvider:
    def __init__(
        self,
        timeout: float = 60.0,
    ):
        self.model = settings.GROQ_MODEL
        self.api_key = settings.GROQ_API_KEY
        self.llm_provider = settings.LLM_PROVIDER
        self.llm_temperature = settings.LLM_TEMPERATURE

        self.llm = init_chat_model(
            api_key=self.api_key,
            model=self.model,
            model_provider=self.llm_provider,
            temperature=self.llm_temperature,
        )

    def structured(self, schema):

        return self.llm.with_structured_output(schema)


# from app.core.config import settings
# from langchain.chat_models import init_chat_model


# class GenericLLMProvider:

#     def __init__(
#         self,
#         timeout: float = 60.0,
#     ):
#         self.model = settings.GROQ_MODEL
#         self.api_key = settings.GROQ_API_KEY
#         self.llm_provider = settings.LLM_PROVIDER
#         self.llm_temperature = settings.LLM_TEMPERATURE

#         self.llm = init_chat_model(
#             model=self.model,
#             model_provider=self.llm_provider,
#             api_key=self.api_key,
#             temperature=self.llm_temperature,
#             timeout=timeout,
#         )

#     def structured(self, schema):

#         return self.llm.with_structured_output(
#             schema,
#             method="json_schema",
#         )
