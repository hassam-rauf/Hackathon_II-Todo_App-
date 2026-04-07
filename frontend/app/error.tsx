/**
 * Global error boundary.
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
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 px-4">
      <h2 className="text-xl font-bold text-gray-900 mb-2">Something went wrong</h2>
      <p className="text-gray-600 mb-4">{error.message}</p>
      <button
        onClick={reset}
        className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
      >
        Try again
      </button>
    </div>
  );
}
