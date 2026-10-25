import React, { useState } from 'react';
import { GitBranch, ChevronDown, ChevronUp, Terminal, ArrowRight, Check } from 'lucide-react';

export default function PipelineTrace({ queryAnalysis, evidenceReason, validationReason }) {
  const [isOpen, setIsOpen] = useState(false);

  if (!queryAnalysis && !evidenceReason && !validationReason) {
    return null;
  }

  return (
    <div className="mt-3 border border-slate-200/80 rounded-lg overflow-hidden bg-slate-50/50">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between px-3 py-2 text-left hover:bg-slate-100/60 transition-colors select-none"
      >
        <div className="flex items-center space-x-2">
          <GitBranch className="w-3.5 h-3.5 text-slate-500" />
          <span className="text-[11px] font-semibold text-slate-700 tracking-tight">
            LangGraph Execution Trace
          </span>
        </div>
        <div className="flex items-center space-x-1 text-[10px] text-slate-400">
          <span>{isOpen ? 'Hide Trace' : 'View Trace'}</span>
          {isOpen ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
        </div>
      </button>

      {isOpen && (
        <div className="p-3 border-t border-slate-200/70 bg-white space-y-2.5 text-xs">
          {/* Query Analysis */}
          {queryAnalysis && (
            <div className="space-y-1.5">
              <span className="text-[10px] font-semibold uppercase tracking-wider text-slate-400">
                Query Analyzer Agent
              </span>
              <div className="bg-slate-50 rounded-md p-2 border border-slate-100 space-y-1 font-mono text-[11px]">
                {queryAnalysis.intent && (
                  <div className="flex items-start space-x-2">
                    <span className="text-slate-400">Intent:</span>
                    <span className="text-slate-800 font-semibold">{queryAnalysis.intent}</span>
                  </div>
                )}
                {queryAnalysis.rewrittenQuery && (
                  <div className="flex items-start space-x-2">
                    <span className="text-slate-400">Rewritten:</span>
                    <span className="text-slate-700">{queryAnalysis.rewrittenQuery}</span>
                  </div>
                )}
                {queryAnalysis.subQueries && queryAnalysis.subQueries.length > 0 && (
                  <div>
                    <span className="text-slate-400 block mb-0.5">Sub-queries:</span>
                    <ul className="list-disc pl-4 text-slate-600">
                      {queryAnalysis.subQueries.map((sq, i) => (
                        <li key={i}>{sq}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Evidence Reason */}
          {evidenceReason && (
            <div className="space-y-1">
              <span className="text-[10px] font-semibold uppercase tracking-wider text-slate-400">
                Evidence Evaluation
              </span>
              <div className="bg-slate-50 rounded-md p-2 border border-slate-100 text-slate-600 text-xs">
                {evidenceReason}
              </div>
            </div>
          )}

          {/* Validation Reason */}
          {validationReason && (
            <div className="space-y-1">
              <span className="text-[10px] font-semibold uppercase tracking-wider text-slate-400">
                Grounding & Citation Validation
              </span>
              <div className="bg-slate-50 rounded-md p-2 border border-slate-100 text-slate-600 text-xs flex items-center space-x-1.5">
                <Check className="w-3.5 h-3.5 text-emerald-600" />
                <span>{validationReason}</span>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
