---
name: auth-builder
description: |
  Build authentication with Better Auth (frontend) and JWT verification (backend).
  This skill should be used when users ask to add login, signup, logout, session management,
  JWT tokens, protected routes, or auth middleware.
---

# Auth Builder

Build authentication layer with Better Auth + JWT for Next.js and FastAPI.

## What This Skill Does
- Set up Better Auth on Next.js frontend (signup, signin, signout)
- Configure JWT token generation and verification
- Create FastAPI auth middleware for protected endpoints
- Implement protected routes on frontend (redirect if not authenticated)
- Handle token refresh and session management
- Set up OAuth providers (optional)

## What This Skill Does NOT Do
- Database models (use database-sqlmodel-builder)
- API endpoints beyond auth (use fastapi-backend-builder)
- Frontend pages beyond auth forms (use frontend-ui-builder)

---

## Before Implementation

| Source | Gather |
|--------|--------|
| **Codebase** | Existing auth files, middleware, env vars |
| **Conversation** | What auth flow (email/password, OAuth), what to protect |
| **Skill References** | `references/patterns.md` for JWT flow and middleware patterns |
| **User Guidelines** | Constitution security principles |

---

## Required Clarifications

1. **Auth method**: "Email/password only, or also OAuth (Google, GitHub)?"
2. **What to protect**: "Which routes/endpoints need authentication?"
3. **Role-based**: "Single role or multiple roles (admin, user)?"

---

## Workflow

1. **Install Better Auth** — `npx @better-auth/cli init` on frontend
2. **Configure auth** — set up providers, JWT secret, token expiry
3. **Create auth pages** — signin, signup using Better Auth React hooks
4. **Backend middleware** — FastAPI dependency that verifies JWT from Authorization header
5. **Protect routes** — frontend (redirect) + backend (401/403)
6. **Test** — signup flow, signin, token verification, protected access, expired token

---

## Domain Standards

### Must Follow
- JWT secret from `AUTH_SECRET` environment variable (min 32 chars)
- Short-lived access tokens (15 min default)
- `Authorization: Bearer <token>` header convention
- HTTPException 401 for missing/invalid tokens
- HTTPException 403 for insufficient permissions
- Passwords never stored in plain text (Better Auth handles hashing)
- HTTPS only in production

### Must Avoid
- Storing JWT secret in code (use .env)
- Long-lived tokens without refresh mechanism
- Passing tokens in URL query parameters
- Custom password hashing (use Better Auth built-in)
- Disabling token expiry
- Storing sensitive user data in JWT payload

---

## Key Patterns

### Better Auth Setup (Frontend)
```typescript
// lib/auth.ts
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_AUTH_URL || "http://localhost:3000",
});

export const { signIn, signUp, signOut, useSession } = authClient;
```

### Sign In Page
```tsx
"use client";
import { useState } from "react";
import { signIn } from "@/lib/auth";

export default function SignInPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const result = await signIn.email({ email, password });
    if (result.error) setError(result.error.message);
  }

  return (
    <form onSubmit={handleSubmit} className="max-w-md mx-auto p-6">
      {error && <p className="text-red-600 text-sm mb-4">{error}</p>}
      <input type="email" value={email} onChange={e => setEmail(e.target.value)}
        className="w-full border rounded-lg px-3 py-2 mb-4" placeholder="Email" />
      <input type="password" value={password} onChange={e => setPassword(e.target.value)}
        className="w-full border rounded-lg px-3 py-2 mb-4" placeholder="Password" />
      <button type="submit"
        className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700">
        Sign In
      </button>
    </form>
  );
}
```

### FastAPI JWT Middleware
```python
import os
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()
AUTH_SECRET = os.getenv("AUTH_SECRET")

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """Verify JWT and return user payload."""
    try:
        payload = jwt.decode(
            credentials.credentials,
            AUTH_SECRET,
            algorithms=["HS256"],
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### Protected Route (Backend)
```python
@router.get("/{user_id}/tasks")
async def list_tasks(
    user_id: str,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user),
):
    if current_user["sub"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    stmt = select(Task).where(Task.user_id == user_id)
    return session.exec(stmt).all()
```

### Protected Route (Frontend)
```tsx
"use client";
import { useSession } from "@/lib/auth";
import { redirect } from "next/navigation";

export default function ProtectedPage() {
  const { data: session, isPending } = useSession();

  if (isPending) return <div>Loading...</div>;
  if (!session) redirect("/signin");

  return <div>Welcome, {session.user.email}</div>;
}
```

---

## Output Checklist

- [ ] Better Auth configured with AUTH_SECRET from env
- [ ] Sign in and sign up pages functional
- [ ] JWT middleware verifies token on every protected endpoint
- [ ] 401 for missing/expired tokens, 403 for wrong user
- [ ] No secrets hardcoded
- [ ] Token passed via Authorization header only
- [ ] Protected frontend routes redirect to signin

---

## Reference Files

| File | When to Read |
|------|--------------|
| `references/patterns.md` | JWT flow, middleware patterns, Better Auth config |
