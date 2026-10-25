import React, { useState } from 'react';
import {
  Plus,
  MessageSquare,
  Search,
  Trash2,
  FileText,
  UploadCloud,
  Settings,
  ChevronLeft,
  ChevronRight,
  Database,
  ExternalLink,
  ShieldCheck,
} from 'lucide-react';
import { formatDate, formatBytes } from '../../utils/helpers';

export default function Sidebar({
  conversations,
  activeId,
  onSelectConversation,
  onNewChat,
  onDeleteConversation,
  documents,
  onOpenUploadModal,
  onOpenSettings,
  backendConnected,
  isCollapsed,
  onToggleCollapse,
}) {
  const [searchQuery, setSearchQuery] = useState('');

  const filteredConversations = conversations.filter((c) =>
    (c.title || '').toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <aside
      className={`relative flex flex-col bg-white border-r border-slate-200 transition-all duration-300 ease-in-out h-full z-20 ${
        isCollapsed ? 'w-16' : 'w-72 sm:w-80'
      }`}
    >
      {/* Brand Header */}
      <div className="flex items-center justify-between p-4 border-b border-slate-100">
        {!isCollapsed && (
          <div className="flex items-center space-x-2.5 overflow-hidden">
            <div className="flex items-center justify-center w-9 h-9 rounded-lg bg-brand-600 text-white shadow-sm flex-shrink-0">
              <Database className="w-5 h-5" />
            </div>
            <div className="flex flex-col min-w-0">
              <div className="flex items-center space-x-1.5">
                <span className="font-semibold text-slate-900 text-sm tracking-tight truncate">
                  Enterprise RAG
                </span>
                <span className="text-[10px] font-medium bg-brand-50 text-brand-700 px-1.5 py-0.5 rounded border border-brand-200">
                  v1.0
                </span>
              </div>
              <span className="text-xs text-slate-500 truncate">Knowledge Assistant</span>
            </div>
          </div>
        )}

        {isCollapsed && (
          <div className="mx-auto flex items-center justify-center w-9 h-9 rounded-lg bg-brand-600 text-white shadow-sm">
            <Database className="w-5 h-5" />
          </div>
        )}

        <button
          onClick={onToggleCollapse}
          title={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
          className="hidden md:flex p-1.5 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-lg transition-colors"
        >
          {isCollapsed ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
        </button>
      </div>

      {/* Primary Action: New Chat */}
      <div className="p-3">
        <button
          onClick={onNewChat}
          className={`w-full flex items-center justify-center space-x-2 bg-brand-600 hover:bg-brand-700 active:bg-brand-800 text-white font-medium py-2.5 px-3 rounded-lg shadow-sm transition-all focus:outline-none focus:ring-2 focus:ring-brand-500 focus:ring-offset-1 text-sm ${
            isCollapsed ? 'px-0' : ''
          }`}
          title="New Chat"
        >
          <Plus className="w-4 h-4 flex-shrink-0" />
          {!isCollapsed && <span>New Chat</span>}
        </button>
      </div>

      {/* Search Input (visible when expanded) */}
      {!isCollapsed && (
        <div className="px-3 pb-2">
          <div className="relative">
            <Search className="w-4 h-4 absolute left-3 top-2.5 text-slate-400" />
            <input
              type="text"
              placeholder="Search conversations..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-3 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded-md focus:bg-white focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition-all text-slate-800 placeholder-slate-400"
            />
          </div>
        </div>
      )}

      {/* Middle Section: Conversations & Documents */}
      <div className="flex-1 overflow-y-auto px-3 py-2 space-y-4">
        {/* Chat History List */}
        <div>
          {!isCollapsed && (
            <div className="flex items-center justify-between px-2 mb-1.5">
              <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">
                Conversations ({filteredConversations.length})
              </span>
            </div>
          )}

          <div className="space-y-1">
            {filteredConversations.map((conv) => {
              const isActive = conv.id === activeId;
              return (
                <div
                  key={conv.id}
                  onClick={() => onSelectConversation(conv.id)}
                  className={`group relative flex items-center rounded-lg cursor-pointer transition-all ${
                    isCollapsed ? 'justify-center p-2.5' : 'px-3 py-2 space-x-2.5'
                  } ${
                    isActive
                      ? 'bg-brand-50 text-brand-900 font-medium'
                      : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
                  }`}
                  title={conv.title}
                >
                  <MessageSquare
                    className={`w-4 h-4 flex-shrink-0 ${
                      isActive ? 'text-brand-600' : 'text-slate-400 group-hover:text-slate-600'
                    }`}
                  />

                  {!isCollapsed && (
                    <>
                      <div className="flex-1 min-w-0">
                        <p className="text-xs truncate">{conv.title || 'Untitled Chat'}</p>
                        <p className="text-[10px] text-slate-400">
                          {formatDate(conv.createdAt)}
                        </p>
                      </div>

                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          onDeleteConversation(conv.id);
                        }}
                        title="Delete chat"
                        className="opacity-0 group-hover:opacity-100 p-1 text-slate-400 hover:text-red-600 hover:bg-white rounded transition-all"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </>
                  )}
                </div>
              );
            })}

            {filteredConversations.length === 0 && !isCollapsed && (
              <p className="text-xs text-slate-400 px-3 py-2 italic text-center">
                No conversations found
              </p>
            )}
          </div>
        </div>

        {/* Uploaded Documents Knowledge Base Section */}
        <div className="pt-2 border-t border-slate-100">
          {!isCollapsed && (
            <div className="flex items-center justify-between px-2 mb-1.5">
              <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">
                Knowledge Base
              </span>
              <button
                onClick={onOpenUploadModal}
                className="text-[11px] text-brand-600 hover:text-brand-700 font-medium flex items-center space-x-1"
                title="Upload PDF document"
              >
                <Plus className="w-3 h-3" />
                <span>Upload</span>
              </button>
            </div>
          )}

          <div className="space-y-1">
            {documents.slice(0, 5).map((doc) => (
              <div
                key={doc.id}
                className={`flex items-center rounded-lg text-slate-600 hover:bg-slate-50 transition-colors ${
                  isCollapsed ? 'justify-center p-2.5' : 'px-3 py-2 space-x-2.5'
                }`}
                title={`${doc.name} (${doc.chunksCreated || 0} chunks)`}
              >
                <FileText className="w-4 h-4 flex-shrink-0 text-slate-400" />
                {!isCollapsed && (
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-medium text-slate-700 truncate">{doc.name}</p>
                    <div className="flex items-center space-x-1.5 text-[10px] text-slate-400">
                      {doc.chunksCreated && <span>{doc.chunksCreated} chunks</span>}
                      {doc.size && <span>• {formatBytes(doc.size)}</span>}
                    </div>
                  </div>
                )}
              </div>
            ))}

            {documents.length === 0 && !isCollapsed && (
              <div
                onClick={onOpenUploadModal}
                className="border border-dashed border-slate-200 rounded-lg p-3 text-center cursor-pointer hover:border-brand-300 hover:bg-brand-50/30 transition-all group"
              >
                <UploadCloud className="w-5 h-5 mx-auto text-slate-400 group-hover:text-brand-600 mb-1" />
                <p className="text-xs font-medium text-slate-600 group-hover:text-brand-700">
                  Upload PDF
                </p>
                <p className="text-[10px] text-slate-400">Index into BM25 & Pinecone</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Footer: Connection Status & Settings */}
      <div className="p-3 border-t border-slate-200 bg-slate-50/50 space-y-2">
        {!isCollapsed && (
          <div className="flex items-center justify-between px-1 text-xs">
            <div className="flex items-center space-x-2">
              <span
                className={`w-2 h-2 rounded-full ${
                  backendConnected ? 'bg-emerald-500 animate-pulse' : 'bg-amber-400'
                }`}
              />
              <span className="text-slate-600 font-medium text-[11px]">
                {backendConnected ? 'Backend Connected' : 'Checking API...'}
              </span>
            </div>
            <span className="text-[10px] text-slate-400 font-mono">LangGraph RAG</span>
          </div>
        )}

        <button
          onClick={onOpenSettings}
          className={`w-full flex items-center rounded-lg text-slate-600 hover:bg-slate-100 hover:text-slate-900 transition-colors text-xs font-medium ${
            isCollapsed ? 'justify-center p-2.5' : 'px-3 py-2 space-x-2.5'
          }`}
          title="System Settings & Status"
        >
          <Settings className="w-4 h-4 flex-shrink-0 text-slate-400" />
          {!isCollapsed && <span>Settings & Details</span>}
        </button>
      </div>
    </aside>
  );
}
