/**
 * Conversation selector dropdown — switch between conversations or start new.
 * Shows preview snippet and relative time for each past conversation.
 *
 * Ref: specs/003-chatkit-frontend/plan.md — Component 6
 * Task: T011
 */

"use client";

import { useState } from "react";
import type { ChatConversation } from "@/lib/api";

interface ChatConversationSelectorProps {
  conversations: ChatConversation[];
  activeId: number | null;
  onSelect: (id: number | null) => void;
  loading: boolean;
}

function relativeTime(dateStr: string): string {
  const diff = Date.now() - new Date(dateStr).getTime();
  const minutes = Math.floor(diff / 60000);
  if (minutes < 1) return "just now";
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  return `${days}d ago`;
}

export default function ChatConversationSelector({
  conversations,
  activeId,
  onSelect,
  loading,
}: ChatConversationSelectorProps) {
  const [open, setOpen] = useState(false);

  const activeConv = conversations.find((c) => c.id === activeId);
  const label = activeConv
    ? activeConv.preview || "Conversation"
    : "New Conversation";

  return (
    <div className="relative px-3 py-2 border-b border-white/5">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between px-3 py-1.5 rounded-lg text-sm text-white/60 hover:text-white/80 hover:bg-white/5 transition-all"
        aria-label="Select conversation"
        aria-expanded={open}
      >
        <span className="truncate">{label}</span>
        <svg
          className={`w-4 h-4 shrink-0 transition-transform ${open ? "rotate-180" : ""}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {open && (
        <div className="absolute left-3 right-3 top-full mt-1 z-10 glass-card py-1 max-h-60 overflow-y-auto">
          {/* New conversation */}
          <button
            onClick={() => {
              onSelect(null);
              setOpen(false);
            }}
            className={`w-full text-left px-3 py-2 text-sm hover:bg-white/5 transition-colors flex items-center gap-2 ${
              activeId === null ? "text-emerald-400" : "text-white/50"
            }`}
          >
            <svg className="w-3.5 h-3.5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            New Conversation
          </button>

          {loading && (
            <div className="px-3 py-2 text-white/30 text-xs">Loading...</div>
          )}

          {/* Past conversations */}
          {conversations.map((conv) => (
            <button
              key={conv.id}
              onClick={() => {
                onSelect(conv.id);
                setOpen(false);
              }}
              className={`w-full text-left px-3 py-2 text-sm hover:bg-white/5 transition-colors ${
                conv.id === activeId ? "text-purple-400" : "text-white/50"
              }`}
            >
              <span className="block truncate text-xs">
                {conv.preview || "Empty conversation"}
              </span>
              <span className="text-white/20 text-[10px]">
                {relativeTime(conv.updatedAt)}
              </span>
            </button>
          ))}

          {!loading && conversations.length === 0 && (
            <div className="px-3 py-2 text-white/20 text-xs">No past conversations</div>
          )}
        </div>
      )}
    </div>
  );
}
