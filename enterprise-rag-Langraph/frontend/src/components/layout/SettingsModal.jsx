import React, { useState, useEffect } from 'react';
import {
  Settings,
  X,
  Server,
  Layers,
  CheckCircle2,
  AlertCircle,
  Database,
  Trash2,
  RefreshCw,
  Cpu,
} from 'lucide-react';
import { api } from '../../api/client';

export default function SettingsModal({ isOpen, onClose }) {
  const [healthStatus, setHealthStatus] = useState('checking');
  const [isChecking, setIsChecking] = useState(false);
  const baseUrl = api.getBaseUrl();

  const verifyConnection = async () => {
    setIsChecking(true);
    setHealthStatus('checking');
    try {
      const res = await api.checkHealth();
      if (res.status === 'healthy') {
        setHealthStatus('healthy');
      } else {
        setHealthStatus('error');
      }
    } catch {
      setHealthStatus('unreachable');
    } finally {
      setIsChecking(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      verifyConnection();
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-xs p-4 animate-fadeIn">
      <div className="bg-white rounded-2xl shadow-xl border border-slate-200 max-w-md w-full overflow-hidden flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-slate-100">
          <div className="flex items-center space-x-2">
            <div className="p-2 rounded-lg bg-slate-100 text-slate-700">
              <Settings className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-semibold text-slate-900 text-sm">
                System Status & Settings
              </h3>
              <p className="text-xs text-slate-500">Enterprise RAG Pipeline Configuration</p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-lg transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Content */}
        <div className="p-5 space-y-4 text-xs">
          {/* Backend Connection */}
          <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-200 space-y-2">
            <div className="flex items-center justify-between">
              <span className="font-semibold text-slate-700 flex items-center space-x-1.5">
                <Server className="w-4 h-4 text-brand-600" />
                <span>FastAPI Backend</span>
              </span>
              <button
                onClick={verifyConnection}
                disabled={isChecking}
                className="text-[11px] text-brand-600 hover:text-brand-700 font-medium flex items-center space-x-1 disabled:opacity-50"
              >
                <RefreshCw className={`w-3 h-3 ${isChecking ? 'animate-spin' : ''}`} />
                <span>Recheck</span>
              </button>
            </div>

            <div className="flex items-center justify-between pt-1">
              <span className="text-slate-500 font-mono text-[11px]">{baseUrl}</span>
              <div>
                {healthStatus === 'healthy' && (
                  <span className="inline-flex items-center space-x-1 text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-full font-medium text-[10px]">
                    <CheckCircle2 className="w-3 h-3 text-emerald-600" />
                    <span>Healthy (200 OK)</span>
                  </span>
                )}
                {healthStatus === 'unreachable' && (
                  <span className="inline-flex items-center space-x-1 text-red-700 bg-red-50 border border-red-200 px-2 py-0.5 rounded-full font-medium text-[10px]">
                    <AlertCircle className="w-3 h-3 text-red-600" />
                    <span>Unreachable</span>
                  </span>
                )}
                {healthStatus === 'checking' && (
                  <span className="inline-flex items-center space-x-1 text-slate-600 bg-slate-100 px-2 py-0.5 rounded-full text-[10px]">
                    <span>Connecting...</span>
                  </span>
                )}
              </div>
            </div>
          </div>

          {/* Architecture Components */}
          <div className="space-y-2">
            <span className="font-semibold text-slate-800 text-[11px] uppercase tracking-wider">
              Configured RAG Architecture
            </span>

            <div className="grid grid-cols-2 gap-2 text-[11px]">
              <div className="p-2.5 rounded-lg border border-slate-200 bg-white">
                <span className="text-slate-400 block mb-0.5">Vector Search</span>
                <span className="font-semibold text-slate-800">Pinecone Vector DB</span>
              </div>
              <div className="p-2.5 rounded-lg border border-slate-200 bg-white">
                <span className="text-slate-400 block mb-0.5">Keyword Search</span>
                <span className="font-semibold text-slate-800">OpenSearch BM25</span>
              </div>
              <div className="p-2.5 rounded-lg border border-slate-200 bg-white">
                <span className="text-slate-400 block mb-0.5">Agent Framework</span>
                <span className="font-semibold text-slate-800">LangGraph Workflow</span>
              </div>
              <div className="p-2.5 rounded-lg border border-slate-200 bg-white">
                <span className="text-slate-400 block mb-0.5">Reranking Model</span>
                <span className="font-semibold text-slate-800">Cross-Encoder</span>
              </div>
            </div>
          </div>

          {/* Local Storage Management */}
          <div className="pt-2 border-t border-slate-100">
            <button
              onClick={() => {
                if (confirm('Clear local conversation history and uploaded document index cache?')) {
                  localStorage.clear();
                  window.location.reload();
                }
              }}
              className="text-xs text-red-600 hover:text-red-700 flex items-center space-x-1.5 py-1"
            >
              <Trash2 className="w-3.5 h-3.5" />
              <span>Clear Local History & Reset App</span>
            </button>
          </div>
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-slate-100 bg-slate-50 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-lg text-xs font-medium transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
