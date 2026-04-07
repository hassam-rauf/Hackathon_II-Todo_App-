/**
 * Signin page — glassmorphism style.
 * Task: T-036
 */

"use client";

import { useState } from "react";
import Link from "next/link";
import { signIn } from "@/lib/auth-client";

export default function SignInPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const result = await signIn.email({ email, password });

      if (result.error) {
        setError(result.error.message ?? "Invalid credentials");
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
    <div className="min-h-screen bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-700 flex items-center justify-center px-4 relative overflow-hidden">
      {/* Decorative blobs */}
      <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-400/20 rounded-full blur-3xl" />
      <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-indigo-400/20 rounded-full blur-3xl" />

      <div className="w-full max-w-md relative z-10 animate-fade-in-scale">
        {/* Branding */}
        <div className="text-center mb-8">
          <Link href="/" className="inline-flex items-center gap-2 group">
            <div className="w-10 h-10 bg-white/20 backdrop-blur-sm rounded-xl flex items-center justify-center group-hover:bg-white/30 transition-colors">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <span className="text-2xl font-bold text-white">TodoApp</span>
          </Link>
          <p className="text-white/50 mt-2 text-sm">Welcome back</p>
        </div>

        {/* Glass Card */}
        <div className="bg-white/10 backdrop-blur-xl rounded-2xl border border-white/20 shadow-2xl p-8">
          <h2 className="text-2xl font-semibold text-white mb-6">Sign In</h2>

          {error && (
            <div className="bg-red-500/20 border border-red-400/30 rounded-lg px-4 py-3 mb-6" role="alert">
              <p className="text-red-200 text-sm">{error}</p>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-white/80 mb-2">
                Email
              </label>
              <input
                id="email"
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-white placeholder-white/40 focus:ring-2 focus:ring-white/30 focus:border-transparent outline-none transition-all"
                placeholder="you@example.com"
                aria-label="Email address"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-white/80 mb-2">
                Password
              </label>
              <input
                id="password"
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-white placeholder-white/40 focus:ring-2 focus:ring-white/30 focus:border-transparent outline-none transition-all"
                placeholder="Enter your password"
                aria-label="Password"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-white text-blue-700 font-semibold py-3 rounded-xl hover:bg-white/90 transition-all shadow-lg disabled:opacity-50 disabled:cursor-not-allowed mt-2"
              aria-label="Sign in"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <svg className="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                  </svg>
                  Signing in...
                </span>
              ) : (
                "Sign In"
              )}
            </button>
          </form>
        </div>

        {/* Link to signup */}
        <p className="text-white/50 text-center mt-6 text-sm">
          Don&apos;t have an account?{" "}
          <Link href="/signup" className="text-white font-medium hover:underline">
            Sign up
          </Link>
        </p>
      </div>
    </div>
  );
}
