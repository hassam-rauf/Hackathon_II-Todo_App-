/**
 * Stats overview bar — dark glass cards for dashboard.
 */

import type { Task } from "@/lib/api";

interface StatsBarProps {
  tasks: Task[];
}

export default function StatsBar({ tasks }: StatsBarProps) {
  const total = tasks.length;
  const completed = tasks.filter((t) => t.completed).length;
  const pending = total - completed;

  const stats = [
    {
      label: "Today's Tasks",
      value: total,
      color: "text-white",
      icon: (
        <svg className="w-5 h-5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
        </svg>
      ),
    },
    {
      label: "Due Soon",
      value: pending,
      color: "text-amber-400",
      icon: (
        <svg className="w-5 h-5 text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      ),
    },
    {
      label: "Completed",
      value: completed,
      color: "text-emerald-400",
      icon: (
        <svg className="w-5 h-5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      ),
    },
  ];

  return (
    <div className="grid grid-cols-3 gap-4">
      {stats.map((stat) => (
        <div
          key={stat.label}
          className="glass-card p-4 transition-transform hover:-translate-y-0.5"
        >
          <div className="flex items-center gap-3">
            <div className="bg-white/5 rounded-lg p-2">
              {stat.icon}
            </div>
            <div>
              <p className="text-white/40 text-xs font-medium">{stat.label}</p>
              <p className={`text-2xl font-bold ${stat.color} mt-0.5`}>{stat.value}</p>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
