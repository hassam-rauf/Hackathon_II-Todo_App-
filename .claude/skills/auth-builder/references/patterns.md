# Auth Patterns Reference

## Authentication Flow

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│  Next.js     │    │ Better Auth  │    │  FastAPI     │
│  Frontend    │───▶│  (Auth API)  │───▶│  Backend     │
│              │    │              │    │              │
│ signIn()     │    │ /api/auth/*  │    │ JWT verify   │
│ signUp()     │    │ JWT issue    │    │ get_current_ │
│ useSession() │    │ session mgmt │    │ user()       │
└─────────────┘    └──────────────┘    └─────────────┘
```

### Flow Steps
1. User submits email/password on frontend
2. Better Auth validates credentials, issues JWT
3. Frontend stores token (httpOnly cookie or memory)
4. Frontend sends `Authorization: Bearer <token>` to FastAPI
5. FastAPI middleware decodes JWT, extracts user_id
6. Route handler checks user_id matches resource owner

## Better Auth Configuration

### Installation
```bash
# In frontend directory
npx @better-auth/cli@latest init
npm install better-auth
```

### Server Config (app/api/auth/[...all]/route.ts)
```typescript
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  secret: process.env.AUTH_SECRET,
  database: {
    url: process.env.DATABASE_URL,
    type: "postgres",
  },
  emailAndPassword: {
    enabled: true,
    minPasswordLength: 8,
  },
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24,      // refresh daily
  },
});

// Export route handlers
export const { GET, POST } = auth.handler;
```

### Client Config (lib/auth-client.ts)
```typescript
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000",
});

export const {
  signIn,
  signUp,
  signOut,
  useSession,
  getSession,
} = authClient;
```

## JWT Patterns

### Token Structure
```json
{
  "sub": "user_123",          // user ID
  "email": "user@example.com",
  "iat": 1711900000,          // issued at
  "exp": 1711900900           // expires (15 min)
}
```

### Backend Verification
```python
import os
import jwt
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()
AUTH_SECRET = os.getenv("AUTH_SECRET")

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
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

### Ownership Check Pattern
```python
def verify_ownership(current_user: dict, resource_user_id: str):
    """Ensure the authenticated user owns the resource."""
    if current_user["sub"] != resource_user_id:
        raise HTTPException(status_code=403, detail="Access denied")
```

## Frontend Auth Patterns

### Auth Context Provider (layout.tsx)
```tsx
// app/layout.tsx
import { SessionProvider } from "@/components/session-provider";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <SessionProvider>{children}</SessionProvider>
      </body>
    </html>
  );
}
```

### Session Provider Component
```tsx
"use client";
import { useSession } from "@/lib/auth-client";
import { createContext, useContext } from "react";

const SessionContext = createContext<ReturnType<typeof useSession> | null>(null);

export function SessionProvider({ children }: { children: React.ReactNode }) {
  const session = useSession();
  return (
    <SessionContext.Provider value={session}>
      {children}
    </SessionContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(SessionContext);
  if (!ctx) throw new Error("useAuth must be used within SessionProvider");
  return ctx;
}
```

### Protected Route Wrapper
```tsx
"use client";
import { useAuth } from "@/components/session-provider";
import { redirect } from "next/navigation";

export default function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { data: session, isPending } = useAuth();

  if (isPending) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin h-8 w-8 border-4 border-blue-600 border-t-transparent rounded-full" />
      </div>
    );
  }

  if (!session) {
    redirect("/signin");
  }

  return <>{children}</>;
}
```

### API Call with Token
```typescript
// lib/api.ts
import { getSession } from "@/lib/auth-client";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function apiRequest(path: string, options: RequestInit = {}) {
  const session = await getSession();
  if (!session?.token) throw new Error("Not authenticated");

  const res = await fetch(`${API}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${session.token}`,
      ...options.headers,
    },
  });

  if (res.status === 401) {
    window.location.href = "/signin";
    throw new Error("Session expired");
  }

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(err.detail);
  }

  return res.json();
}
```

## Environment Variables

### Frontend (.env.local)
```env
AUTH_SECRET=your-secret-key-min-32-chars-long-here
DATABASE_URL=postgresql://user:pass@ep-xxx.neon.tech/db?sslmode=require
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend (.env)
```env
AUTH_SECRET=your-secret-key-min-32-chars-long-here  # same key as frontend
DATABASE_URL=postgresql://user:pass@ep-xxx.neon.tech/db?sslmode=require
```

## Error Handling Matrix

| Scenario | Status | Detail |
|----------|--------|--------|
| No Authorization header | 401 | "Not authenticated" |
| Malformed token | 401 | "Invalid token" |
| Expired token | 401 | "Token expired" |
| Valid token, wrong user | 403 | "Access denied" |
| Valid token, correct user | 200 | (proceed) |
| Signup duplicate email | 409 | "Email already registered" |
| Login wrong password | 401 | "Invalid credentials" |

## Testing Auth

### Mock Auth Dependency (pytest)
```python
import pytest
from fastapi.testclient import TestClient

def mock_current_user():
    return {"sub": "test-user-1", "email": "test@example.com"}

@pytest.fixture
def client(app):
    app.dependency_overrides[get_current_user] = mock_current_user
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
```
