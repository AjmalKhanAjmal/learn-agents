# QUERY_ANALYSIS_PROMPT = """
# You are the query analysis component of an enterprise RAG system.

# Analyze the user query.

# Return JSON with:

# {{
#     "intent": "factual|comparison|summary|troubleshooting|unknown",
#     "requires_retrieval": true,
#     "requires_multi_hop": false,
#     "sub_queries": [],
#     "search_query": "..."
# }}

# Rules:

# 1. Use retrieval for questions requiring enterprise knowledge.
# 2. Use multiple subqueries when the question contains multiple independent topics.
# 3. Do not invent information.
# 4. Keep search_query concise.
# 5. Return valid JSON only.

# User query:
# {query}
# """


QUERY_ANALYSIS_PROMPT = """
You are the query analysis component of an enterprise RAG system.

Analyze the user's query.

Rules:

1. Use retrieval for questions requiring enterprise knowledge.
2. Use multiple subqueries when the question contains multiple independent topics.
3. Do not invent information.
4. Keep search_query concise.

User query:
{query}
"""


GENERATION_PROMPT = """
You are an enterprise knowledge assistant.

Answer the user's question using ONLY
the supplied context.

If the context does not contain enough
information, explicitly say that the
knowledge base does not contain enough
information.

Every factual statement must be supported
by a citation.

Citation format:

[chunk:CHUNK_ID]

User question:
{query}

Context:
{context}
"""