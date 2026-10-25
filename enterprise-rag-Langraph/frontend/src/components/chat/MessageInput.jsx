import React, { useState, useRef, useEffect } from 'react';
import {
  ArrowUp,
  Square,
  Paperclip,
  Loader2,
  FileText,
  X,
  AlertCircle,
  CheckCircle2,
} from 'lucide-react';
import { formatBytes } from '../../utils/helpers';

export default function MessageInput({
  onSendMessage,
  onStopGeneration,
  isLoading,
  onUploadFile,
  isUploading,
  uploadProgress,
  lastUploadedDoc,
}) {
  const [input, setInput] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileError, setFileError] = useState(null);
  const textareaRef = useRef(null);
  const fileInputRef = useRef(null);

  // Auto-resize textarea based on content
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      const scrollHeight = textareaRef.current.scrollHeight;
      textareaRef.current.style.height = `${Math.min(scrollHeight, 180)}px`;
    }
  }, [input]);

  const handleSubmit = (e) => {
    e?.preventDefault();
    if (isLoading) return;

    if (input.trim()) {
      onSendMessage(input.trim());
      setInput('');
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleFileSelect = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setFileError(null);
    if (!file.name.toLowerCase().endsWith('.pdf')) {
      setFileError('Only PDF files are supported by the backend extractor.');
      return;
    }

    if (file.size > 50 * 1024 * 1024) {
      setFileError('File size exceeds the 50MB limit.');
      return;
    }

    setSelectedFile(file);
    try {
      await onUploadFile(file);
      // Auto-clear file preview after short delay upon success
      setTimeout(() => setSelectedFile(null), 3000);
    } catch (err) {
      setFileError(err.message || 'Upload failed');
    } finally {
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const canSubmit = input.trim().length > 0 && !isLoading;

  return (
    <div className="border-t border-slate-200 bg-white/95 backdrop-blur p-4">
      <div className="max-w-4xl mx-auto">
        {/* Document Upload Status Bar (if file selected or uploaded) */}
        {selectedFile && (
          <div className="mb-2 p-2 bg-slate-50 border border-slate-200 rounded-lg flex items-center justify-between text-xs">
            <div className="flex items-center space-x-2 min-w-0">
              <FileText className="w-4 h-4 text-brand-600 flex-shrink-0" />
              <span className="font-medium text-slate-800 truncate">{selectedFile.name}</span>
              <span className="text-slate-400">({formatBytes(selectedFile.size)})</span>

              {isUploading && (
                <div className="flex items-center space-x-1.5 text-brand-600 ml-2">
                  <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  <span>Extracting & Indexing ({uploadProgress}%)</span>
                </div>
              )}

              {!isUploading && !fileError && (
                <div className="flex items-center space-x-1 text-emerald-600 ml-2">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>Indexed into OpenSearch & Pinecone</span>
                </div>
              )}
            </div>

            <button
              onClick={() => {
                setSelectedFile(null);
                setFileError(null);
              }}
              className="p-1 text-slate-400 hover:text-slate-600 rounded"
              title="Dismiss"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          </div>
        )}

        {/* Upload Error Banner */}
        {fileError && (
          <div className="mb-2 p-2 bg-red-50 border border-red-200 rounded-lg flex items-center justify-between text-xs text-red-700">
            <div className="flex items-center space-x-1.5">
              <AlertCircle className="w-4 h-4 flex-shrink-0" />
              <span>{fileError}</span>
            </div>
            <button
              onClick={() => setFileError(null)}
              className="p-1 text-red-500 hover:text-red-800"
            >
              <X className="w-3 h-3" />
            </button>
          </div>
        )}

        {/* Text Input Container */}
        <div className="relative flex items-end border border-slate-300 rounded-2xl bg-white shadow-xs focus-within:border-brand-500 focus-within:ring-2 focus-within:ring-brand-500/20 transition-all p-2">
          {/* File Attachment Button */}
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileSelect}
            accept=".pdf"
            className="hidden"
          />
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            disabled={isUploading || isLoading}
            className="p-2 text-slate-400 hover:text-brand-600 hover:bg-slate-100 rounded-xl transition-colors disabled:opacity-40 disabled:cursor-not-allowed flex-shrink-0"
            title="Attach PDF document for RAG indexing"
          >
            <Paperclip className="w-4 h-4" />
          </button>

          {/* Multiline Textarea */}
          <textarea
            ref={textareaRef}
            rows={1}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask a question about your knowledge base..."
            className="flex-1 max-h-44 resize-none border-0 bg-transparent px-3 py-2 text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-0 leading-relaxed font-sans"
          />

          {/* Send / Stop Generation Button */}
          <div className="flex-shrink-0 flex items-center space-x-1 pl-1">
            {isLoading ? (
              <button
                type="button"
                onClick={onStopGeneration}
                className="p-2 bg-slate-900 hover:bg-slate-800 text-white rounded-xl shadow-xs transition-colors flex items-center justify-center"
                title="Stop generation"
              >
                <Square className="w-4 h-4 fill-current" />
              </button>
            ) : (
              <button
                type="button"
                onClick={handleSubmit}
                disabled={!canSubmit}
                className={`p-2 rounded-xl shadow-xs transition-all flex items-center justify-center ${
                  canSubmit
                    ? 'bg-brand-600 hover:bg-brand-700 active:bg-brand-800 text-white cursor-pointer'
                    : 'bg-slate-100 text-slate-400 cursor-not-allowed'
                }`}
                title="Send message (Enter)"
              >
                <ArrowUp className="w-4 h-4 stroke-[2.5]" />
              </button>
            )}
          </div>
        </div>

        {/* Input Footer Note */}
        <div className="flex items-center justify-between mt-2 px-2 text-[11px] text-slate-400">
          <span>
            Press <kbd className="font-mono bg-slate-100 px-1 py-0.5 rounded border border-slate-200">Enter</kbd> to send, <kbd className="font-mono bg-slate-100 px-1 py-0.5 rounded border border-slate-200">Shift + Enter</kbd> for newline
          </span>
          <span className="hidden sm:inline">
            Answers are grounded via OpenSearch BM25 + Pinecone
          </span>
        </div>
      </div>
    </div>
  );
}
