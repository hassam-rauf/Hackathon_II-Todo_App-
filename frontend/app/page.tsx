/**
 * Public landing page — space theme with galaxy background.
 * Hero with laptop mockup and green CTA.
 */

import Link from "next/link";

export default function LandingPage() {
  return (
    <div className="min-h-screen space-bg overflow-hidden relative">
      {/* Stars overlay */}
      <div className="fixed inset-0 stars pointer-events-none" />

      {/* Nebula glow effects */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden">
        <div className="absolute top-1/4 -left-20 w-96 h-96 bg-purple-600/10 rounded-full blur-[120px]" />
        <div className="absolute bottom-1/4 -right-20 w-96 h-96 bg-blue-600/10 rounded-full blur-[120px]" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-violet-900/5 rounded-full blur-[150px]" />
      </div>

      {/* Navbar */}
      <nav className="relative z-10 flex items-center justify-between px-6 py-5 max-w-6xl mx-auto animate-fade-in">
        <div className="flex items-center gap-2">
          <svg className="w-6 h-6 text-emerald-400" fill="currentColor" viewBox="0 0 24 24">
            <path d="M3 5a2 2 0 012-2h14a2 2 0 012 2v14a2 2 0 01-2 2H5a2 2 0 01-2-2V5zm6 7l2 2 4-4" />
            <path fill="none" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4" />
          </svg>
          <span className="text-xl font-bold text-white">ToDo</span>
        </div>
        <div className="flex items-center gap-3">
          <Link
            href="/signin"
            className="text-white/60 hover:text-white px-4 py-2 text-sm font-medium transition-colors"
          >
            Log In
          </Link>
          <Link
            href="/signup"
            className="bg-white/10 backdrop-blur-sm text-white border border-white/20 px-5 py-2 rounded-xl text-sm font-medium hover:bg-white/20 transition-all"
          >
            Sign Up
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative z-10 max-w-6xl mx-auto px-6 pt-16 pb-20 md:pt-24 md:pb-28">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          {/* Left — Text */}
          <div className="animate-fade-in">
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-white leading-tight">
              Organize your life.
              <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-300 to-blue-300">
                Focus on what matters.
              </span>
            </h1>
            <p className="text-lg text-white/40 mt-6 max-w-lg">
              Get done with our simple and effective to-do app.
            </p>

            <div className="mt-10 flex flex-col sm:flex-row gap-4">
              <Link
                href="/signup"
                className="bg-emerald-500 hover:bg-emerald-400 text-white px-8 py-3.5 rounded-xl font-semibold text-lg transition-all shadow-lg shadow-emerald-500/20 hover:shadow-emerald-400/30 hover:-translate-y-0.5 text-center"
              >
                Get Started &mdash; It&apos;s Free
              </Link>
            </div>
            <p className="text-white/30 text-sm mt-3">No credit card required</p>
          </div>

          {/* Right — Laptop Mockup */}
          <div className="animate-fade-in-delay-2 animate-float hidden md:block">
            <div className="relative">
              {/* Laptop frame */}
              <div className="bg-gray-900 rounded-2xl border border-white/10 shadow-2xl shadow-purple-900/20 overflow-hidden">
                {/* Toolbar */}
                <div className="flex items-center gap-2 px-4 py-3 bg-gray-800/80 border-b border-white/5">
                  <div className="flex gap-1.5">
                    <div className="w-3 h-3 rounded-full bg-red-500/80" />
                    <div className="w-3 h-3 rounded-full bg-yellow-500/80" />
                    <div className="w-3 h-3 rounded-full bg-green-500/80" />
                  </div>
                  <div className="flex-1 mx-8">
                    <div className="bg-gray-700/50 rounded-md px-3 py-1 text-xs text-white/30 text-center">
                      todoapp.vercel.app
                    </div>
                  </div>
                </div>

                {/* Mini dashboard preview */}
                <div className="p-4 space-y-3 bg-gradient-to-br from-gray-900 to-[#12082a]">
                  {/* Mini header */}
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <div className="w-7 h-7 rounded-full bg-gradient-to-br from-purple-500 to-blue-500" />
                      <div>
                        <p className="text-white text-xs font-medium">Welcome back, Alex!</p>
                        <p className="text-white/30 text-[10px]">Dashboard</p>
                      </div>
                    </div>
                    <div className="bg-emerald-500/20 text-emerald-400 text-[10px] px-2 py-1 rounded-md">+ New Task</div>
                  </div>

                  {/* Mini stats */}
                  <div className="grid grid-cols-3 gap-2">
                    <div className="glass-card p-2 text-center">
                      <p className="text-white/40 text-[9px]">Tasks</p>
                      <p className="text-white text-sm font-bold">5</p>
                    </div>
                    <div className="glass-card p-2 text-center">
                      <p className="text-white/40 text-[9px]">Due Soon</p>
                      <p className="text-amber-400 text-sm font-bold">2</p>
                    </div>
                    <div className="glass-card p-2 text-center">
                      <p className="text-white/40 text-[9px]">Done</p>
                      <p className="text-emerald-400 text-sm font-bold">12</p>
                    </div>
                  </div>

                  {/* Mini task list */}
                  <div className="space-y-1.5">
                    {["Finish project report", "Email design team", "Review pull requests"].map((t, i) => (
                      <div key={t} className="glass-card px-3 py-2 flex items-center gap-2">
                        <div className={`w-3 h-3 rounded border ${i === 2 ? "bg-emerald-500 border-emerald-500" : "border-white/20"}`} />
                        <span className={`text-[11px] ${i === 2 ? "text-white/30 line-through" : "text-white/70"}`}>{t}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
              {/* Laptop base */}
              <div className="mx-auto w-3/4 h-3 bg-gray-800 rounded-b-xl border-x border-b border-white/5" />
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="relative z-10 max-w-6xl mx-auto px-6 pb-20 md:pb-28">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[
            {
              icon: "M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z",
              title: "Task Management",
              desc: "Create, update, and organize your tasks with an intuitive interface.",
            },
            {
              icon: "M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z",
              title: "Secure & Private",
              desc: "JWT authentication and encrypted connections keep your data safe.",
            },
            {
              icon: "M13 10V3L4 14h7v7l9-11h-7z",
              title: "Lightning Fast",
              desc: "Built with Next.js and FastAPI for blazing performance.",
            },
          ].map((feature, i) => (
            <div
              key={feature.title}
              className={`glass-card glass-card-hover p-6 md:p-8 transition-all hover:-translate-y-1 animate-fade-in-delay-${i + 1}`}
            >
              <div className="w-12 h-12 bg-white/5 rounded-xl flex items-center justify-center text-purple-400 mb-4 border border-white/5">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d={feature.icon} />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-white mb-2">{feature.title}</h3>
              <p className="text-white/40 text-sm leading-relaxed">{feature.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="relative z-10 border-t border-white/5 py-8">
        <div className="max-w-6xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-white/20 text-sm">
            &copy; 2026 ToDo. Built with Next.js, FastAPI & Neon.
          </p>
          <div className="flex gap-6 text-sm text-white/20">
            <span>Phase II &mdash; Full-Stack Web App</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
