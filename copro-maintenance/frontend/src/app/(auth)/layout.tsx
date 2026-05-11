import type { ReactNode } from "react";
import { Building2 } from "lucide-react";
import Link from "next/link";

export default function AuthLayout({ children }: { children: ReactNode }) {
  return (
    <div className="flex min-h-screen flex-col bg-muted/30">
      {/* Minimal header for auth pages */}
      <div className="flex h-16 items-center justify-center border-b border-border bg-white">
        <Link href="/" className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary text-primary-foreground">
            <Building2 className="h-4 w-4" />
          </div>
          <span className="text-lg font-semibold tracking-tight text-foreground">
            CoproMaintenance
          </span>
        </Link>
      </div>

      {/* Centered content */}
      <div className="flex flex-1 items-center justify-center px-4 py-12 sm:px-6 lg:px-8">
        <div className="w-full max-w-md">{children}</div>
      </div>

      {/* Footer */}
      <div className="border-t border-border bg-white py-4 text-center text-xs text-muted-foreground">
        © {new Date().getFullYear()} CoproMaintenance ·{" "}
        <Link href="/" className="text-primary hover:underline">
          Retour à l&apos;accueil
        </Link>
      </div>
    </div>
  );
}
