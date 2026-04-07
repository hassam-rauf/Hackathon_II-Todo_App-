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
};
