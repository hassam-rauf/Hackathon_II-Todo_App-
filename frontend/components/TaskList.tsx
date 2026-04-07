/**
 * Task list — maps tasks array to TaskCard components.
 * Task: T-026
 */

"use client";

import type { Task } from "@/lib/api";
import TaskCard from "./TaskCard";
import EmptyState from "./EmptyState";

interface TaskListProps {
  tasks: Task[];
  onToggle: (taskId: number) => Promise<void>;
  onDelete: (taskId: number) => Promise<void>;
  onUpdate: (taskId: number, title: string, description?: string) => Promise<void>;
}

export default function TaskList({ tasks, onToggle, onDelete, onUpdate }: TaskListProps) {
  if (tasks.length === 0) {
    return <EmptyState />;
  }

  return (
    <div className="flex flex-col gap-3">
      {tasks.map((task) => (
        <TaskCard
          key={task.id}
          task={task}
          onToggle={onToggle}
          onDelete={onDelete}
          onUpdate={onUpdate}
        />
      ))}
    </div>
  );
}
