/**
 * Better Auth server-side configuration.
 * Tasks: T-033, T-034
 * Ref: specs/phase2-web/authentication/plan.md
 */

import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";
import { Pool } from "pg";

const pool = new Pool({
  connectionString: process.env.DATABASE_URL!,
  ssl: { rejectUnauthorized: false },
});

export const auth = betterAuth({
  baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000",
  secret: process.env.AUTH_SECRET,
  database: pool,
  emailAndPassword: {
    enabled: true,
    minPasswordLength: 8,
  },
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24,      // refresh daily
    cookieCache: {
      enabled: true,
      maxAge: 60 * 5, // 5 minutes
    },
  },
  plugins: [jwt()],
});
