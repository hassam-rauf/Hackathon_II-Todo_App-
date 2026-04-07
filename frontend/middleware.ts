/**
 * Auth middleware — protect /dashboard, redirect logic.
 * Uses Better Auth session cookie to check auth state.
 */

import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Better Auth stores session in a cookie named "better-auth.session_token"
  const sessionToken =
    request.cookies.get("better-auth.session_token")?.value ||
    request.cookies.get("__Secure-better-auth.session_token")?.value;

  const isAuthenticated = !!sessionToken;

  // Protected routes: redirect to signin if not authenticated
  if (pathname.startsWith("/dashboard") && !isAuthenticated) {
    return NextResponse.redirect(new URL("/signin", request.url));
  }

  // Auth pages: redirect to dashboard if already authenticated
  if ((pathname === "/signin" || pathname === "/signup") && isAuthenticated) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*", "/signin", "/signup"],
};
