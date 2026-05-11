"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import {
  LayoutDashboard,
  Building2,
  Wrench,
  Calendar,
  FileText,
  LogOut,
  User,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import api from "@/lib/api";

const NAV_ITEMS = [
  {
    href: "/dashboard",
    label: "Dashboard",
    icon: LayoutDashboard,
  },
  {
    href: "/dashboard/buildings",
    label: "Immeubles",
    icon: Building2,
  },
  {
    href: "/dashboard/equipment",
    label: "Équipements",
    icon: Wrench,
  },
  {
    href: "/dashboard/calendar",
    label: "Calendrier",
    icon: Calendar,
  },
  {
    href: "/dashboard/documents",
    label: "Documents",
    icon: FileText,
  },
];

interface UserProfile {
  id: number;
  email: string;
  full_name: string;
  company: string | null;
}

function getInitials(name: string): string {
  return name
    .split(" ")
    .map((w) => w.charAt(0).toUpperCase())
    .slice(0, 2)
    .join("");
}

export default function Sidebar() {
  const pathname = usePathname();
  const [user, setUser] = useState<UserProfile | null>(null);

  useEffect(() => {
    api.get<UserProfile>("/auth/me").then(setUser).catch(() => {});
  }, []);

  function isActive(href: string) {
    if (href === "/dashboard") return pathname === "/dashboard";
    return pathname.startsWith(href);
  }

  const navContainer = {
    hidden: {},
    show: { transition: { staggerChildren: 0.05 } },
  };
  const navItem = {
    hidden: { opacity: 0, x: -12 },
    show: { opacity: 1, x: 0 },
  };

  const initials = user ? getInitials(user.full_name) : "";
  const displayName = user?.full_name || "Mon Compte";
  const displayRole = user?.company || (user ? "Syndic" : "");

  return (
    <aside className="flex h-full w-64 flex-col border-r border-border bg-muted">
      {/* Logo */}
      <div className="flex h-16 items-center gap-3 border-b border-border px-6">
        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary text-primary-foreground">
          <Building2 className="h-5 w-5" />
        </div>
        <span className="text-lg font-semibold tracking-tight text-card-foreground">
          CoproMaintenance
        </span>
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-1 px-3 py-4">
        <motion.div
          variants={navContainer}
          initial="hidden"
          animate="show"
          className="space-y-1"
        >
          {NAV_ITEMS.map((item) => {
            const active = isActive(item.href);
            return (
              <motion.div key={item.href} variants={navItem}>
                <Tooltip>
                  <TooltipTrigger>
                    <Link
                      href={item.href}
                      className={cn(
                        "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors",
                        active
                          ? "bg-accent text-accent-foreground"
                          : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
                      )}
                    >
                      <item.icon
                        className={cn(
                          "h-5 w-5",
                          active ? "text-primary" : "text-muted-foreground"
                        )}
                      />
                      {item.label}
                    </Link>
                  </TooltipTrigger>
                  <TooltipContent side="right">{item.label}</TooltipContent>
                </Tooltip>
              </motion.div>
            );
          })}
        </motion.div>
      </nav>

      {/* User info */}
      <div className="border-t border-border p-4">
        <div className="flex items-center gap-3">
          <Avatar className="h-9 w-9 border border-border">
            <AvatarFallback className="bg-accent text-primary text-sm font-medium">
              {initials || <User className="h-4 w-4" />}
            </AvatarFallback>
          </Avatar>
          <div className="flex-1 min-w-0">
            <p className="truncate text-sm font-medium text-card-foreground">
              {displayName}
            </p>
            {displayRole && (
              <p className="truncate text-xs text-muted-foreground">{displayRole}</p>
            )}
          </div>
          <Button
            variant="ghost"
            size="icon"
            className="h-8 w-8 text-muted-foreground hover:text-destructive"
            onClick={() => {
              localStorage.removeItem("token");
              window.location.href = "/login";
            }}
          >
            <LogOut className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </aside>
  );
}
