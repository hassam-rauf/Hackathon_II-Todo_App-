/**
 * Centralized API client for backend communication.
 * Task: T-025, T-038 (auth token integration)
 * Ref: specs/phase2-web/frontend-ui/plan.md — API Client
 */

import { authClient } from "@/lib/auth-client";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface Task {
  id: number;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface TaskCreate {
  title: string;
  description?: string;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
}

/** A single tool call from the AI agent response. */
export interface ToolCall {
  tool: string;
  args: Record<string, unknown>;
  result: Record<string, unknown>;
}

/** A chat message in the UI thread. */
export interface ChatMessage {
  id: number | string;
  role: "user" | "assistant";
  content: string;
  toolCalls?: ToolCall[];
  createdAt: string;
}

/** A conversation summary for the selector dropdown. */
export interface ChatConversation {
  id: number;
  preview: string;
  updatedAt: string;
}

/** Response from POST /api/{user_id}/chat. */
export interface ChatResponse {
  conversation_id: number;
  response: string;
  tool_calls: ToolCall[];
}

async function getAuthHeaders(): Promise<Record<string, string>> {
  try {
    const result = await authClient.token();
    if (result?.data?.token) {
      return { Authorization: `Bearer ${result.data.token}` };
    }
  } catch {
    // No token available
  }
  return {};
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const authHeaders = await getAuthHeaders();

  const res = await fetch(`${API}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...authHeaders,
      ...options.headers,
    },
  });

  if (res.status === 401) {
    window.location.href = "/signin";
    throw new Error("Session expired");
  }

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }

  return res.json();
}

export const api = {
  getTasks: (userId: string, status?: string): Promise<Task[]> =>
    request(`/api/${userId}/tasks${status ? `?status=${status}` : ""}`),

  createTask: (userId: string, data: TaskCreate): Promise<Task> =>
    request(`/api/${userId}/tasks`, {
      method: "POST",
      body: JSON.stringify(data),
    }),

  updateTask: (userId: string, taskId: number, data: TaskUpdate): Promise<Task> =>
    request(`/api/${userId}/tasks/${taskId}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),

  deleteTask: (userId: string, taskId: number): Promise<{ ok: boolean }> =>
    request(`/api/${userId}/tasks/${taskId}`, { method: "DELETE" }),

  toggleComplete: (userId: string, taskId: number): Promise<Task> =>
    request(`/api/${userId}/tasks/${taskId}/complete`, { method: "PATCH" }),

  // Chat API — Task: T005
  sendChatMessage: (
    userId: string,
    message: string,
    conversationId?: number,
  ): Promise<ChatResponse> =>
    request(`/api/${userId}/chat`, {
      method: "POST",
      body: JSON.stringify({
        message,
        ...(conversationId != null ? { conversation_id: conversationId } : {}),
      }),
    }),

  getConversations: (userId: string): Promise<ChatConversation[]> =>
    request<{ id: number; preview: string; updated_at: string }[]>(
      `/api/${userId}/conversations`,
    ).then((data) =>
      data.map((c) => ({ id: c.id, preview: c.preview, updatedAt: c.updated_at })),
    ),

  getMessages: (userId: string, conversationId: number): Promise<ChatMessage[]> =>
    request<{ id: number; role: string; content: string; created_at: string }[]>(
      `/api/${userId}/conversations/${conversationId}/messages`,
    ).then((data) =>
      data.map((m) => ({
        id: m.id,
        role: m.role as "user" | "assistant",
        content: m.content,
        createdAt: m.created_at,
      })),
    ),
};
