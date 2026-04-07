/**
 * Public landing page — hero, features, CTA.
 * Glassmorphism design with blue-to-indigo gradient.
 */

import Link from "next/link";

const features = [
  {
    icon: (
      <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    ),
    title: "Task Management",
    description: "Create, update, and organize your tasks with an intuitive interface. Mark complete, edit inline, and stay productive.",
  },
  {
    icon: (
      <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
      </svg>
    ),
    title: "Secure & Private",
    description: "Your data is protected with JWT authentication and encrypted connections. Only you can access your tasks.",
  },
  {
    icon: (
      <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13 10V3L4 14h7v7l9-11h-7z" />
      </svg>
    ),
    title: "Lightning Fast",
    description: "Built with Next.js and FastAPI for blazing performance. Optimistic updates mean zero waiting.",
  },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-700 overflow-hidden">
      {/* Decorative blobs */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-blue-400/20 rounded-full blur-3xl" />
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-indigo-400/20 rounded-full blur-3xl" />
      </div>

      {/* Navbar */}
      <nav className="relative z-10 flex items-center justify-between px-6 py-5 max-w-6xl mx-auto animate-fade-in">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-white/20 backdrop-blur-sm rounded-lg flex items-center justify-center">
            <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <span className="text-xl font-bold text-white">TodoApp</span>
        </div>
        <div className="flex items-center gap-3">
          <Link
            href="/signin"
            className="text-white/80 hover:text-white px-4 py-2 text-sm font-medium transition-colors"
          >
            Sign In
          </Link>
          <Link
            href="/signup"
            className="bg-white text-blue-700 px-5 py-2 rounded-xl text-sm font-semibold hover:bg-white/90 transition-all shadow-lg shadow-black/10"
          >
            Get Started
          </Link>
        </div>
      </nav>

      {/* Hero */}
      <section className="relative z-10 max-w-4xl mx-auto text-center px-6 pt-16 pb-20 md:pt-24 md:pb-28">
        <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-white leading-tight animate-fade-in">
          Manage Your Tasks
          <br />
          <span className="text-white/80">Like Never Before</span>
        </h1>
        <p className="text-lg md:text-xl text-white/60 mt-6 max-w-2xl mx-auto animate-fade-in-delay-1">
          A modern, secure task manager built with Next.js and FastAPI.
          Stay organized, track progress, and get things done.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center mt-10 animate-fade-in-delay-2">
          <Link
            href="/signup"
            className="bg-white text-blue-700 px-8 py-3.5 rounded-xl font-semibold text-lg hover:bg-white/90 transition-all shadow-xl shadow-black/10 hover:shadow-2xl hover:-translate-y-0.5"
          >
            Get Started Free
          </Link>
          <Link
            href="/signin"
            className="bg-white/10 backdrop-blur-sm text-white border border-white/20 px-8 py-3.5 rounded-xl font-semibold text-lg hover:bg-white/20 transition-all"
          >
            Sign In
          </Link>
        </div>
      </section>

      {/* Features */}
      <section className="relative z-10 max-w-6xl mx-auto px-6 pb-20 md:pb-28">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {features.map((feature, i) => (
            <div
              key={feature.title}
              className={`bg-white/10 backdrop-blur-xl rounded-2xl border border-white/20 p-6 md:p-8 hover:bg-white/15 transition-all hover:-translate-y-1 animate-fade-in-delay-${i + 1}`}
            >
              <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center text-white mb-4">
                {feature.icon}
              </div>
              <h3 className="text-lg font-semibold text-white mb-2">{feature.title}</h3>
              <p className="text-white/60 text-sm leading-relaxed">{feature.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="relative z-10 border-t border-white/10 py-8">
        <div className="max-w-6xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-white/40 text-sm">
            &copy; 2026 TodoApp. Built with Next.js, FastAPI & Neon.
          </p>
          <div className="flex gap-6 text-sm text-white/40">
            <span>Phase II — Full-Stack Web App</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
