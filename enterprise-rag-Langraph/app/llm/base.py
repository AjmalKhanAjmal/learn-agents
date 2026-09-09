from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from typing import Any

class LLMProvider(ABC):
    @abstractmethod
    async def generate(self,
        system_prompt: str,
        user_prompt: str,
        max_output_tokens: int,
        temperature: float | None = None,
        metadata: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """
        Generate a complete response from the LLM.
        """
        raise NotImplementedError
        
    @abstractmethod
    async def stream(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        max_output_tokens: int,
        temperature: float | None = None,
        metadata: dict[str, str] | None = None,
    ) -> AsyncIterator[str]:
        """
        Stream the LLM response.
        """
        raise NotImplementedError