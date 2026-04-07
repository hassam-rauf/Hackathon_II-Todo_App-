/**
 * Stats overview bar — total, completed, pending, progress rate.
 */

import type { Task } from "@/lib/api";

interface StatsBarProps {
  tasks: Task[];
}

export default function StatsBar({ tasks }: StatsBarProps) {
  const total = tasks.length;
  const completed = tasks.filter((t) => t.completed).length;
  const pending = total - completed;
  const rate = total > 0 ? Math.round((completed / total) * 100) : 0;

  const stats = [
    { label: "Total Tasks", value: total, bg: "bg-white", text: "text-gray-900", sub: "text-gray-500" },
    { label: "Completed", value: completed, bg: "bg-gradient-to-br from-emerald-50 to-green-50 border-emerald-200/50", text: "text-emerald-700", sub: "text-emerald-600" },
    { label: "Pending", value: pending, bg: "bg-gradient-to-br from-amber-50 to-orange-50 border-amber-200/50", text: "text-amber-700", sub: "text-amber-600" },
    { label: "Progress", value: `${rate}%`, bg: "bg-gradient-to-br from-blue-50 to-indigo-50 border-blue-200/50", text: "text-blue-700", sub: "text-blue-600" },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {stats.map((stat) => (
        <div
          key={stat.label}
          className={`${stat.bg} rounded-xl shadow-sm border border-gray-200/50 p-4 transition-transform hover:-translate-y-0.5`}
        >
          <p className={`text-xs font-medium ${stat.sub} uppercase tracking-wide`}>{stat.label}</p>
          <p className={`text-2xl font-bold ${stat.text} mt-1`}>{stat.value}</p>
        </div>
      ))}
    </div>
  );
}
