/**
 * Enterprise RAG API Client
 * Connects directly to the FastAPI backend endpoints
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

class ApiError extends Error {
  constructor(message, status = 500, details = null) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.details = details;
  }
}

/**
 * Perform a fetch request with timeout and standardized error handling
 */
async function request(endpoint, options = {}, timeoutMs = 60000) {
  const url = `${API_BASE_URL}${endpoint}`;
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(url, {
      ...options,
      signal: options.signal || controller.signal,
    });
    clearTimeout(id);

    if (!response.ok) {
      let errorMessage = `HTTP Error ${response.status}: ${response.statusText}`;
      let errorDetails = null;
      try {
        const errorJson = await response.json();
        errorMessage = errorJson.detail || errorJson.message || errorMessage;
        errorDetails = errorJson;
      } catch {
        // Fallback to text or status
      }
      throw new ApiError(errorMessage, response.status, errorDetails);
    }

    return await response.json();
  } catch (err) {
    clearTimeout(id);
    if (err.name === 'AbortError') {
      throw new ApiError('Request timed out. The RAG pipeline took too long to respond.', 408);
    }
    if (err instanceof ApiError) {
      throw err;
    }
    throw new ApiError(
      `Unable to reach backend at ${API_BASE_URL}. Ensure FastAPI is running and CORS is enabled. (${err.message})`,
      0
    );
  }
}

export const api = {
  getBaseUrl() {
    return API_BASE_URL;
  },

  /**
   * Health check
   */
  async checkHealth() {
    return await request('/health', { method: 'GET' }, 5000);
  },

  /**
   * LangGraph Chat endpoint
   * POST /chat/graph
   * Payload: { "query": string }
   * Returns: Full AgentState object (answer, reranked_results, evidence_score, etc.)
   */
  async sendGraphChat(query, signal = null) {
    return await request(
      '/chat/graph',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
        signal,
      },
      90000 // 90 seconds timeout for multi-step agent flow
    );
  },

  /**
   * Upload Document endpoint
   * POST /documents/upload
   * Payload: FormData with 'file'
   */
  async uploadDocument(file, signal = null) {
    const formData = new FormData();
    formData.append('file', file);

    return await request(
      '/documents/upload',
      {
        method: 'POST',
        body: formData,
        signal,
      },
      120000 // 2 minutes for large PDF extraction & indexing
    );
  },

  /**
   * Hybrid retrieval search
   * POST /retrieval/hybrid_retrieval
   */
  async searchHybrid(query, topK = 5) {
    return await request('/retrieval/hybrid_retrieval', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, top_k: topK }),
    });
  },

  /**
   * Direct vector search
   * POST /retrieval/search
   */
  async searchVector(query, topK = 3, scoreThreshold = 0.5) {
    return await request('/retrieval/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query,
        top_k: topK,
        score_threshold: scoreThreshold,
      }),
    });
  },
};
