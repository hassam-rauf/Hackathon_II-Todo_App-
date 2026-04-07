# Frontend — Claude Code Instructions

## Stack
- Next.js 16+ (App Router), TypeScript, Tailwind CSS

## Conventions
- Server components by default; `"use client"` only for interactivity
- Tailwind CSS only — no inline styles, no CSS modules
- Mobile-first responsive: base → sm → md → lg
- ARIA labels on all interactive elements
- API calls through `lib/api.ts` only
- Components in `components/`, pages in `app/`

## Running
```bash
cd frontend && npm run dev  # localhost:3000
```

## Environment
- `NEXT_PUBLIC_API_URL` — backend URL (default: http://localhost:8000)
