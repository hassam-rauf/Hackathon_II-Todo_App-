/**
 * OpenAI ChatKit Web Component wrapper.
 * Loads the ChatKit script from CDN and configures it with CustomApiConfig
 * to connect to our backend chat endpoint.
 *
 * @see https://platform.openai.com/docs/guides/chatkit
 * Uses @openai/chatkit types for full type safety.
 *
 * Ref: specs/003-chatkit-frontend/plan.md
 */

"use client";

import { useEffect, useRef, useCallback } from "react";
import type { ChatKitOptions, CustomApiConfig, OpenAIChatKit } from "@openai/chatkit";

const CHATKIT_SCRIPT_URL = "https://cdn.openai.com/chatkit/chatkit-latest.js";

interface ChatKitPanelProps {
  isOpen: boolean;
  onClose: () => void;
  userId: string;
  onTasksChanged: () => void;
}

export default function ChatKitPanel({
  isOpen,
  onClose,
  userId,
  onTasksChanged,
}: ChatKitPanelProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const chatkitRef = useRef<OpenAIChatKit | null>(null);
  const scriptLoaded = useRef(false);

  const loadScript = useCallback((): Promise<void> => {
    if (scriptLoaded.current) return Promise.resolve();

    return new Promise((resolve, reject) => {
      // Check if already loaded
      if (document.querySelector(`script[src="${CHATKIT_SCRIPT_URL}"]`)) {
        scriptLoaded.current = true;
        resolve();
        return;
      }

      const script = document.createElement("script");
      script.src = CHATKIT_SCRIPT_URL;
      script.type = "module";
      script.onload = () => {
        scriptLoaded.current = true;
        resolve();
      };
      script.onerror = () => reject(new Error("Failed to load ChatKit script"));
      document.head.appendChild(script);
    });
  }, []);

  const initChatKit = useCallback(async () => {
    if (!containerRef.current) return;

    try {
      await loadScript();
    } catch {
      // Script load failed — ChatKit CDN may be unreachable
      return;
    }

    // Create the web component if it doesn't exist
    if (!chatkitRef.current) {
      const element = document.createElement("openai-chatkit") as OpenAIChatKit;
      element.style.width = "100%";
      element.style.height = "100%";
      containerRef.current.appendChild(element);
      chatkitRef.current = element;

      // Listen for tool-related events to refresh tasks
      element.addEventListener("chatkit.response.end", () => {
        onTasksChanged();
      });
    }

    // Configure ChatKit with our backend
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    const domainKey = process.env.NEXT_PUBLIC_OPENAI_DOMAIN_KEY || "";

    const apiConfig: CustomApiConfig = {
      url: `${apiUrl}/api/${userId}/chat`,
      domainKey,
    };

    const options: ChatKitOptions = {
      api: apiConfig,
      theme: {
        colorScheme: "dark",
        radius: "round",
        density: "compact",
        color: {
          accent: {
            primary: "#8b5cf6",
            level: 2,
          },
          surface: {
            background: "#0d1130",
            foreground: "#e2e8f0",
          },
          grayscale: {
            hue: 240,
            tint: 2,
          },
        },
      },
      header: {
        enabled: true,
        title: { text: "Todo AI Assistant" },
        rightAction: {
          icon: "close",
          onClick: onClose,
        },
      },
      history: {
        enabled: true,
        showDelete: true,
      },
      startScreen: {
        greeting: "How can I help manage your tasks?",
        prompts: [
          {
            label: "Show my tasks",
            prompt: "List all my pending tasks",
            icon: "document",
          },
          {
            label: "Add a new task",
            prompt: "Add a task: ",
            icon: "plus",
          },
          {
            label: "What's completed?",
            prompt: "Show me my completed tasks",
            icon: "check-circle",
          },
        ],
      },
      composer: {
        placeholder: "Ask me to manage your tasks...",
      },
      disclaimer: {
        text: "AI assistant for task management. Powered by OpenAI.",
      },
    };

    chatkitRef.current.setOptions(options);
  }, [userId, onClose, onTasksChanged, loadScript]);

  useEffect(() => {
    if (isOpen) {
      initChatKit();
    }
  }, [isOpen, initChatKit]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (chatkitRef.current && containerRef.current) {
        try {
          containerRef.current.removeChild(chatkitRef.current);
        } catch {
          // Already removed
        }
        chatkitRef.current = null;
      }
    };
  }, []);

  if (!isOpen) return null;

  return (
    <>
      {/* Mobile backdrop */}
      <div
        className="fixed inset-0 bg-black/50 z-40 md:hidden"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* ChatKit container */}
      <div
        className="fixed top-0 right-0 h-full z-50 flex flex-col chat-panel-enter
          w-full md:w-96
          bg-[#0d1130]/95 backdrop-blur-xl
          border-l border-white/8"
        role="complementary"
        aria-label="AI Chat Panel (ChatKit)"
      >
        <div ref={containerRef} className="w-full h-full" />
      </div>
    </>
  );
}
