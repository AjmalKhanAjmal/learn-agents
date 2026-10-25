import { useState, useEffect, useRef, useCallback } from 'react';
import { api } from '../api/client';
import { generateId } from '../utils/helpers';

const STORAGE_KEY = 'enterprise_rag_conversations_v1';
const ACTIVE_CONV_KEY = 'enterprise_rag_active_conv_v1';

export function useChat() {
  const [conversations, setConversations] = useState(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        return JSON.parse(stored);
      }
    } catch (e) {
      console.error('Failed to load conversations from localStorage', e);
    }
    const defaultConvId = generateId('conv');
    return [
      {
        id: defaultConvId,
        title: 'New Conversation',
        createdAt: new Date().toISOString(),
        messages: [],
      },
    ];
  });

  const [activeId, setActiveId] = useState(() => {
    try {
      const stored = localStorage.getItem(ACTIVE_CONV_KEY);
      if (stored) return stored;
    } catch {}
    return conversations[0]?.id || 'default';
  });

  const [isLoading, setIsLoading] = useState(false);
  const [currentStep, setCurrentStep] = useState('');
  const [error, setError] = useState(null);

  const abortControllerRef = useRef(null);

  // Sync conversations to localStorage
  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(conversations));
    } catch (e) {
      console.error('Failed to persist conversations', e);
    }
  }, [conversations]);

  // Sync active conversation
  useEffect(() => {
    try {
      localStorage.setItem(ACTIVE_CONV_KEY, activeId);
    } catch {}
  }, [activeId]);

  const activeConversation = conversations.find((c) => c.id === activeId) || conversations[0];

  /**
   * Start a brand new conversation
   */
  const createNewChat = useCallback(() => {
    const newId = generateId('conv');
    const newConv = {
      id: newId,
      title: 'New Conversation',
      createdAt: new Date().toISOString(),
      messages: [],
    };
    setConversations((prev) => [newConv, ...prev]);
    setActiveId(newId);
    setError(null);
  }, []);

  /**
   * Delete a conversation
   */
  const deleteConversation = useCallback(
    (id) => {
      setConversations((prev) => {
        const filtered = prev.filter((c) => c.id !== id);
        if (filtered.length === 0) {
          const freshId = generateId('conv');
          const fresh = {
            id: freshId,
            title: 'New Conversation',
            createdAt: new Date().toISOString(),
            messages: [],
          };
          setActiveId(freshId);
          return [fresh];
        }
        if (activeId === id) {
          setActiveId(filtered[0].id);
        }
        return filtered;
      });
    },
    [activeId]
  );

  /**
   * Clear all messages in current conversation
   */
  const clearCurrentChat = useCallback(() => {
    if (!activeId) return;
    setConversations((prev) =>
      prev.map((c) => (c.id === activeId ? { ...c, messages: [], title: 'New Conversation' } : c))
    );
    setError(null);
  }, [activeId]);

  /**
   * Send a query through the LangGraph RAG pipeline
   */
  const sendMessage = useCallback(
    async (queryText) => {
      const trimmed = queryText?.trim();
      if (!trimmed || isLoading) return;

      setError(null);
      setIsLoading(true);
      setCurrentStep('Analyzing query intent...');

      const userMessageId = generateId('msg_user');
      const assistantMessageId = generateId('msg_ai');

      const userMessage = {
        id: userMessageId,
        role: 'user',
        content: trimmed,
        timestamp: new Date().toISOString(),
      };

      // Add user message immediately
      setConversations((prev) =>
        prev.map((c) => {
          if (c.id === activeId) {
            const isFirst = c.messages.length === 0;
            const newTitle = isFirst
              ? trimmed.length > 35
                ? `${trimmed.substring(0, 32)}...`
                : trimmed
              : c.title;

            return {
              ...c,
              title: newTitle,
              messages: [...c.messages, userMessage],
            };
          }
          return c;
        })
      );

      // Simulation steps for RAG pipeline feedback
      const stepTimer1 = setTimeout(() => setCurrentStep('Executing hybrid BM25 & vector retrieval...'), 1200);
      const stepTimer2 = setTimeout(() => setCurrentStep('Reranking evidence documents...'), 3000);
      const stepTimer3 = setTimeout(() => setCurrentStep('Synthesizing grounded response...'), 5500);

      const controller = new AbortController();
      abortControllerRef.current = controller;

      try {
        const response = await api.sendGraphChat(trimmed, controller.signal);

        clearTimeout(stepTimer1);
        clearTimeout(stepTimer2);
        clearTimeout(stepTimer3);

        const assistantMessage = {
          id: assistantMessageId,
          role: 'assistant',
          content: response.answer || 'No answer generated.',
          timestamp: new Date().toISOString(),
          // RAG Specific Data directly from AgentState
          sources: response.reranked_results || response.fused_results || [],
          evidenceScore: response.evidence_score,
          evidenceReason: response.evidence_reason,
          evidenceSufficient: response.evidence_sufficient,
          grounded: response.grounded,
          groundingScore: response.grounding_score,
          validationReason: response.validation_reason,
          queryAnalysis: {
            intent: response.intent,
            rewrittenQuery: response.rewritten_query,
            subQueries: response.sub_queries,
            requiresRetrieval: response.requires_retrieval,
          },
        };

        setConversations((prev) =>
          prev.map((c) =>
            c.id === activeId
              ? {
                  ...c,
                  messages: [...c.messages, assistantMessage],
                }
              : c
          )
        );
      } catch (err) {
        clearTimeout(stepTimer1);
        clearTimeout(stepTimer2);
        clearTimeout(stepTimer3);

        if (err.name === 'AbortError') {
          // Stopped by user
          return;
        }

        console.error('Failed to get answer from RAG graph:', err);
        const errorMessage = {
          id: assistantMessageId,
          role: 'assistant',
          content: `**Error:** ${err.message}`,
          isError: true,
          timestamp: new Date().toISOString(),
        };

        setConversations((prev) =>
          prev.map((c) =>
            c.id === activeId
              ? {
                  ...c,
                  messages: [...c.messages, errorMessage],
                }
              : c
          )
        );
        setError(err.message);
      } finally {
        setIsLoading(false);
        setCurrentStep('');
        abortControllerRef.current = null;
      }
    },
    [activeId, isLoading]
  );

  /**
   * Stop generation / abort ongoing request
   */
  const stopGeneration = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
      setIsLoading(false);
      setCurrentStep('');
    }
  }, []);

  /**
   * Regenerate the last assistant response
   */
  const regenerateAnswer = useCallback(
    async (messageId) => {
      if (isLoading || !activeConversation) return;

      const msgs = activeConversation.messages;
      const targetIndex = msgs.findIndex((m) => m.id === messageId);
      if (targetIndex <= 0) return;

      // Find the corresponding user prompt (previous user message)
      const userMsg = msgs
        .slice(0, targetIndex)
        .reverse()
        .find((m) => m.role === 'user');

      if (!userMsg) return;

      // Remove the targeted assistant message and any subsequent messages
      setConversations((prev) =>
        prev.map((c) =>
          c.id === activeId
            ? {
                ...c,
                messages: c.messages.filter((m) => m.id !== messageId),
              }
            : c
        )
      );

      // Re-invoke with userMsg content
      await sendMessage(userMsg.content);
    },
    [isLoading, activeConversation, activeId, sendMessage]
  );

  return {
    conversations,
    activeId,
    setActiveId,
    activeConversation,
    isLoading,
    currentStep,
    error,
    sendMessage,
    stopGeneration,
    createNewChat,
    deleteConversation,
    clearCurrentChat,
    regenerateAnswer,
  };
}
