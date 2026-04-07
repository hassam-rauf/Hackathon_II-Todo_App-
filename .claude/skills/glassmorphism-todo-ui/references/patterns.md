# Glassmorphism UI Patterns

## Core Tailwind Classes

### Gradient Backgrounds
```
Full page:     min-h-screen bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-700
Subtle:        bg-gradient-to-br from-gray-50 to-blue-50
Button:        bg-gradient-to-r from-blue-500 to-indigo-500 hover:from-blue-600 hover:to-indigo-600
```

### Glass Cards
```
Dark glass:    bg-white/10 backdrop-blur-xl rounded-2xl border border-white/20 shadow-2xl
Light glass:   bg-white/80 backdrop-blur-xl rounded-2xl border border-white/30 shadow-xl
Solid card:    bg-white rounded-xl border border-gray-200/50 shadow-sm
Stats card:    bg-gradient-to-br from-blue-500/10 to-indigo-500/10 rounded-xl border border-blue-200/30 p-4
```

### Form Inputs (on glass)
```
bg-white/20 border border-white/30 rounded-lg px-4 py-3 text-white placeholder-white/50
focus:ring-2 focus:ring-white/40 focus:border-transparent outline-none
```

### Form Inputs (on light bg)
```
bg-white border border-gray-200 rounded-lg px-4 py-3 text-gray-900
focus:ring-2 focus:ring-blue-500/40 focus:border-blue-400 outline-none
```

### Buttons
```
Primary:   bg-white text-blue-700 font-semibold px-6 py-3 rounded-xl hover:bg-white/90 transition-all shadow-lg
Secondary: bg-white/20 text-white border border-white/30 px-6 py-3 rounded-xl hover:bg-white/30 transition-all
Gradient:  bg-gradient-to-r from-blue-500 to-indigo-500 text-white px-6 py-3 rounded-xl hover:shadow-lg transition-all
```

---

## Animation Classes

```css
/* Fade-in on mount */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in { animation: fadeIn 0.5s ease-out; }

/* Stagger children */
.animate-fade-in-delay-1 { animation: fadeIn 0.5s ease-out 0.1s both; }
.animate-fade-in-delay-2 { animation: fadeIn 0.5s ease-out 0.2s both; }
.animate-fade-in-delay-3 { animation: fadeIn 0.5s ease-out 0.3s both; }
```

---

## Layout: Landing Page

```tsx
<div className="min-h-screen bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-700">
  {/* Navbar */}
  <nav className="flex items-center justify-between px-6 py-4 max-w-6xl mx-auto">
    <span className="text-xl font-bold text-white">TodoApp</span>
    <Link href="/signin" className="bg-white/20 text-white px-4 py-2 rounded-lg">
      Sign In
    </Link>
  </nav>

  {/* Hero */}
  <section className="max-w-4xl mx-auto text-center px-6 py-20">
    <h1 className="text-4xl md:text-6xl font-bold text-white mb-6">...</h1>
    <p className="text-xl text-white/70 mb-8">...</p>
    <div className="flex gap-4 justify-center">
      <Link href="/signup" className="bg-white text-blue-700 px-8 py-3 rounded-xl font-semibold">
        Get Started
      </Link>
    </div>
  </section>

  {/* Features - 3 column */}
  <section className="max-w-6xl mx-auto px-6 pb-20 grid grid-cols-1 md:grid-cols-3 gap-6">
    <div className="bg-white/10 backdrop-blur-xl rounded-2xl border border-white/20 p-6">
      ...
    </div>
  </section>
</div>
```

---

## Layout: Auth Page (Signin/Signup)

```tsx
<div className="min-h-screen bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-700 flex items-center justify-center px-4">
  <div className="w-full max-w-md">
    {/* Logo */}
    <div className="text-center mb-8">
      <h1 className="text-3xl font-bold text-white">TodoApp</h1>
      <p className="text-white/60 mt-2">tagline</p>
    </div>

    {/* Glass Form Card */}
    <div className="bg-white/10 backdrop-blur-xl rounded-2xl border border-white/20 shadow-2xl p-8">
      <h2 className="text-2xl font-semibold text-white mb-6">Sign In</h2>
      <form>
        <input className="w-full bg-white/20 border border-white/30 rounded-lg px-4 py-3 text-white placeholder-white/50" />
        <button className="w-full bg-white text-blue-700 font-semibold py-3 rounded-xl">
          Sign In
        </button>
      </form>
    </div>

    {/* Link to other page */}
    <p className="text-white/60 text-center mt-6">
      Don't have an account? <Link className="text-white underline">Sign up</Link>
    </p>
  </div>
</div>
```

---

## Layout: Dashboard

```tsx
<div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
  {/* Header */}
  <header className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white">
    <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
      <div>
        <h1 className="text-lg font-semibold">TodoApp</h1>
        <p className="text-sm text-white/70">Welcome, {name}</p>
      </div>
      <button className="bg-white/20 px-4 py-2 rounded-lg text-sm">Sign Out</button>
    </div>
  </header>

  {/* Stats Bar */}
  <div className="max-w-5xl mx-auto px-6 -mt-6">
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div className="bg-white rounded-xl shadow-sm border border-gray-200/50 p-4">
        <p className="text-sm text-gray-500">Total</p>
        <p className="text-2xl font-bold text-gray-900">{count}</p>
      </div>
    </div>
  </div>

  {/* Task Area */}
  <main className="max-w-5xl mx-auto px-6 py-8">
    <TaskForm />
    <TaskList />
  </main>
</div>
```

---

## Stats Card Variants

```tsx
// Total Tasks
<div className="bg-white rounded-xl shadow-sm border border-gray-200/50 p-4">
  <p className="text-sm text-gray-500">Total Tasks</p>
  <p className="text-2xl font-bold text-gray-900">{total}</p>
</div>

// Completed (green accent)
<div className="bg-gradient-to-br from-emerald-50 to-green-50 rounded-xl border border-emerald-200/50 p-4">
  <p className="text-sm text-emerald-600">Completed</p>
  <p className="text-2xl font-bold text-emerald-700">{completed}</p>
</div>

// Pending (amber accent)
<div className="bg-gradient-to-br from-amber-50 to-orange-50 rounded-xl border border-amber-200/50 p-4">
  <p className="text-sm text-amber-600">Pending</p>
  <p className="text-2xl font-bold text-amber-700">{pending}</p>
</div>

// Completion Rate (blue accent)
<div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl border border-blue-200/50 p-4">
  <p className="text-sm text-blue-600">Progress</p>
  <p className="text-2xl font-bold text-blue-700">{rate}%</p>
</div>
```
