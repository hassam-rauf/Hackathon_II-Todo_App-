/**
 * Create task form — dark glass theme.
 * Task: T-027
 */

"use client";

import { useState } from "react";

interface TaskFormProps {
  onSubmit: (title: string, description?: string) => Promise<void>;
}

export default function TaskForm({ onSubmit }: TaskFormProps) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [expanded, setExpanded] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const trimmed = title.trim();

    if (!trimmed) {
      setError("Title is required");
      return;
    }

    setError("");
    setSubmitting(true);

    try {
      await onSubmit(trimmed, description.trim() || undefined);
      setTitle("");
      setDescription("");
      setExpanded(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create task");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="glass-card p-5 mb-6">
      <div className="flex flex-col gap-3">
        <div className="flex gap-3">
          <input
            type="text"
            placeholder="What needs to be done?"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            onFocus={() => setExpanded(true)}
            className="glass-input flex-1 px-4 py-2.5"
            maxLength={200}
            aria-required="true"
            aria-label="Task title"
          />
          <button
            type="submit"
            disabled={submitting}
            className="bg-emerald-500 hover:bg-emerald-400 text-white px-5 py-2.5 rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-emerald-500/10 font-medium text-sm flex items-center gap-2 flex-shrink-0"
            aria-label="Add task"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
            </svg>
            {submitting ? "Adding..." : "New Task"}
          </button>
        </div>

        {expanded && (
          <textarea
            placeholder="Add details (optional)"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="glass-input w-full px-4 py-2.5 resize-none"
            rows={2}
            maxLength={1000}
            aria-label="Task description"
          />
        )}

        {error && <p className="text-red-400 text-sm" role="alert">{error}</p>}
      </div>
    </form>
  );
}
