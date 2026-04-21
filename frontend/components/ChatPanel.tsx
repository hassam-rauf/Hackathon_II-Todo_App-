/**
 * Chat panel container — slide-in panel with state management.
 * Connects to POST /api/{user_id}/chat, manages messages and conversation state.
 *
 * Ref: specs/003-chatkit-frontend/plan.md — Component 3
 * Task: T009
 */

"use client";

import { useCallback, useEffect, useState } from "react";
import { api, type ChatMessage, type ChatConversation } from "@/lib/api";
import ChatMessages from "@/components/ChatMessages";
import ChatInput from "@/components/ChatInput";
import ChatConversationSelector from "@/components/ChatConversationSelector";

interface ChatPanelProps {
  isOpen: boolean;
  onClose: () => void;
  userId: string;
  onTasksChanged: () => void;
}

export default function ChatPanel({
  isOpen,
  onClose,
  userId,
  onTasksChanged,
}: ChatPanelProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [conversations, setConversations] = useState<ChatConversation[]>([]);
  const [conversationsLoading, setConversationsLoading] = useState(false);

  const fetchConversations = useCallback(async () => {
    setConversationsLoading(true);
    try {
      const data = await api.getConversations(userId);
      setConversations(data);
    } catch {
      // Non-critical — selector just won't show history
    } finally {
      setConversationsLoading(false);
    }
  }, [userId]);

  useEffect(() => {
    if (isOpen && userId) {
      fetchConversations();
    }
  }, [isOpen, userId, fetchConversations]);

  async function handleSelectConversation(id: number | null) {
    if (id === null) {
      // New conversation
      setMessages([]);
      setConversationId(null);
      setError(null);
      return;
    }

    // Load existing conversation messages
    try {
      setLoading(true);
      setError(null);
      const msgs = await api.getMessages(userId, id);
      setMessages(msgs);
      setConversationId(id);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load conversation");
    } finally {
      setLoading(false);
    }
  }

  async function handleSend(text: string) {
    // Optimistically add user message
    const tempId = `temp-${Date.now()}`;
    const userMsg: ChatMessage = {
      id: tempId,
      role: "user",
      content: text,
      createdAt: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);
    setError(null);

    try {
      const res = await api.sendChatMessage(userId, text, conversationId ?? undefined);

      // Update conversation ID (first message creates it)
      if (!conversationId) {
        setConversationId(res.conversation_id);
      }

      // Add assistant message
      const assistantMsg: ChatMessage = {
        id: `assistant-${Date.now()}`,
        role: "assistant",
        content: res.response,
        toolCalls: res.tool_calls.length > 0 ? res.tool_calls : undefined,
        createdAt: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, assistantMsg]);

      // Refresh task list if agent used tools
      if (res.tool_calls.length > 0) {
        onTasksChanged();
      }

      // Refresh conversations list
      fetchConversations();
    } catch (err) {
      const errMsg = err instanceof Error ? err.message : "Failed to send message";
      setError(errMsg);
      // Remove the optimistic user message on error
      setMessages((prev) => prev.filter((m) => m.id !== tempId));
    } finally {
      setLoading(false);
    }
  }

  function handleRetry() {
    // Find the last user message and resend
    const lastUserMsg = [...messages].reverse().find((m) => m.role === "user");
    if (lastUserMsg) {
      setError(null);
      handleSend(lastUserMsg.content);
    }
  }

  if (!isOpen) return null;

  return (
    <>
      {/* Mobile backdrop */}
      <div
        className="fixed inset-0 bg-black/50 z-40 md:hidden"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Panel */}
      <div
        className="fixed top-0 right-0 h-full z-50 flex flex-col chat-panel-enter
          w-full md:w-96
          bg-[#0d1130]/95 backdrop-blur-xl
          border-l border-white/8"
        role="complementary"
        aria-label="AI Chat Panel"
      >
        {/* Header */}
        <div className="flex items-center justify-between px-4 py-3 border-b border-white/5">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-full bg-gradient-to-br from-purple-500 to-emerald-500 flex items-center justify-center">
              <svg className="w-3.5 h-3.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </div>
            <span className="text-white/90 text-sm font-medium">AI Assistant</span>
          </div>
          <button
            onClick={onClose}
            className="text-white/40 hover:text-white/80 p-1 transition-colors"
            aria-label="Close chat panel"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Conversation selector */}
        <ChatConversationSelector
          conversations={conversations}
          activeId={conversationId}
          onSelect={handleSelectConversation}
          loading={conversationsLoading}
        />

        {/* Messages */}
        <ChatMessages messages={messages} isLoading={loading && !error} />

        {/* Error */}
        {error && (
          <div className="px-4 py-2 text-center">
            <p className="text-red-400/80 text-xs mb-1">{error}</p>
            <button
              onClick={handleRetry}
              className="text-purple-400/80 hover:text-purple-300 text-xs underline"
            >
              Retry
            </button>
          </div>
        )}

        {/* Input */}
        <ChatInput onSend={handleSend} disabled={loading} isLoading={loading} />
      </div>
    </>
  );
}
