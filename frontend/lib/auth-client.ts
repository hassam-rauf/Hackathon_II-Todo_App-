/**
 * Better Auth client-side hooks.
 * Tasks: T-033, T-034
 * Ref: specs/phase2-web/authentication/plan.md
 */

import { createAuthClient } from "better-auth/react";
import { jwtClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000",
  plugins: [jwtClient()],
});

export const { signIn, signUp, signOut, useSession, getSession } = authClient;
