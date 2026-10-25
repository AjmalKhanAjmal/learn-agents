import React from 'react';
import { Menu, Trash2, Upload, Sparkles, Layers } from 'lucide-react';

export default function ChatHeader({
  title,
  onToggleMobileSidebar,
  onClearChat,
  onOpenUploadModal,
  hasMessages,
}) {
  return (
    <header className="h-14 border-b border-slate-200 bg-white/95 backdrop-blur px-4 flex items-center justify-between z-10">
      <div className="flex items-center space-x-3 min-w-0">
        <button
          onClick={onToggleMobileSidebar}
          className="md:hidden p-1.5 text-slate-500 hover:text-slate-800 hover:bg-slate-100 rounded-lg transition-colors"
          title="Toggle menu"
        >
          <Menu className="w-5 h-5" />
        </button>

        <div className="flex items-center space-x-2 min-w-0">
          <h1 className="font-semibold text-slate-800 text-sm truncate max-w-[220px] sm:max-w-md">
            {title || 'New Conversation'}
          </h1>
          <span className="hidden sm:inline-flex items-center space-x-1 text-[11px] font-medium bg-slate-100 text-slate-600 px-2 py-0.5 rounded-full border border-slate-200">
            <Layers className="w-3 h-3 text-brand-600" />
            <span>Hybrid RAG</span>
          </span>
        </div>
      </div>

      <div className="flex items-center space-x-2">
        <button
          onClick={onOpenUploadModal}
          className="flex items-center space-x-1.5 text-xs font-medium text-slate-600 hover:text-brand-700 hover:bg-brand-50 px-2.5 py-1.5 rounded-lg border border-slate-200 transition-colors"
          title="Upload new document to knowledge base"
        >
          <Upload className="w-3.5 h-3.5 text-brand-600" />
          <span className="hidden sm:inline">Upload Document</span>
        </button>

        {hasMessages && (
          <button
            onClick={onClearChat}
            className="p-1.5 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
            title="Clear current messages"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        )}
      </div>
    </header>
  );
}
