/**
 * Create task form — title required, description optional.
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
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create task");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-xl border border-gray-200/50 shadow-sm p-5 mb-6">
      <div className="flex flex-col gap-3">
        <div>
          <label htmlFor="task-title" className="block text-sm font-medium text-gray-700 mb-1.5">
            Title *
          </label>
          <input
            id="task-title"
            type="text"
            placeholder="What needs to be done?"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full border border-gray-200 rounded-lg px-4 py-2.5 focus:ring-2 focus:ring-blue-500/30 focus:border-blue-400 outline-none transition-all"
            maxLength={200}
            aria-required="true"
          />
        </div>

        <div>
          <label htmlFor="task-description" className="block text-sm font-medium text-gray-700 mb-1.5">
            Description
          </label>
          <textarea
            id="task-description"
            placeholder="Add details (optional)"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full border border-gray-200 rounded-lg px-4 py-2.5 focus:ring-2 focus:ring-blue-500/30 focus:border-blue-400 outline-none resize-none transition-all"
            rows={2}
            maxLength={1000}
          />
        </div>

        {error && <p className="text-red-600 text-sm" role="alert">{error}</p>}

        <button
          type="submit"
          disabled={submitting}
          className="w-full sm:w-auto self-end bg-gradient-to-r from-blue-500 to-indigo-500 hover:from-blue-600 hover:to-indigo-600 text-white px-6 py-2.5 rounded-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-sm hover:shadow-md font-medium"
          aria-label="Add task"
        >
          {submitting ? "Adding..." : "Add Task"}
        </button>
      </div>
    </form>
  );
}
