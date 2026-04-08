/**
 * Tool call indicator chip — shows what the AI agent did.
 * Displays compact chips with per-tool icons and result summaries.
 *
 * Ref: specs/003-chatkit-frontend/plan.md — Component 7
 * Task: T006
 */

import type { ToolCall } from "@/lib/api";

interface ToolCallChipProps {
  toolCall: ToolCall;
}

function getToolDisplay(toolCall: ToolCall): { icon: string; label: string } {
  const result = toolCall.result as Record<string, unknown>;
  const args = toolCall.args as Record<string, unknown>;
  const status = result?.status as string | undefined;
  const isError = status === "error";

  if (isError) {
    const message = (result?.message as string) || "Unknown error";
    return { icon: "✗", label: `Failed: ${message}` };
  }

  switch (toolCall.tool) {
    case "add_task": {
      const title = (args?.title as string) || (result?.title as string) || "task";
      return { icon: "✓", label: `Added: ${title}` };
    }
    case "complete_task": {
      const title = (result?.title as string) || `task #${args?.task_id ?? ""}`;
      return { icon: "✓", label: `Completed: ${title}` };
    }
    case "delete_task": {
      const taskId = args?.task_id ?? "";
      return { icon: "🗑", label: `Deleted: task #${taskId}` };
    }
    case "update_task": {
      const title = (result?.title as string) || `task #${args?.task_id ?? ""}`;
      return { icon: "✏", label: `Updated: ${title}` };
    }
    case "list_tasks": {
      const tasks = result?.tasks;
      const count = Array.isArray(tasks) ? tasks.length : 0;
      return { icon: "📋", label: `Listed ${count} task${count !== 1 ? "s" : ""}` };
    }
    default:
      return { icon: "⚙", label: toolCall.tool };
  }
}

export default function ToolCallChip({ toolCall }: ToolCallChipProps) {
  const result = toolCall.result as Record<string, unknown>;
  const isError = (result?.status as string) === "error";
  const { icon, label } = getToolDisplay(toolCall);

  return (
    <span className={`tool-chip ${isError ? "tool-chip-error" : ""}`} aria-label={`Tool action: ${label}`}>
      <span>{icon}</span>
      <span>{label}</span>
    </span>
  );
}
