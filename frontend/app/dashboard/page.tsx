/**
 * Member dashboard — stats overview + task management.
 * Authenticated route (protected by middleware).
 */

"use client";

import { useCallback, useEffect, useState } from "react";
import { api, type Task } from "@/lib/api";
import { useAuth } from "@/components/session-provider";
import { signOut, getSession } from "@/lib/auth-client";
import TaskForm from "@/components/TaskForm";
import TaskList from "@/components/TaskList";
import StatsBar from "@/components/StatsBar";

export default function DashboardPage() {
  const { data: session, isPending } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [authChecked, setAuthChecked] = useState(false);

  const userId = session?.user?.id;
  const userName = session?.user?.name || session?.user?.email?.split("@")[0] || "User";

  // Double-check session with a direct fetch if useSession says no session
  useEffect(() => {
    if (!isPending && !session && !authChecked) {
      getSession()
        .then((res) => {
          setAuthChecked(true);
          if (!res.data) {
            window.location.href = "/signin";
          }
        })
        .catch(() => {
          setAuthChecked(true);
          window.location.href = "/signin";
        });
    } else if (session) {
      setAuthChecked(true);
    }
  }, [isPending, session, authChecked]);

  const fetchTasks = useCallback(async () => {
    if (!userId) return;
    try {
      setError("");
      const data = await api.getTasks(userId);
      setTasks(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load tasks");
    } finally {
      setLoading(false);
    }
  }, [userId]);

  useEffect(() => {
    if (userId) fetchTasks();
  }, [userId, fetchTasks]);

  // Loading state
  if (isPending || (!session && !authChecked)) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 flex items-center justify-center">
        <div className="animate-spin h-8 w-8 border-4 border-blue-600 border-t-transparent rounded-full" />
      </div>
    );
  }

  if (!session) return null;

  async function handleCreate(title: string, description?: string) {
    const task = await api.createTask(userId!, { title, description });
    setTasks((prev) => [task, ...prev]);
  }

  async function handleToggle(taskId: number) {
    setTasks((prev) =>
      prev.map((t) => (t.id === taskId ? { ...t, completed: !t.completed } : t))
    );
    try {
      await api.toggleComplete(userId!, taskId);
    } catch {
      setTasks((prev) =>
        prev.map((t) => (t.id === taskId ? { ...t, completed: !t.completed } : t))
      );
    }
  }

  async function handleDelete(taskId: number) {
    await api.deleteTask(userId!, taskId);
    setTasks((prev) => prev.filter((t) => t.id !== taskId));
  }

  async function handleUpdate(taskId: number, title: string, description?: string) {
    const updated = await api.updateTask(userId!, taskId, { title, description });
    setTasks((prev) => prev.map((t) => (t.id === taskId ? updated : t)));
  }

  async function handleSignOut() {
    await signOut();
    window.location.href = "/signin";
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      {/* Header */}
      <header className="bg-gradient-to-r from-blue-600 to-indigo-600 shadow-lg">
        <div className="max-w-5xl mx-auto px-6 py-5 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 bg-white/20 backdrop-blur-sm rounded-lg flex items-center justify-center">
              <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <h1 className="text-lg font-semibold text-white">TodoApp</h1>
              <p className="text-xs text-white/60">
                Welcome, {userName}
              </p>
            </div>
          </div>
          <button
            onClick={handleSignOut}
            className="bg-white/15 backdrop-blur-sm text-white/90 hover:text-white hover:bg-white/25 px-4 py-2 rounded-lg text-sm font-medium transition-all border border-white/10"
            aria-label="Sign out"
          >
            Sign Out
          </button>
        </div>
      </header>

      {/* Stats Bar */}
      <div className="max-w-5xl mx-auto px-6 -mt-4 relative z-10 animate-fade-in">
        <StatsBar tasks={tasks} />
      </div>

      {/* Main Content */}
      <main className="max-w-3xl mx-auto px-6 py-8">
        <div className="animate-fade-in-delay-1">
          <TaskForm onSubmit={handleCreate} />
        </div>

        {loading && (
          <div className="space-y-3" aria-label="Loading tasks">
            {[1, 2, 3].map((i) => (
              <div key={i} className="animate-pulse bg-white rounded-xl border border-gray-200/50 p-4">
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-2" />
                <div className="h-3 bg-gray-200 rounded w-1/2" />
              </div>
            ))}
          </div>
        )}

        {error && (
          <div className="text-center py-8">
            <p className="text-red-600 mb-3">{error}</p>
            <button
              onClick={fetchTasks}
              className="px-4 py-2 bg-gradient-to-r from-blue-500 to-indigo-500 text-white rounded-lg hover:shadow-lg transition-all"
            >
              Retry
            </button>
          </div>
        )}

        {!loading && !error && (
          <div className="animate-fade-in-delay-2">
            <TaskList
              tasks={tasks}
              onToggle={handleToggle}
              onDelete={handleDelete}
              onUpdate={handleUpdate}
            />
          </div>
        )}
      </main>
    </div>
  );
}
