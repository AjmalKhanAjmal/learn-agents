import React from 'react';
import { ShieldCheck, AlertTriangle, CheckCircle2, XCircle } from 'lucide-react';
import { formatScore } from '../../utils/helpers';

export default function EvidenceBadge({
  evidenceScore,
  evidenceSufficient,
  grounded,
  groundingScore,
}) {
  const hasEvidence = evidenceScore !== undefined && evidenceScore !== null;
  const hasGrounding = grounded !== undefined && grounded !== null;

  if (!hasEvidence && !hasGrounding) return null;

  return (
    <div className="flex flex-wrap items-center gap-2 my-2.5">
      {/* Evidence Score Pill */}
      {hasEvidence && (
        <div
          className={`inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-md text-xs font-medium border ${
            evidenceSufficient
              ? 'bg-emerald-50 text-emerald-800 border-emerald-200'
              : 'bg-amber-50 text-amber-800 border-amber-200'
          }`}
          title={`Evidence Score: ${(evidenceScore * 100).toFixed(1)}%`}
        >
          {evidenceSufficient ? (
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
          ) : (
            <AlertTriangle className="w-3.5 h-3.5 text-amber-600" />
          )}
          <span>Evidence Score: {formatScore(evidenceScore)}</span>
          <span className="text-[10px] text-slate-500 font-normal">
            ({evidenceSufficient ? 'Sufficient' : 'Low Confidence'})
          </span>
        </div>
      )}

      {/* Grounding Verification Pill */}
      {hasGrounding && (
        <div
          className={`inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-md text-xs font-medium border ${
            grounded
              ? 'bg-blue-50 text-blue-800 border-blue-200'
              : 'bg-slate-100 text-slate-700 border-slate-200'
          }`}
          title={`Grounding Score: ${groundingScore !== undefined ? formatScore(groundingScore) : 'N/A'}`}
        >
          <ShieldCheck className={`w-3.5 h-3.5 ${grounded ? 'text-blue-600' : 'text-slate-500'}`} />
          <span>Citation Grounding: {grounded ? 'Verified' : 'Unverified'}</span>
          {groundingScore !== undefined && groundingScore !== null && (
            <span className="text-[10px] font-mono text-slate-500">
              ({formatScore(groundingScore)})
            </span>
          )}
        </div>
      )}
    </div>
  );
}
