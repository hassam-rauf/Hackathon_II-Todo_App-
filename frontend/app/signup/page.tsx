/**
 * Signup page — dark space theme.
 * Task: T-035
 */

"use client";

import { useState } from "react";
import Link from "next/link";
import { signUp } from "@/lib/auth-client";

export default function SignUpPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const result = await signUp.email({ name, email, password });

      if (result.error) {
        setError(result.error.message ?? "Signup failed");
      } else {
        window.location.href = "/dashboard";
      }
    } catch {
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen space-bg flex items-center justify-center px-4 relative overflow-hidden">
      {/* Stars */}
      <div className="fixed inset-0 stars pointer-events-none" />

      {/* Nebula glows */}
      <div className="absolute top-1/4 -left-40 w-80 h-80 bg-purple-600/10 rounded-full blur-[120px]" />
      <div className="absolute bottom-1/4 -right-40 w-80 h-80 bg-blue-600/10 rounded-full blur-[120px]" />

      <div className="w-full max-w-md relative z-10 animate-fade-in-scale">
        {/* Branding */}
        <div className="text-center mb-8">
          <Link href="/" className="inline-flex items-center gap-2 group">
            <svg className="w-7 h-7 text-emerald-400" fill="currentColor" viewBox="0 0 24 24">
              <path d="M3 5a2 2 0 012-2h14a2 2 0 012 2v14a2 2 0 01-2 2H5a2 2 0 01-2-2V5zm6 7l2 2 4-4" />
              <path fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4" />
            </svg>
            <span className="text-2xl font-bold text-white">ToDo</span>
          </Link>
          <p className="text-white/30 mt-2 text-sm">Create your account</p>
        </div>

        {/* Glass Card */}
        <div className="glass-card shadow-2xl p-8">
          <h2 className="text-2xl font-semibold text-white mb-6">Sign Up</h2>

          {error && (
            <div className="bg-red-500/10 border border-red-500/20 rounded-lg px-4 py-3 mb-6" role="alert">
              <p className="text-red-400 text-sm">{error}</p>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-white/50 mb-2">
                Name
              </label>
              <input
                id="name"
                type="text"
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="glass-input w-full px-4 py-3"
                placeholder="Your name"
                aria-label="Full name"
              />
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-white/50 mb-2">
                Email
              </label>
              <input
                id="email"
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="glass-input w-full px-4 py-3"
                placeholder="you@example.com"
                aria-label="Email address"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-white/50 mb-2">
                Password
              </label>
              <input
                id="password"
                type="password"
                required
                minLength={8}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="glass-input w-full px-4 py-3"
                placeholder="Min 8 characters"
                aria-label="Password"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-emerald-500 hover:bg-emerald-400 text-white font-semibold py-3 rounded-xl transition-all shadow-lg shadow-emerald-500/15 disabled:opacity-50 disabled:cursor-not-allowed mt-2"
              aria-label="Sign up"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <svg className="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                  </svg>
                  Creating account...
                </span>
              ) : (
                "Create Account"
              )}
            </button>
          </form>
        </div>

        <p className="text-white/30 text-center mt-6 text-sm">
          Already have an account?{" "}
          <Link href="/signin" className="text-purple-400 font-medium hover:text-purple-300 transition-colors">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}
