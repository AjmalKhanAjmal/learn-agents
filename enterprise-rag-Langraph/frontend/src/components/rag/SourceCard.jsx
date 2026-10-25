import React, { useState } from 'react';
import {
  FileText,
  ChevronDown,
  ChevronUp,
  ExternalLink,
  Copy,
  Check,
  Layers,
  Sparkles,
} from 'lucide-react';
import { getFilenameFromPath, formatScore } from '../../utils/helpers';

export default function SourceCard({ sources, activeChunkId, onSelectChunk }) {
  const [expandedIndex, setExpandedIndex] = useState(null);
  const [copiedId, setCopiedId] = useState(null);

  if (!sources || sources.length === 0) {
    return (
      <div className="mt-3 p-3 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-500 flex items-center space-x-2">
        <Layers className="w-4 h-4 text-slate-400 flex-shrink-0" />
        <span>No specific source documents retrieved for this response.</span>
      </div>
    );
  }

  const toggleExpand = (index) => {
    setExpandedIndex(expandedIndex === index ? null : index);
  };

  const copySnippet = (e, text, id) => {
    e.stopPropagation();
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 1500);
  };

  return (
    <div className="mt-4 pt-3 border-t border-slate-100">
      <div className="flex items-center justify-between mb-2.5">
        <div className="flex items-center space-x-1.5">
          <Layers className="w-4 h-4 text-brand-600" />
          <h4 className="text-xs font-semibold text-slate-800 uppercase tracking-wider">
            Evidence Sources ({sources.length})
          </h4>
        </div>
        <span className="text-[11px] text-slate-400">Hybrid BM25 + Vector Search</span>
      </div>

      <div className="grid grid-cols-1 gap-2">
        {sources.map((item, index) => {
          // Normalize source object structure
          const chunkId = item.chunk_id || item.metadata?.chunk_id || `chunk_${index}`;
          const content = item.content || item.page_content || '';
          const meta = item.meta_data || item.metadata || {};
          const sourcePath = meta.source || meta.path || 'Document';
          const filename = getFilenameFromPath(sourcePath);
          const pageNum = meta.page_number || meta.page;
          const rerankScore = item.rerank_score;
          const retrievalScore = item.retrieval_score || item.score;
          const isExpanded = expandedIndex === index;
          const isHighlight = activeChunkId && activeChunkId === chunkId;

          return (
            <div
              key={chunkId || index}
              className={`border rounded-lg transition-all duration-200 overflow-hidden bg-white ${
                isHighlight
                  ? 'border-brand-500 ring-2 ring-brand-100'
                  : 'border-slate-200 hover:border-slate-300'
              }`}
            >
              {/* Source Header */}
              <div
                onClick={() => toggleExpand(index)}
                className="flex items-center justify-between p-3 cursor-pointer select-none hover:bg-slate-50/70"
              >
                <div className="flex items-center space-x-2.5 min-w-0">
                  <div className="p-1.5 rounded bg-brand-50 text-brand-700 flex-shrink-0">
                    <FileText className="w-3.5 h-3.5" />
                  </div>

                  <div className="min-w-0">
                    <div className="flex items-center space-x-2">
                      <span className="text-xs font-semibold text-slate-800 truncate">
                        {filename}
                      </span>
                      {pageNum !== undefined && (
                        <span className="text-[10px] bg-slate-100 text-slate-600 px-1.5 py-0.2 rounded">
                          p. {pageNum}
                        </span>
                      )}
                    </div>
                    <p className="text-[10px] font-mono text-slate-400 truncate">
                      {chunkId}
                    </p>
                  </div>
                </div>

                <div className="flex items-center space-x-3 flex-shrink-0">
                  {/* Scores */}
                  <div className="flex items-center space-x-1.5 text-[11px]">
                    {rerankScore !== undefined && rerankScore !== null && (
                      <span
                        className="bg-emerald-50 text-emerald-700 border border-emerald-200 px-1.5 py-0.5 rounded font-medium text-[10px]"
                        title="Rerank Cross-Encoder Score"
                      >
                        Rerank: {formatScore(rerankScore)}
                      </span>
                    )}
                    {retrievalScore !== undefined && retrievalScore !== null && (
                      <span
                        className="bg-slate-100 text-slate-600 border border-slate-200 px-1.5 py-0.5 rounded text-[10px]"
                        title="Initial Retrieval Score"
                      >
                        Retr: {formatScore(retrievalScore)}
                      </span>
                    )}
                  </div>

                  <button
                    type="button"
                    className="p-1 text-slate-400 hover:text-slate-600 rounded"
                    title={isExpanded ? 'Collapse' : 'Expand snippet'}
                  >
                    {isExpanded ? (
                      <ChevronUp className="w-4 h-4" />
                    ) : (
                      <ChevronDown className="w-4 h-4" />
                    )}
                  </button>
                </div>
              </div>

              {/* Expanded Snippet Content */}
              {isExpanded && (
                <div className="p-3 bg-slate-50/70 border-t border-slate-100 text-xs text-slate-700 leading-relaxed font-sans">
                  <div className="flex justify-between items-center mb-1.5 pb-1 border-b border-slate-200/60">
                    <span className="text-[10px] font-semibold uppercase tracking-wider text-slate-400">
                      Extracted Passage
                    </span>
                    <button
                      onClick={(e) => copySnippet(e, content, chunkId)}
                      className="flex items-center space-x-1 text-[11px] text-slate-500 hover:text-slate-800 transition-colors"
                      title="Copy snippet"
                    >
                      {copiedId === chunkId ? (
                        <>
                          <Check className="w-3 h-3 text-emerald-600" />
                          <span className="text-emerald-600 font-medium">Copied</span>
                        </>
                      ) : (
                        <>
                          <Copy className="w-3 h-3" />
                          <span>Copy</span>
                        </>
                      )}
                    </button>
                  </div>
                  <p className="whitespace-pre-wrap font-sans text-slate-600 select-text">
                    {content}
                  </p>
                  {meta && Object.keys(meta).length > 0 && (
                    <div className="mt-2 pt-2 border-t border-slate-200/50 flex flex-wrap gap-2 text-[10px] text-slate-400 font-mono">
                      {Object.entries(meta).map(([k, v]) => {
                        if (typeof v === 'object' || v === null) return null;
                        return (
                          <span key={k} className="bg-white px-1.5 py-0.5 rounded border border-slate-200">
                            {k}: {String(v)}
                          </span>
                        );
                      })}
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
