/**
 * Global loading skeleton — space theme.
 * Task: T-031
 */

export default function Loading() {
  return (
    <div className="min-h-screen space-bg flex items-center justify-center">
      <div className="animate-spin h-8 w-8 border-4 border-purple-500 border-t-transparent rounded-full" />
    </div>
  );
}
