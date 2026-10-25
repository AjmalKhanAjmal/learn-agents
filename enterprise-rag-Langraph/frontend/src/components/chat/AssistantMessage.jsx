import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import {
  Database,
  Copy,
  Check,
  RefreshCw,
  AlertCircle,
  FileText,
  Clock,
} from 'lucide-react';
import SourceCard from '../rag/SourceCard';
import EvidenceBadge from '../rag/EvidenceBadge';
import PipelineTrace from '../rag/PipelineTrace';
import { formatTimestamp } from '../../utils/helpers';

export default function AssistantMessage({
  message,
  onRegenerate,
  isLatest,
  isLoading,
}) {
  const [copied, setCopied] = useState(false);
  const [activeCitationChunk, setActiveCitationChunk] = useState(null);

  const handleCopy = () => {
    if (!message.content) return;
    navigator.clipboard.writeText(message.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const isError = message.isError;

  return (
    <div className="flex items-start space-x-3 mb-6 group">
      {/* Assistant Avatar */}
      <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-slate-900 text-white flex items-center justify-center shadow-xs">
        <Database className="w-4 h-4 text-brand-400" />
      </div>

      {/* Main Content Area */}
      <div className="flex-1 min-w-0 max-w-3xl">
        <div className="bg-white border border-slate-200/90 rounded-2xl rounded-tl-xs p-4 sm:p-5 shadow-xs">
          {/* Error Message Display */}
          {isError ? (
            <div className="flex items-start space-x-2.5 text-red-700 bg-red-50 p-3 rounded-lg border border-red-200">
              <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5 text-red-600" />
              <div className="text-xs sm:text-sm leading-relaxed">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {message.content}
                </ReactMarkdown>
              </div>
            </div>
          ) : (
            <>
              {/* Markdown Rendered Answer */}
              <div className="markdown-body">
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  components={{
                    // Style code blocks with copy capability
                    code({ node, inline, className, children, ...props }) {
                      const match = /language-(\w+)/.exec(className || '');
                      return !inline ? (
                        <div className="relative group/code my-2 rounded-lg overflow-hidden border border-slate-800">
                          {match && (
                            <div className="bg-slate-800 text-slate-300 text-[10px] px-3 py-1 font-mono uppercase tracking-wider">
                              {match[1]}
                            </div>
                          )}
                          <pre className="!m-0 !rounded-none">
                            <code className={className} {...props}>
                              {children}
                            </code>
                          </pre>
                        </div>
                      ) : (
                        <code className={className} {...props}>
                          {children}
                        </code>
                      );
                    },
                  }}
                >
                  {message.content}
                </ReactMarkdown>
              </div>

              {/* Evidence & Grounding Confidence Badges */}
              <EvidenceBadge
                evidenceScore={message.evidenceScore}
                evidenceSufficient={message.evidenceSufficient}
                grounded={message.grounded}
                groundingScore={message.groundingScore}
              />

              {/* RAG Source Documents */}
              <SourceCard
                sources={message.sources}
                activeChunkId={activeCitationChunk}
                onSelectChunk={setActiveCitationChunk}
              />

              {/* Technical LangGraph Execution Trace */}
              <PipelineTrace
                queryAnalysis={message.queryAnalysis}
                evidenceReason={message.evidenceReason}
                validationReason={message.validationReason}
              />
            </>
          )}

          {/* Action Toolbar */}
          <div className="mt-3 pt-2 flex items-center justify-between border-t border-slate-100 text-[11px] text-slate-400">
            <div className="flex items-center space-x-1">
              <Clock className="w-3 h-3" />
              <span>{formatTimestamp(message.timestamp)}</span>
            </div>

            <div className="flex items-center space-x-1">
              {!isError && (
                <button
                  onClick={handleCopy}
                  className="flex items-center space-x-1 px-2 py-1 rounded text-slate-500 hover:text-slate-800 hover:bg-slate-100 transition-colors"
                  title="Copy response to clipboard"
                >
                  {copied ? (
                    <>
                      <Check className="w-3.5 h-3.5 text-emerald-600" />
                      <span className="text-emerald-600 font-medium">Copied</span>
                    </>
                  ) : (
                    <>
                      <Copy className="w-3.5 h-3.5" />
                      <span>Copy</span>
                    </>
                  )}
                </button>
              )}

              {onRegenerate && isLatest && !isLoading && (
                <button
                  onClick={() => onRegenerate(message.id)}
                  className="flex items-center space-x-1 px-2 py-1 rounded text-slate-500 hover:text-brand-600 hover:bg-brand-50 transition-colors"
                  title="Regenerate answer"
                >
                  <RefreshCw className="w-3.5 h-3.5" />
                  <span>Regenerate</span>
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
