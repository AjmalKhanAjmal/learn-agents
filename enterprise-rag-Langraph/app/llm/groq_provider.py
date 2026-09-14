from typing import Any

from app.llm.base import LLMProvider
from groq import AsyncGroq
 
 

class GroqProvider(LLMProvider):
    def __init__(
        self,
        api_key: str,
        model: str,
        timeout: float = 60.0,
    ):
        self.model = model

        self.groq_client = AsyncGroq(api_key=api_key, timeout=timeout)

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        max_output_tokens: int,
        temperature: float | None = None,
        metadata: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]

            request: dict[str, Any] = {
                "model": self.model,
                "messages": messages,
                "max_completion_tokens": max_output_tokens,
                "stream": False,
            }

            if temperature is not None:
                request["temperature"] = temperature

            response = await self.groq_client.chat.completions.create(**request)

            content = response.choices[0].message.content

            usage = {}
            if response.usage:
                usage = {
                    "input_tokens": (response.usage.prompt_tokens),
                    "output_tokens": (response.usage.completion_tokens),
                    "total_tokens": (response.usage.total_tokens),
                }

            return {
                "text": content,
                "response_id": response.id,
                "model": response.model,
                "usage": usage,
            }

        except Exception as error:
            raise error

        # if temperature is not None:
        #     request["temperature"] = temperature

        # try:

        #     response = await self.client.chat.completions.create(
        #         **request
        #     )

        #     choice = response.choices[0]

        #     content = choice.message.content or ""

        #     usage = {}

        #     if response.usage:

        #         usage = {
        #             "input_tokens": (
        #                 response.usage.prompt_tokens
        #             ),
        #             "output_tokens": (
        #                 response.usage.completion_tokens
        #             ),
        #             "total_tokens": (
        #                 response.usage.total_tokens
        #             ),
        #         }

        #     return {
        #         "text": content,
        #         "response_id": response.id,
        #         "model": response.model,
        #         "usage": usage,
        #     }

    async def stream(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        max_output_tokens: int,
        temperature: float | None = None,
        metadata: dict[str, str] | None = None,
    ):
        pass
