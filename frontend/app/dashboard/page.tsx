/**
 * Member dashboard — space theme with sidebar, stats, and productivity chart.
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
import ProductivityChart from "@/components/ProductivityChart";
import ChatKitPanel from "@/components/ChatKitPanel";

export default function DashboardPage() {
  const { data: session, isPending } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [authChecked, setAuthChecked] = useState(false);
  const [activeTab, setActiveTab] = useState("dashboard");
  const [chatOpen, setChatOpen] = useState(false);

  const userId = session?.user?.id;
  const userName = session?.user?.name || session?.user?.email?.split("@")[0] || "User";

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

  if (isPending || (!session && !authChecked)) {
    return (
      <div className="min-h-screen space-bg flex items-center justify-center">
        <div className="animate-spin h-8 w-8 border-4 border-purple-500 border-t-transparent rounded-full" />
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

  const completed = tasks.filter((t) => t.completed).length;
  const pending = tasks.filter((t) => !t.completed).length;
  const total = tasks.length;
  const rate = total > 0 ? Math.round((completed / total) * 100) : 0;

  return (
    <div className="min-h-screen space-bg relative">
      {/* Stars */}
      <div className="fixed inset-0 stars pointer-events-none" />

      <div className="relative z-10 flex min-h-screen">
        {/* Sidebar */}
        <aside className="hidden md:flex w-64 flex-col p-4 border-r border-white/5">
          {/* Logo */}
          <div className="flex items-center gap-2 px-4 py-3 mb-6">
            <svg className="w-6 h-6 text-emerald-400" fill="currentColor" viewBox="0 0 24 24">
              <path d="M3 5a2 2 0 012-2h14a2 2 0 012 2v14a2 2 0 01-2 2H5a2 2 0 01-2-2V5zm6 7l2 2 4-4" />
              <path fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4" />
            </svg>
            <span className="text-lg font-bold text-white">ToDo</span>
          </div>

          {/* Nav items */}
          <nav className="flex flex-col gap-1">
            <button
              onClick={() => setActiveTab("dashboard")}
              className={`sidebar-item ${activeTab === "dashboard" ? "active" : ""}`}
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
              </svg>
              Dashboard
            </button>
            <button
              onClick={() => setActiveTab("todos")}
              className={`sidebar-item ${activeTab === "todos" ? "active" : ""}`}
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
              </svg>
              My Todos
            </button>
            <button
              onClick={() => setChatOpen(true)}
              className={`sidebar-item ${chatOpen ? "active" : ""}`}
              aria-label="Open AI Chat"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
              AI Chat
            </button>
            <button
              onClick={() => setActiveTab("settings")}
              className={`sidebar-item ${activeTab === "settings" ? "active" : ""}`}
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              Settings
            </button>
          </nav>

          {/* Spacer */}
          <div className="flex-1" />

          {/* Sign out */}
          <button
            onClick={handleSignOut}
            className="sidebar-item text-red-400/60 hover:text-red-400 hover:bg-red-500/10"
            aria-label="Sign out"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            Sign Out
          </button>
        </aside>

        {/* Main Content */}
        <main className="flex-1 overflow-y-auto">
          {/* Top bar */}
          <header className="flex items-center justify-between px-6 py-5 border-b border-white/5">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-blue-500 flex items-center justify-center text-white font-semibold text-sm">
                {userName.charAt(0).toUpperCase()}
              </div>
              <div>
                <p className="text-white font-medium">Hi, {userName}!</p>
                <p className="text-white/30 text-xs">Welcome back</p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              {/* Mobile menu */}
              <button
                onClick={handleSignOut}
                className="md:hidden text-white/40 hover:text-white p-2"
                aria-label="Sign out"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
              </button>
            </div>
          </header>

          {/* Dashboard content */}
          <div className="p-6 max-w-6xl mx-auto">
            {/* Stats Bar */}
            <div className="animate-fade-in mb-6">
              <StatsBar tasks={tasks} />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {/* Left — Task lists (2 cols) */}
              <div className="lg:col-span-2 space-y-6">
                {/* Add task */}
                <div className="animate-fade-in-delay-1">
                  <TaskForm onSubmit={handleCreate} />
                </div>

                {/* Tasks */}
                {loading && (
                  <div className="space-y-3" aria-label="Loading tasks">
                    {[1, 2, 3].map((i) => (
                      <div key={i} className="animate-pulse glass-card p-4">
                        <div className="h-4 bg-white/10 rounded w-3/4 mb-2" />
                        <div className="h-3 bg-white/10 rounded w-1/2" />
                      </div>
                    ))}
                  </div>
                )}

                {error && (
                  <div className="text-center py-8">
                    <p className="text-red-400 mb-3">{error}</p>
                    <button
                      onClick={fetchTasks}
                      className="px-4 py-2 bg-purple-500/20 text-purple-300 rounded-lg hover:bg-purple-500/30 transition-all border border-purple-500/20"
                    >
                      Retry
                    </button>
                  </div>
                )}

                {!loading && !error && (
                  <div className="animate-fade-in-delay-2">
                    <h2 className="text-white/60 text-sm font-medium mb-3 uppercase tracking-wider">
                      Today&apos;s Tasks
                    </h2>
                    <TaskList
                      tasks={tasks}
                      onToggle={handleToggle}
                      onDelete={handleDelete}
                      onUpdate={handleUpdate}
                    />
                  </div>
                )}
              </div>

              {/* Right — Sidebar widgets */}
              <div className="space-y-6 animate-fade-in-delay-3">
                {/* Quick Notes */}
                <div className="glass-card p-5">
                  <h3 className="text-white/80 text-sm font-semibold mb-3 flex items-center gap-2">
                    <svg className="w-4 h-4 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                    Quick Notes
                  </h3>
                  <div className="space-y-2 text-sm">
                    <p className="text-white/30">
                      {pending > 0
                        ? `You have ${pending} pending task${pending !== 1 ? "s" : ""} to complete.`
                        : "All tasks completed! Great work."}
                    </p>
                    {completed > 0 && (
                      <p className="text-emerald-400/60 text-xs">
                        {completed} task{completed !== 1 ? "s" : ""} completed so far
                      </p>
                    )}
                  </div>
                </div>

                {/* Productivity Stats */}
                <div className="glass-card p-5">
                  <h3 className="text-white/80 text-sm font-semibold mb-4 flex items-center gap-2">
                    <svg className="w-4 h-4 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                    </svg>
                    Productivity Stats
                  </h3>
                  <ProductivityChart rate={rate} completed={completed} pending={pending} total={total} />
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>

      {/* Mobile FAB — AI Chat toggle */}
      {!chatOpen && (
        <button
          onClick={() => setChatOpen(true)}
          className="fixed bottom-6 right-6 z-30 md:hidden w-14 h-14 rounded-full bg-emerald-500/80 hover:bg-emerald-500 shadow-lg shadow-emerald-500/20 flex items-center justify-center transition-all"
          aria-label="Open AI Chat"
        >
          <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
          </svg>
        </button>
      )}

      {/* ChatKit Panel — OpenAI ChatKit Web Component (primary UI per requirement) */}
      {userId && (
        <ChatKitPanel
          isOpen={chatOpen}
          onClose={() => setChatOpen(false)}
          userId={userId}
          onTasksChanged={fetchTasks}
        />
      )}
    </div>
  );
}
