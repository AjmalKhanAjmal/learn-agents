"""
Generation service — wraps Anthropic Claude for grounded, cited answers.

Design constraints
------------------
* The LLM is ONLY allowed to answer from the provided context.
* Every factual claim must be cited with [SOURCE: chunk_id].
* If the context does not contain enough information, the model
  must say so rather than hallucinate.
"""
from __future__ import annotations

import re
import time
from typing import Any

import anthropic
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.core.config import (
    PINECONE_API_KEY,
    PINECONE_INDEX
)
from app.core.exceptions import GenerationError, LLMRateLimitError
from app.core.logging import get_logger
from app.models.schemas import AnswerResponse, Citation, RetrievedChunk

logger = get_logger(__name__)

# ── Prompts ────────────────────────────────────────────────────────────────────

_SYSTEM_PROMPT = """\
You are an expert enterprise document assistant with strict grounding rules.

## Your rules — follow them without exception:

1. **Context-only answers**: Answer SOLELY from the PROVIDED CONTEXT below.
   Never use outside knowledge, training data, or assumptions.

2. **Mandatory citations**: Every factual sentence MUST end with a citation tag
   in the exact format: [SOURCE: <chunk_id>]
   Example: "The refund policy allows 30 days. [SOURCE: a3f9c12b]"

3. **No-answer protocol**: If the context does not contain sufficient information
   to answer the question, respond with:
   "I could not find enough information in the provided documents to answer this question."
   Do NOT fabricate or infer.

4. **Citation integrity**: Only cite chunk IDs that appear in the context.
   Never invent chunk IDs.

5. **Completeness**: Use all relevant context passages. Synthesise across
   multiple chunks when appropriate, citing each one used.

6. **Format**: Respond in clear, professional prose. Use bullet points or
   numbered lists only when the content genuinely warrants it.
"""

_CONTEXT_TEMPLATE = """\
## Retrieved Context

{context_blocks}

---
## Question

{question}

## Answer (cite every fact with [SOURCE: chunk_id]):
"""


def _build_context_blocks(chunks: list[RetrievedChunk]) -> str:
    blocks = []
    for chunk in chunks:
        blocks.append(
            f"[chunk_id: {chunk.chunk_id}]\n"
            f"[source: {chunk.filename}]\n"
            f"[relevance: {chunk.score:.4f}]\n"
            f"{chunk.text}"
        )
    return "\n\n---\n\n".join(blocks)


# ── Citation parsing ───────────────────────────────────────────────────────────

_CITATION_RE = re.compile(r"\[SOURCE:\s*([a-zA-Z0-9_\-]+)\]")


def _extract_citations(
    answer_text: str,
    chunks: list[RetrievedChunk],
) -> list[Citation]:
    """
    Parse [SOURCE: chunk_id] tags from the generated answer and build
    Citation objects with the matching excerpt and relevance score.
    """
    chunk_map = {c.chunk_id: c for c in chunks}
    seen: set[str] = set()
    citations: list[Citation] = []

    for match in _CITATION_RE.finditer(answer_text):
        cid = match.group(1).strip()
        if cid in seen or cid not in chunk_map:
            continue
        seen.add(cid)
        chunk = chunk_map[cid]
        # Use first 200 chars of the chunk as an excerpt
        excerpt = chunk.text[:200].rstrip() + ("…" if len(chunk.text) > 200 else "")
        citations.append(
            Citation(
                source_document=chunk.filename,
                chunk_id=cid,
                excerpt=excerpt,
                relevance_score=chunk.score,
            )
        )

    return sorted(citations, key=lambda c: c.relevance_score, reverse=True)


# ── Generation service ─────────────────────────────────────────────────────────

class GenerationService:
    """
    Grounded answer generation using Anthropic Claude.

    Parameters
    ----------
    model       : Claude model string (e.g. 'claude-3-5-sonnet-20241022')
    max_tokens  : Maximum tokens in the generated answer
    temperature : Sampling temperature (low = more deterministic)
    """

    def __init__(
        self,
        model: str | None = None,
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> None:
        self.model = model or settings.llm_model
        self.max_tokens = max_tokens or settings.llm_max_tokens
        self.temperature = temperature if temperature is not None else settings.llm_temperature
        self._client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    # ── Public ─────────────────────────────────────────────────────────────────

    @retry(
        retry=retry_if_exception_type(LLMRateLimitError),
        stop=stop_after_attempt(4),
        wait=wait_exponential(multiplier=2, min=5, max=60),
        reraise=True,
    )
    def generate(
        self,
        question: str,
        chunks: list[RetrievedChunk],
        extra_instructions: str = "",
    ) -> dict[str, Any]:
        """
        Generate a grounded, cited answer from retrieved chunks.

        Returns
        -------
        dict with keys: answer, citations, input_tokens, output_tokens
        """
        if not chunks:
            return {
                "answer": (
                    "I could not find any relevant documents to answer your question. "
                    "Please ensure documents have been uploaded and indexed."
                ),
                "citations": [],
                "input_tokens": 0,
                "output_tokens": 0,
            }

        context_blocks = _build_context_blocks(chunks)
        user_content = _CONTEXT_TEMPLATE.format(
            context_blocks=context_blocks,
            question=question,
        )
        if extra_instructions:
            user_content += f"\n\n## Additional Instructions\n{extra_instructions}"

        t0 = time.monotonic()
        try:
            response = self._client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=_SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_content}],
            )
        except anthropic.RateLimitError as exc:
            raise LLMRateLimitError(f"Anthropic rate limit: {exc}") from exc
        except anthropic.APIError as exc:
            raise GenerationError(f"Anthropic API error: {exc}") from exc

        elapsed_ms = (time.monotonic() - t0) * 1000
        answer_text = response.content[0].text

        citations = _extract_citations(answer_text, chunks)

        logger.info(
            "generation_complete",
            model=self.model,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            citations_found=len(citations),
            elapsed_ms=round(elapsed_ms, 1),
        )

        return {
            "answer": answer_text,
            "citations": citations,
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
            "generation_duration_ms": round(elapsed_ms, 1),
        }

    def health_check(self) -> dict[str, Any]:
        """Lightweight probe — sends a minimal message to verify credentials."""
        t0 = time.monotonic()
        try:
            self._client.messages.create(
                model=self.model,
                max_tokens=5,
                messages=[{"role": "user", "content": "ping"}],
            )
            return {"status": "ok", "latency_ms": round((time.monotonic() - t0) * 1000, 2)}
        except Exception as exc:
            return {"status": "error", "error": str(exc)}