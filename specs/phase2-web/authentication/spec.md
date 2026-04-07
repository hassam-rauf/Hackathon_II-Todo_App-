# Authentication — Feature Spec

**Phase**: II — Cycle 3
**Tasks**: T-033 → T-041
**Skill**: auth-builder

---

## Objective

Add multi-user authentication to the Todo app using Better Auth (Next.js frontend) and JWT verification (FastAPI backend). Replace the hardcoded "demo-user" with real user identity.

## User Stories

1. **As a new user**, I can sign up with email, password, and name so I have my own account.
2. **As a returning user**, I can sign in with email and password to access my tasks.
3. **As an authenticated user**, my JWT token is sent with every API request so the backend knows who I am.
4. **As a user**, I cannot see or modify another user's tasks (user isolation).
5. **As an unauthenticated visitor**, I am redirected to /signin when trying to access the app.

## Key Entities

### User (managed by Better Auth)
| Field | Type | Constraint |
|-------|------|-----------|
| id | string | PK, auto-generated |
| email | string | unique, required |
| name | string | required |
| createdAt | timestamp | auto |

### JWT Token Payload
| Claim | Type | Description |
|-------|------|-------------|
| sub | string | User ID |
| email | string | User email |
| iat | number | Issued at |
| exp | number | Expiry |

## Auth Flow

```
User signup/signin → Better Auth validates → JWT issued →
Frontend stores session → Bearer token sent to FastAPI →
FastAPI middleware verifies JWT → Extracts user_id (sub) →
Route checks user_id matches URL param → Returns user's data only
```

## Error Matrix

| Scenario | Status | Detail |
|----------|--------|--------|
| No Authorization header | 401 | Not authenticated |
| Malformed token | 401 | Invalid token |
| Expired token | 401 | Token expired |
| Valid token, wrong user | 403 | Access denied |
| Signup duplicate email | 409 | Email already registered |
| Login wrong password | 401 | Invalid credentials |

## Acceptance Criteria

- [ ] User can sign up with email, password, name
- [ ] User can sign in with email, password
- [ ] JWT token sent as Authorization: Bearer header on all API calls
- [ ] FastAPI middleware validates JWT on every protected endpoint
- [ ] 401 for missing/invalid/expired tokens
- [ ] 403 when accessing another user's tasks
- [ ] Unauthenticated users redirected to /signin
- [ ] AUTH_SECRET shared between frontend and backend (env var, not hardcoded)
- [ ] "demo-user" hardcode removed from frontend
- [ ] All auth tests pass

## Non-Goals

- OAuth providers (Google, GitHub) — future enhancement
- Role-based access control — single role only
- Token refresh mechanism — session-based refresh via Better Auth
- Password reset flow
