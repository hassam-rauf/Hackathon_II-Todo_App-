/**
 * Global error boundary — space theme.
 * Task: T-031
 */

"use client";

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen space-bg px-4">
      <div className="fixed inset-0 stars pointer-events-none" />
      <div className="relative z-10 text-center">
        <h2 className="text-xl font-bold text-white mb-2">Something went wrong</h2>
        <p className="text-white/40 mb-4">{error.message}</p>
        <button
          onClick={reset}
          className="px-4 py-2 bg-purple-500/20 hover:bg-purple-500/30 text-purple-300 rounded-lg transition-colors border border-purple-500/20"
        >
          Try again
        </button>
      </div>
    </div>
  );
}
