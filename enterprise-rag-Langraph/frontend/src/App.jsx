import React, { useState, useEffect } from 'react';
import Sidebar from './components/layout/Sidebar';
import ChatHeader from './components/layout/ChatHeader';
import MessageList from './components/chat/MessageList';
import MessageInput from './components/chat/MessageInput';
import DocumentUploadModal from './components/upload/DocumentUploadModal';
import SettingsModal from './components/layout/SettingsModal';
import { useChat } from './hooks/useChat';
import { useUpload } from './hooks/useUpload';
import { api } from './api/client';

export default function App() {
  const {
    conversations,
    activeId,
    setActiveId,
    activeConversation,
    isLoading,
    currentStep,
    sendMessage,
    stopGeneration,
    createNewChat,
    deleteConversation,
    clearCurrentChat,
    regenerateAnswer,
  } = useChat();

  const {
    documents,
    isUploading,
    uploadProgress,
    uploadError,
    lastUploadedDoc,
    uploadFile,
    removeDocument,
  } = useUpload();

  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false);
  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);
  const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [backendConnected, setBackendConnected] = useState(false);

  // Check backend health periodically
  useEffect(() => {
    let isMounted = true;
    const checkBackend = async () => {
      try {
        const res = await api.checkHealth();
        if (isMounted) setBackendConnected(res?.status === 'healthy');
      } catch {
        if (isMounted) setBackendConnected(false);
      }
    };

    checkBackend();
    const interval = setInterval(checkBackend, 15000);
    return () => {
      isMounted = false;
      clearInterval(interval);
    };
  }, []);

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-slate-50 font-sans">
      {/* Desktop & Collapsible Sidebar */}
      <div className="hidden md:flex h-full flex-shrink-0">
        <Sidebar
          conversations={conversations}
          activeId={activeId}
          onSelectConversation={setActiveId}
          onNewChat={createNewChat}
          onDeleteConversation={deleteConversation}
          documents={documents}
          onOpenUploadModal={() => setIsUploadModalOpen(true)}
          onOpenSettings={() => setIsSettingsOpen(true)}
          backendConnected={backendConnected}
          isCollapsed={isSidebarCollapsed}
          onToggleCollapse={() => setIsSidebarCollapsed(!isSidebarCollapsed)}
        />
      </div>

      {/* Mobile Drawer Sidebar */}
      {isMobileSidebarOpen && (
        <div className="fixed inset-0 z-40 md:hidden flex">
          <div
            className="fixed inset-0 bg-slate-900/40 backdrop-blur-xs transition-opacity"
            onClick={() => setIsMobileSidebarOpen(false)}
          />
          <div className="relative z-50 w-72 max-w-[80vw] h-full bg-white shadow-2xl">
            <Sidebar
              conversations={conversations}
              activeId={activeId}
              onSelectConversation={(id) => {
                setActiveId(id);
                setIsMobileSidebarOpen(false);
              }}
              onNewChat={() => {
                createNewChat();
                setIsMobileSidebarOpen(false);
              }}
              onDeleteConversation={deleteConversation}
              documents={documents}
              onOpenUploadModal={() => {
                setIsUploadModalOpen(true);
                setIsMobileSidebarOpen(false);
              }}
              onOpenSettings={() => {
                setIsSettingsOpen(true);
                setIsMobileSidebarOpen(false);
              }}
              backendConnected={backendConnected}
              isCollapsed={false}
              onToggleCollapse={() => setIsMobileSidebarOpen(false)}
            />
          </div>
        </div>
      )}

      {/* Main Chat Interface */}
      <main className="flex-1 flex flex-col h-full min-w-0 bg-slate-50 relative">
        <ChatHeader
          title={activeConversation?.title}
          onToggleMobileSidebar={() => setIsMobileSidebarOpen(!isMobileSidebarOpen)}
          onClearChat={clearCurrentChat}
          onOpenUploadModal={() => setIsUploadModalOpen(true)}
          hasMessages={activeConversation?.messages?.length > 0}
        />

        {/* Message Stream */}
        <MessageList
          messages={activeConversation?.messages || []}
          isLoading={isLoading}
          currentStep={currentStep}
          onSelectPrompt={(prompt) => sendMessage(prompt)}
          onRegenerate={regenerateAnswer}
        />

        {/* Message Input Box */}
        <MessageInput
          onSendMessage={sendMessage}
          onStopGeneration={stopGeneration}
          isLoading={isLoading}
          onUploadFile={uploadFile}
          isUploading={isUploading}
          uploadProgress={uploadProgress}
          lastUploadedDoc={lastUploadedDoc}
        />
      </main>

      {/* Upload Modal */}
      <DocumentUploadModal
        isOpen={isUploadModalOpen}
        onClose={() => setIsUploadModalOpen(false)}
        documents={documents}
        onUploadFile={uploadFile}
        onRemoveDocument={removeDocument}
        isUploading={isUploading}
        uploadProgress={uploadProgress}
        uploadError={uploadError}
      />

      {/* Settings Modal */}
      <SettingsModal
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
      />
    </div>
  );
}
