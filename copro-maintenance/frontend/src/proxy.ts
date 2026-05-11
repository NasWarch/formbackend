import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

/**
 * CoproMaintenance Proxy — JWT Authentication
 *
 * Protects dashboard and app routes. Redirects to /login if no token.
 * Uses the new proxy.js convention (Next.js 16 replaces middleware).
 */

// Routes that require authentication
const protectedPaths = ["/dashboard", "/immeubles", "/equipements", "/calendar", "/documents", "/settings"];

// Routes that should be inaccessible when authenticated
const authPaths = ["/login", "/register"];

export function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Check for JWT token in cookie or Authorization header
  const token =
    request.cookies.get("token")?.value ||
    request.headers.get("Authorization")?.replace("Bearer ", "") ||
    null;

  const isProtected = protectedPaths.some((path) =>
    pathname.startsWith(path)
  );
  const isAuthPage = authPaths.some((path) => pathname.startsWith(path));

  // Redirect unauthenticated users to login
  if (isProtected && !token) {
    const loginUrl = new URL("/login", request.url);
    loginUrl.searchParams.set("redirect", pathname);
    return NextResponse.redirect(loginUrl);
  }

  // Redirect authenticated users away from auth pages
  if (isAuthPage && token) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon)
     * - public files (images, etc.)
     */
    "/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)",
  ],
};
