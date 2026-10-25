import { useState, useEffect, useCallback } from 'react';
import { api } from '../api/client';
import { generateId, getFilenameFromPath } from '../utils/helpers';

const UPLOADED_DOCS_KEY = 'enterprise_rag_uploaded_docs_v1';

export function useUpload() {
  const [documents, setDocuments] = useState(() => {
    try {
      const stored = localStorage.getItem(UPLOADED_DOCS_KEY);
      if (stored) return JSON.parse(stored);
    } catch (e) {
      console.error('Failed to load uploaded documents', e);
    }
    return [];
  });

  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadError, setUploadError] = useState(null);
  const [lastUploadedDoc, setLastUploadedDoc] = useState(null);

  useEffect(() => {
    try {
      localStorage.setItem(UPLOADED_DOCS_KEY, JSON.stringify(documents));
    } catch (e) {
      console.error('Failed to persist uploaded documents', e);
    }
  }, [documents]);

  const uploadFile = useCallback(async (file) => {
    if (!file) return null;
    setIsUploading(true);
    setUploadProgress(15);
    setUploadError(null);

    // Realistic upload progress simulation
    const pTimer1 = setTimeout(() => setUploadProgress(45), 600);
    const pTimer2 = setTimeout(() => setUploadProgress(75), 1800);

    try {
      const result = await api.uploadDocument(file);
      clearTimeout(pTimer1);
      clearTimeout(pTimer2);
      setUploadProgress(100);

      const docItem = {
        id: generateId('doc'),
        name: file.name,
        size: file.size,
        path: result.path,
        uploadedAt: result.uploaded_at || new Date().toISOString(),
        chunksCreated: result.splitted_data ? result.splitted_data.length : null,
        status: result.status || 'success',
        message: result.message || 'File uploaded successfully',
      };

      setDocuments((prev) => [docItem, ...prev]);
      setLastUploadedDoc(docItem);
      return docItem;
    } catch (err) {
      clearTimeout(pTimer1);
      clearTimeout(pTimer2);
      setUploadError(err.message || 'Failed to upload document');
      throw err;
    } finally {
      setIsUploading(false);
      setTimeout(() => setUploadProgress(0), 1000);
    }
  }, []);

  const removeDocument = useCallback((docId) => {
    setDocuments((prev) => prev.filter((d) => d.id !== docId));
  }, []);

  return {
    documents,
    isUploading,
    uploadProgress,
    uploadError,
    lastUploadedDoc,
    uploadFile,
    removeDocument,
  };
}
