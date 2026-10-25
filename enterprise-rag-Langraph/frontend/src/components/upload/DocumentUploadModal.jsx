import React, { useState, useRef } from 'react';
import {
  UploadCloud,
  FileText,
  X,
  CheckCircle2,
  AlertCircle,
  Loader2,
  Trash2,
  Layers,
} from 'lucide-react';
import { formatBytes, formatDate } from '../../utils/helpers';

export default function DocumentUploadModal({
  isOpen,
  onClose,
  documents,
  onUploadFile,
  onRemoveDocument,
  isUploading,
  uploadProgress,
  uploadError,
}) {
  const [dragActive, setDragActive] = useState(false);
  const [localError, setLocalError] = useState(null);
  const fileInputRef = useRef(null);

  if (!isOpen) return null;

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      processFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileInput = (e) => {
    if (e.target.files && e.target.files[0]) {
      processFile(e.target.files[0]);
    }
  };

  const processFile = async (file) => {
    setLocalError(null);
    if (!file.name.toLowerCase().endsWith('.pdf')) {
      setLocalError('Only PDF files are currently supported by the RAG backend.');
      return;
    }

    if (file.size > 50 * 1024 * 1024) {
      setLocalError('File size exceeds the 50MB maximum limit.');
      return;
    }

    try {
      await onUploadFile(file);
    } catch (err) {
      setLocalError(err.message || 'Upload failed');
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-xs p-4 animate-fadeIn">
      <div className="bg-white rounded-2xl shadow-xl border border-slate-200 max-w-lg w-full overflow-hidden flex flex-col max-h-[90vh]">
        {/* Modal Header */}
        <div className="flex items-center justify-between p-4 border-b border-slate-100">
          <div className="flex items-center space-x-2">
            <div className="p-2 rounded-lg bg-brand-50 text-brand-600">
              <UploadCloud className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-semibold text-slate-900 text-sm">
                Knowledge Base Documents
              </h3>
              <p className="text-xs text-slate-500">
                Upload PDFs for BM25 text & Pinecone vector indexing
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-lg transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-5 overflow-y-auto space-y-5">
          {/* Drag & Drop Zone */}
          <div
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
            className={`border-2 border-dashed rounded-xl p-6 text-center cursor-pointer transition-all ${
              dragActive
                ? 'border-brand-500 bg-brand-50/50'
                : 'border-slate-200 hover:border-brand-400 hover:bg-slate-50/50'
            }`}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf"
              onChange={handleFileInput}
              className="hidden"
            />

            <UploadCloud className="w-8 h-8 text-brand-600 mx-auto mb-2" />
            <p className="text-xs font-semibold text-slate-800">
              Click to browse or drag and drop your PDF
            </p>
            <p className="text-[11px] text-slate-400 mt-1">
              Supports standard PDFs up to 50MB
            </p>
          </div>

          {/* Upload Progress */}
          {isUploading && (
            <div className="p-3 bg-brand-50 border border-brand-200 rounded-xl space-y-2">
              <div className="flex items-center justify-between text-xs text-brand-900 font-medium">
                <span className="flex items-center space-x-2">
                  <Loader2 className="w-4 h-4 text-brand-600 animate-spin" />
                  <span>Processing & Ingesting PDF into RAG Pipeline...</span>
                </span>
                <span>{uploadProgress}%</span>
              </div>
              <div className="w-full bg-brand-200/50 rounded-full h-1.5 overflow-hidden">
                <div
                  className="bg-brand-600 h-full rounded-full transition-all duration-300"
                  style={{ width: `${uploadProgress}%` }}
                />
              </div>
              <p className="text-[10px] text-brand-700">
                Extracting text, chunking text, generating dense embeddings, and updating BM25 index.
              </p>
            </div>
          )}

          {/* Error Message */}
          {(localError || uploadError) && (
            <div className="p-3 bg-red-50 border border-red-200 rounded-xl text-xs text-red-700 flex items-start space-x-2">
              <AlertCircle className="w-4 h-4 text-red-600 flex-shrink-0 mt-0.5" />
              <span>{localError || uploadError}</span>
            </div>
          )}

          {/* List of Ingested Documents */}
          <div>
            <h4 className="text-xs font-semibold text-slate-800 uppercase tracking-wider mb-2 flex items-center justify-between">
              <span>Indexed Documents ({documents.length})</span>
            </h4>

            <div className="space-y-2 max-h-48 overflow-y-auto">
              {documents.map((doc) => (
                <div
                  key={doc.id}
                  className="p-2.5 bg-slate-50 border border-slate-200 rounded-lg flex items-center justify-between text-xs"
                >
                  <div className="flex items-center space-x-2.5 min-w-0">
                    <FileText className="w-4 h-4 text-brand-600 flex-shrink-0" />
                    <div className="min-w-0">
                      <p className="font-medium text-slate-800 truncate">{doc.name}</p>
                      <div className="flex items-center space-x-2 text-[10px] text-slate-400">
                        {doc.size && <span>{formatBytes(doc.size)}</span>}
                        {doc.chunksCreated && <span>• {doc.chunksCreated} chunks</span>}
                        <span>• {formatDate(doc.uploadedAt)}</span>
                      </div>
                    </div>
                  </div>

                  <button
                    onClick={() => onRemoveDocument(doc.id)}
                    className="p-1 text-slate-400 hover:text-red-600 rounded transition-colors"
                    title="Remove from local list"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              ))}

              {documents.length === 0 && (
                <div className="text-center py-4 border border-dashed border-slate-200 rounded-lg text-slate-400 text-xs">
                  No documents in knowledge base yet
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Modal Footer */}
        <div className="p-4 border-t border-slate-100 bg-slate-50 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-lg text-xs font-medium transition-colors"
          >
            Done
          </button>
        </div>
      </div>
    </div>
  );
}
