# Authentication — Architecture Plan

**Phase**: II — Cycle 3
**Spec**: specs/phase2-web/authentication/spec.md

---

## Architecture Decision

**Better Auth + JWT for cross-service authentication.**

- Better Auth runs inside Next.js (server-side), manages users/sessions in Neon PostgreSQL
- JWT plugin issues signed tokens using shared AUTH_SECRET (HS256)
- FastAPI verifies JWT independently — no callback to auth server needed
- Stateless verification on backend = fast, scalable

## Component Map

```
frontend/
├── lib/auth.ts              ← Better Auth server config (NEW)
├── lib/auth-client.ts       ← Better Auth client hooks (NEW)
├── lib/api.ts               ← Add Bearer token to requests (MODIFY)
├── app/api/auth/[...all]/route.ts  ← Auth API catchall (NEW)
├── app/signin/page.tsx      ← Sign in form (NEW)
├── app/signup/page.tsx      ← Sign up form (NEW)
├── app/page.tsx             ← Replace demo-user with auth (MODIFY)
├── app/layout.tsx           ← Add SessionProvider (MODIFY)
└── components/session-provider.tsx  ← Auth context (NEW)

backend/
├── auth.py                  ← JWT verify + get_current_user (NEW)
├── routes/tasks.py          ← Add auth dependency (MODIFY)
└── pyproject.toml           ← Add PyJWT dependency (MODIFY)

tests/backend/
└── test_auth.py             ← Auth middleware + isolation tests (NEW)
```

## Data Flow

1. **Signup**: POST /api/auth/sign-up/email → Better Auth creates user in DB → returns session + JWT
2. **Signin**: POST /api/auth/sign-in/email → Better Auth validates → returns session + JWT
3. **API Call**: Frontend gets token from session → sends `Authorization: Bearer <token>` → FastAPI decodes JWT → extracts `sub` as user_id → checks URL user_id matches → returns data
4. **Protected Page**: useSession() hook checks auth state → no session = redirect to /signin

## Dependencies

**Frontend (npm)**:
- `better-auth` — auth framework
- `pg` — PostgreSQL driver for Better Auth

**Backend (uv)**:
- `PyJWT` — JWT decode/verify

## Security Constraints

- AUTH_SECRET from env var only, min 32 chars, same in both services
- HS256 algorithm for JWT signing
- Passwords hashed by Better Auth (bcrypt)
- No sensitive data in JWT payload beyond sub + email
- HTTPOnly cookies for session management
- Bearer token for cross-service API calls

## Testing Strategy

- **Unit**: JWT decode with valid/expired/invalid tokens (mock PyJWT)
- **Integration**: Protected endpoints return 401 without token, 403 for wrong user
- **Override pattern**: `app.dependency_overrides[get_current_user]` for existing task tests
