"use client";

import { useEffect, useState } from "react";
import { usePathname } from "next/navigation";
import Link from "next/link";
import {
  Bell,
  ChevronRight,
  Home,
  LogOut,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import api, { ApiError } from "@/lib/api";

const LABEL_MAP: Record<string, string> = {
  dashboard: "Tableau de bord",
  buildings: "Immeubles",
  equipment: "Équipements",
  calendar: "Calendrier",
  documents: "Documents",
  new: "Nouvel équipement",
};

function buildBreadcrumbs(pathname: string) {
  const segments = pathname.split("/").filter(Boolean);
  const crumbs: { label: string; href: string }[] = [
    { label: "Accueil", href: "/dashboard" },
  ];

  let currentPath = "";
  for (const segment of segments) {
    currentPath += `/${segment}`;
    const label = LABEL_MAP[segment] || segment.replace(/-/g, " ");
    crumbs.push({
      label: label.charAt(0).toUpperCase() + label.slice(1),
      href: currentPath,
    });
  }

  return crumbs;
}

function getInitials(name: string): string {
  return name
    .split(" ")
    .map((w) => w.charAt(0).toUpperCase())
    .slice(0, 2)
    .join("");
}

interface UserProfile {
  id: number;
  email: string;
  full_name: string;
  company: string | null;
}

export default function Header() {
  const pathname = usePathname();
  const breadcrumbs = buildBreadcrumbs(pathname);
  const [scrolled, setScrolled] = useState(false);
  const [user, setUser] = useState<UserProfile | null>(null);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 0);
    window.addEventListener("scroll", onScroll, { passive: true });

    // Fetch user info
    api.get<UserProfile>("/auth/me").then(setUser).catch(() => {});

    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  const initials = user ? getInitials(user.full_name) : "??";
  const displayName = user?.full_name || "Mon compte";
  const displayEmail = user?.email || "";

  return (
    <header
      className={cn(
        "sticky top-0 z-30 flex h-16 items-center justify-between border-b bg-white px-6 transition-shadow duration-200",
        scrolled
          ? "border-border shadow-sm"
          : "border-transparent"
      )}
    >
      {/* Breadcrumb */}
      <nav className="flex items-center gap-1.5 text-sm">
        {breadcrumbs.map((crumb, i) => (
          <span key={crumb.href} className="flex items-center gap-1.5">
            {i > 0 && (
              <ChevronRight className="h-4 w-4 text-muted-foreground/50" />
            )}
            {i === 0 ? (
              <Link
                href={crumb.href}
                className="flex items-center gap-1 text-muted-foreground hover:text-primary transition-colors"
              >
                <Home className="h-4 w-4" />
              </Link>
            ) : i === breadcrumbs.length - 1 ? (
              <span className="font-medium text-card-foreground">{crumb.label}</span>
            ) : (
              <Link
                href={crumb.href}
                className="text-muted-foreground hover:text-primary transition-colors"
              >
                {crumb.label}
              </Link>
            )}
          </span>
        ))}
      </nav>

      {/* Right side */}
      <div className="flex items-center gap-3">
        {/* Notifications */}
        <Button
          variant="ghost"
          size="icon"
          className="relative h-9 w-9 text-muted-foreground hover:text-foreground"
        >
          <Bell className="h-5 w-5" />
          <span className="absolute -top-0.5 -right-0.5 flex h-4 w-4 items-center justify-center rounded-full bg-destructive text-[10px] font-bold text-white">
            3
          </span>
        </Button>

        {/* User menu */}
        <DropdownMenu>
          <DropdownMenuTrigger>
            <button className="flex items-center gap-2 rounded-full hover:bg-muted p-1 transition-colors">
              <Avatar className="h-8 w-8 border border-border">
                <AvatarFallback className="bg-accent text-primary text-xs font-medium">
                  {initials}
                </AvatarFallback>
              </Avatar>
            </button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" className="w-56">
            <DropdownMenuLabel>
              <div className="flex flex-col gap-0.5">
                <span className="truncate">{displayName}</span>
                {displayEmail && (
                  <span className="text-xs font-normal text-muted-foreground truncate">
                    {displayEmail}
                  </span>
                )}
              </div>
            </DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem
              className="cursor-pointer text-destructive"
              onClick={() => {
                localStorage.removeItem("token");
                window.location.href = "/login";
              }}
            >
              <LogOut className="mr-2 h-4 w-4" />
              Déconnexion
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </header>
  );
}
