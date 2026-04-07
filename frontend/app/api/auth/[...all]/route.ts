/**
 * Better Auth catchall API route.
 * Task: T-033
 * Handles: /api/auth/sign-in, /api/auth/sign-up, /api/auth/session, etc.
 */

import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

export const { GET, POST } = toNextJsHandler(auth.handler);
