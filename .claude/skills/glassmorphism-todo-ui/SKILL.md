---
name: glassmorphism-todo-ui
description: |
  Build glassmorphism-styled Next.js pages and components with frosted glass cards,
  gradient backgrounds, and modern UI patterns.
  This skill should be used when users ask to create landing pages, auth pages,
  dashboards, or any UI with glassmorphism/frosted-glass aesthetic.
---

# Glassmorphism Todo UI Builder

Build production-grade glassmorphism interfaces for Next.js App Router.

## What This Skill Does
- Create pages with gradient backgrounds and frosted glass cards
- Build auth pages (signin/signup) with glassmorphism styling
- Build dashboards with stats overview cards
- Create public landing pages with hero sections and feature highlights
- Apply consistent blue-to-indigo color scheme

## What This Skill Does NOT Do
- Backend API development
- Authentication logic (use auth-builder)
- Database operations

---

## Before Implementation

| Source | Gather |
|--------|--------|
| **Codebase** | Existing components, Tailwind config, layout.tsx |
| **Conversation** | Which page, what data, what interactions |
| **Skill References** | `references/patterns.md` for glassmorphism tokens and layouts |
| **User Guidelines** | Constitution UI/UX principles |

---

## Design System

### Color Tokens
```
Primary gradient:  from-blue-600 via-blue-700 to-indigo-700
Accent gradient:   from-blue-500 to-indigo-500
Glass card:        bg-white/10 backdrop-blur-xl border border-white/20
Glass card light:  bg-white/80 backdrop-blur-xl border border-white/30
Solid card:        bg-white/90 backdrop-blur-sm border border-gray-200/50
Text on gradient:  text-white
Text on light:     text-gray-900
Muted text:        text-white/70 (on gradient), text-gray-500 (on light)
```

### Glass Card Pattern
```tsx
<div className="bg-white/10 backdrop-blur-xl rounded-2xl border border-white/20 shadow-2xl p-8">
  {/* content */}
</div>
```

### Gradient Background
```tsx
<div className="min-h-screen bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-700">
  {/* content on gradient */}
</div>
```

---

## Workflow

1. **Determine page type**: Landing, Auth, or Dashboard
2. **Apply gradient background** for auth/landing; light bg for dashboard
3. **Use glass cards** for content containers
4. **Add animations**: fade-in on mount, hover transforms on cards
5. **Ensure responsive**: mobile-first with Tailwind breakpoints
6. **ARIA labels** on all interactive elements

---

## Page Patterns

### Landing Page
- Full gradient background
- Navbar with logo + CTA
- Hero: headline + subtext + buttons
- Feature cards (3-column grid) with glass effect
- Footer

### Auth Pages (Signin/Signup)
- Full gradient background
- Centered glass card with form
- App branding above form
- Loading states on submit
- Links between signin/signup

### Dashboard
- Light background (gray-50/white)
- Colored header/navbar with user info
- Stats bar with metric cards
- Task management area with glass-style cards

---

## Output Checklist

- [ ] Gradient background applied correctly
- [ ] Glass cards use backdrop-blur-xl + border-white/20
- [ ] Mobile-first responsive (base → md → lg)
- [ ] ARIA labels on interactive elements
- [ ] Loading states for async operations
- [ ] Consistent color tokens from design system

---

## Reference Files

| File | When to Read |
|------|--------------|
| `references/patterns.md` | Component code patterns, Tailwind classes, layout examples |
