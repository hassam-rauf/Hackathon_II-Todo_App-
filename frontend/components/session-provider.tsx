/**
 * Session context provider for auth state.
 * Task: T-038
 * Ref: specs/phase2-web/authentication/plan.md — Frontend Auth
 */

"use client";

import { useSession } from "@/lib/auth-client";
import { createContext, useContext } from "react";

type SessionContextType = ReturnType<typeof useSession>;

const SessionContext = createContext<SessionContextType | null>(null);

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
