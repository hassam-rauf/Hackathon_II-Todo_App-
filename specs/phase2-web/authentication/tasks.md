# Authentication — Tasks

**Phase**: II — Cycle 3
**Plan**: specs/phase2-web/authentication/plan.md

---

## Tasks

### T-033: Better Auth install + configure in Next.js
- [ ] Install `better-auth` and `pg` in frontend
- [ ] Create `frontend/lib/auth.ts` — server-side Better Auth config with emailAndPassword enabled
- [ ] Create `frontend/app/api/auth/[...all]/route.ts` — catchall auth API route
- [ ] Create `frontend/lib/auth-client.ts` — client-side auth hooks (signIn, signUp, signOut, useSession)
- **Test**: Auth API route responds at /api/auth

### T-034: JWT plugin enable in Better Auth config
- [ ] Add JWT plugin to server config (`better-auth/plugins`)
- [ ] Add jwtClient plugin to client config (`better-auth/client/plugins`)
- [ ] Configure HS256 signing with AUTH_SECRET
- **Test**: Token issued on signin contains sub, email, exp claims

### T-035: Signup page (/signup)
- [ ] Create `frontend/app/signup/page.tsx` with name, email, password fields
- [ ] Form validation (all required, password min 8 chars)
- [ ] Error display for duplicate email
- [ ] Redirect to / on success
- [ ] Link to /signin
- **Test**: Signup form renders, validates required fields

### T-036: Signin page (/signin)
- [ ] Create `frontend/app/signin/page.tsx` with email, password fields
- [ ] Error display for invalid credentials
- [ ] Redirect to / on success
- [ ] Link to /signup
- **Test**: Signin form renders, validates required fields

### T-037: JWT middleware in FastAPI
- [ ] Add `PyJWT` to `backend/pyproject.toml`
- [ ] Create `backend/auth.py` with `get_current_user` dependency
- [ ] Verify JWT using AUTH_SECRET with HS256
- [ ] Return 401 for missing/invalid/expired tokens
- [ ] Extract `sub` as user_id from payload
- **Test**: Valid token → user dict; expired → 401; invalid → 401; missing → 401

### T-038: Protected frontend routes
- [ ] Create `frontend/components/session-provider.tsx` — SessionProvider + useAuth hook
- [ ] Wrap app in SessionProvider via `frontend/app/layout.tsx`
- [ ] Update `frontend/app/page.tsx` — redirect to /signin if no session
- [ ] Replace hardcoded "demo-user" with `session.user.id`
- **Test**: Unauthenticated user sees signin, authenticated sees tasks

### T-039: User isolation (API filters by user_id from JWT)
- [ ] Add `Depends(get_current_user)` to all 6 task route handlers
- [ ] Verify `current_user["sub"] == user_id` in each handler, 403 if mismatch
- [ ] Update existing task tests to override `get_current_user` dependency
- **Test**: User A cannot access User B's tasks (403)

### T-040: Shared AUTH_SECRET in both .env files
- [ ] Add `AUTH_SECRET=<generated-32-char-key>` to `frontend/.env.local`
- [ ] Add `DATABASE_URL` to `frontend/.env.local` (for Better Auth DB)
- [ ] Create `backend/.env` with `AUTH_SECRET=<same-key>`
- [ ] Verify both services use same secret
- **Test**: Same AUTH_SECRET value in both env files

### T-041: Auth tests
- [ ] `tests/backend/test_auth.py` — JWT middleware tests (valid, expired, invalid, missing)
- [ ] Test protected endpoints return 401 without token
- [ ] Test user isolation returns 403 for wrong user
- [ ] Update `tests/backend/test_tasks_api.py` — add get_current_user override to fixtures
- **Test**: All auth + existing task tests pass
