import React, { useEffect, useRef } from 'react';
import UserMessage from './UserMessage';
import AssistantMessage from './AssistantMessage';
import WelcomeScreen from './WelcomeScreen';
import { Database, Loader2, Sparkles } from 'lucide-react';

export default function MessageList({
  messages,
  isLoading,
  currentStep,
  onSelectPrompt,
  onRegenerate,
}) {
  const bottomRef = useRef(null);

  // Auto-scroll to the latest message or loading indicator
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading, currentStep]);

  if (!messages || messages.length === 0) {
    return <WelcomeScreen onSelectPrompt={onSelectPrompt} />;
  }

  return (
    <div className="flex-1 overflow-y-auto px-4 py-6 sm:px-8">
      <div className="max-w-4xl mx-auto">
        {messages.map((message, index) => {
          const isLatest = index === messages.length - 1;
          if (message.role === 'user') {
            return <UserMessage key={message.id || index} message={message} />;
          }
          return (
            <AssistantMessage
              key={message.id || index}
              message={message}
              isLatest={isLatest}
              isLoading={isLoading}
              onRegenerate={onRegenerate}
            />
          );
        })}

        {/* Loading Indicator with Multi-step Pipeline feedback */}
        {isLoading && (
          <div className="flex items-start space-x-3 mb-6 animate-fadeIn">
            <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-slate-900 text-white flex items-center justify-center shadow-xs">
              <Database className="w-4 h-4 text-brand-400" />
            </div>

            <div className="flex-1 max-w-xl">
              <div className="bg-white border border-slate-200 rounded-2xl rounded-tl-xs p-4 shadow-xs">
                <div className="flex items-center space-x-3 mb-2">
                  <Loader2 className="w-4 h-4 text-brand-600 animate-spin" />
                  <span className="text-xs font-semibold text-slate-800">
                    Running LangGraph RAG Pipeline
                  </span>
                </div>

                <div className="flex items-center space-x-2 text-xs text-slate-500">
                  <div className="flex space-x-1">
                    <span className="w-1.5 h-1.5 rounded-full bg-brand-500 animate-bounce" style={{ animationDelay: '0ms' }}></span>
                    <span className="w-1.5 h-1.5 rounded-full bg-brand-500 animate-bounce" style={{ animationDelay: '150ms' }}></span>
                    <span className="w-1.5 h-1.5 rounded-full bg-brand-500 animate-bounce" style={{ animationDelay: '300ms' }}></span>
                  </div>
                  <span className="text-slate-600 font-mono text-[11px]">
                    {currentStep || 'Processing query...'}
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>
    </div>
  );
}
