from pydantic import BaseModel, Field

from langchain_core.messages import HumanMessage

from app.generation.service import LLMService
from app.agents.prompts import QUERY_ANALYSIS_PROMPT


class QueryAnalysis(BaseModel):

    intent: str

    requires_retrieval: bool

    requires_multi_hop: bool

    sub_queries: list[str] = Field(default_factory=list)

    search_query: str


class QueryAnalyzer:

    def __init__(self):

        self.llm = LLMService()

        self.model = self.llm.structured(
            QueryAnalysis
        )

    def analyze(self, query: str) -> QueryAnalysis:

        prompt = QUERY_ANALYSIS_PROMPT.format(
            query=query
        )

        return self.model.invoke(
            [
                HumanMessage(content=prompt)
            ]
        )