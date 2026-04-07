/**
 * Single task card with toggle, edit, delete actions.
 * Tasks: T-028, T-029, T-030
 */

"use client";

import { useState } from "react";
import type { Task } from "@/lib/api";

interface TaskCardProps {
  task: Task;
  onToggle: (taskId: number) => Promise<void>;
  onDelete: (taskId: number) => Promise<void>;
  onUpdate: (taskId: number, title: string, description?: string) => Promise<void>;
}

export default function TaskCard({ task, onToggle, onDelete, onUpdate }: TaskCardProps) {
  const [editing, setEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [editDescription, setEditDescription] = useState(task.description || "");
  const [loading, setLoading] = useState(false);

  const date = new Date(task.created_at).toLocaleDateString();

  async function handleToggle() {
    setLoading(true);
    try {
      await onToggle(task.id);
    } finally {
      setLoading(false);
    }
  }

  async function handleDelete() {
    if (!window.confirm(`Delete "${task.title}"?`)) return;
    setLoading(true);
    try {
      await onDelete(task.id);
    } finally {
      setLoading(false);
    }
  }

  async function handleSave() {
    const trimmed = editTitle.trim();
    if (!trimmed) return;

    setLoading(true);
    try {
      await onUpdate(task.id, trimmed, editDescription.trim() || undefined);
      setEditing(false);
    } finally {
      setLoading(false);
    }
  }

  function handleCancel() {
    setEditTitle(task.title);
    setEditDescription(task.description || "");
    setEditing(false);
  }

  if (editing) {
    return (
      <div className="bg-white border-2 border-blue-300/50 rounded-xl shadow-sm p-4">
        <input
          type="text"
          value={editTitle}
          onChange={(e) => setEditTitle(e.target.value)}
          className="w-full border border-gray-200 rounded-lg px-4 py-2.5 mb-2 focus:ring-2 focus:ring-blue-500/30 focus:border-blue-400 outline-none"
          maxLength={200}
          aria-label="Edit task title"
        />
        <textarea
          value={editDescription}
          onChange={(e) => setEditDescription(e.target.value)}
          className="w-full border border-gray-200 rounded-lg px-4 py-2.5 mb-3 focus:ring-2 focus:ring-blue-500/30 focus:border-blue-400 outline-none resize-none"
          rows={2}
          maxLength={1000}
          placeholder="Description (optional)"
          aria-label="Edit task description"
        />
        <div className="flex gap-2 justify-end">
          <button
            onClick={handleCancel}
            className="px-4 py-1.5 text-sm bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition-colors"
          >
            Cancel
          </button>
          <button
            onClick={handleSave}
            disabled={loading || !editTitle.trim()}
            className="px-4 py-1.5 text-sm bg-gradient-to-r from-blue-500 to-indigo-500 hover:from-blue-600 hover:to-indigo-600 text-white rounded-lg transition-all disabled:opacity-50"
          >
            {loading ? "Saving..." : "Save"}
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={`bg-white border border-gray-200/50 rounded-xl shadow-sm p-4 flex items-start gap-3 transition-all hover:shadow-md ${loading ? "opacity-50" : ""}`}>
      <button
        onClick={handleToggle}
        disabled={loading}
        className={`mt-0.5 flex-shrink-0 w-5 h-5 rounded-md border-2 flex items-center justify-center transition-all ${
          task.completed
            ? "bg-gradient-to-br from-blue-500 to-indigo-500 border-transparent"
            : "border-gray-300 hover:border-blue-400"
        }`}
        aria-label={task.completed ? "Mark as pending" : "Mark as completed"}
      >
        {task.completed && (
          <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
          </svg>
        )}
      </button>

      <div className="flex-1 min-w-0">
        <h3 className={`font-medium ${task.completed ? "line-through text-gray-400" : "text-gray-900"}`}>
          {task.title}
        </h3>
        {task.description && (
          <p className={`text-sm mt-1 ${task.completed ? "text-gray-300 line-through" : "text-gray-500"}`}>
            {task.description}
          </p>
        )}
        <p className="text-xs text-gray-400 mt-2">{date}</p>
      </div>

      <div className="flex gap-1 flex-shrink-0">
        <button
          onClick={() => setEditing(true)}
          disabled={loading}
          className="p-1.5 text-gray-400 hover:text-blue-600 transition-colors rounded-md hover:bg-blue-50"
          aria-label="Edit task"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
        </button>
        <button
          onClick={handleDelete}
          disabled={loading}
          className="p-1.5 text-gray-400 hover:text-red-600 transition-colors rounded-md hover:bg-red-50"
          aria-label="Delete task"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
        </button>
      </div>
    </div>
  );
}
