/**
 * Chat message list — displays message bubbles and tool call chips.
 * Auto-scrolls to latest message. Shows typing indicator when loading.
 *
 * Ref: specs/003-chatkit-frontend/plan.md — Component 4
 * Task: T008
 */

"use client";

import { useEffect, useRef } from "react";
import type { ChatMessage } from "@/lib/api";
import ToolCallChip from "@/components/ToolCallChip";

interface ChatMessagesProps {
  messages: ChatMessage[];
  isLoading: boolean;
}

export default function ChatMessages({ messages, isLoading }: ChatMessagesProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  if (messages.length === 0 && !isLoading) {
    return (
      <div className="flex-1 flex items-center justify-center p-6">
        <div className="text-center">
          <div className="text-3xl mb-3">💬</div>
          <p className="text-white/40 text-sm">Ask the AI to manage your tasks</p>
          <p className="text-white/20 text-xs mt-1">
            Try &quot;Add a task called Buy groceries&quot;
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-3">
      {messages.map((msg) => (
        <div key={msg.id}>
          {/* Tool call chips (above assistant message) */}
          {msg.role === "assistant" && msg.toolCalls && msg.toolCalls.length > 0 && (
            <div className="flex flex-wrap gap-1.5 mb-2 justify-start">
              {msg.toolCalls.map((tc, i) => (
                <ToolCallChip key={`${msg.id}-tc-${i}`} toolCall={tc} />
              ))}
            </div>
          )}

          {/* Message bubble */}
          <div
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`max-w-[85%] px-4 py-2.5 text-sm leading-relaxed break-words ${
                msg.role === "user"
                  ? "chat-bubble-user text-emerald-100"
                  : "chat-bubble-assistant text-purple-100"
              }`}
            >
              {msg.content}
            </div>
          </div>
        </div>
      ))}

      {/* Typing indicator */}
      {isLoading && (
        <div className="flex justify-start">
          <div className="chat-bubble-assistant px-4 py-3 flex items-center gap-1.5">
            <span className="typing-dot" />
            <span className="typing-dot" />
            <span className="typing-dot" />
          </div>
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  );
}
