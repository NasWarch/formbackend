"use client";

import { motion } from "framer-motion";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { CheckCircle2, Clock, AlertTriangle } from "lucide-react";

type ComplianceStatus = "ok" | "pending" | "overdue";

interface ComplianceBadgeProps {
  status: ComplianceStatus;
  className?: string;
}

const statusConfig: Record<
  ComplianceStatus,
  {
    label: string;
    icon: typeof CheckCircle2;
    className: string;
  }
> = {
  ok: {
    label: "Conforme",
    icon: CheckCircle2,
    className:
      "bg-[#e8f5ee] text-[#1a7a4a] border-[#1a7a4a]/20 hover:bg-[#d4efe0]",
  },
  pending: {
    label: "À prévoir",
    icon: Clock,
    className:
      "bg-orange-50 text-[#d97706] border-[#d97706]/20 hover:bg-orange-100",
  },
  overdue: {
    label: "En retard",
    icon: AlertTriangle,
    className: "bg-red-50 text-[#dc2626] border-[#dc2626]/20 hover:bg-red-100",
  },
};

export default function ComplianceBadge({
  status,
  className,
}: ComplianceBadgeProps) {
  const config = statusConfig[status];
  const Icon = config.icon;

  return (
    <motion.span
      whileHover={{ scale: 1.05 }}
      transition={{ duration: 0.15, ease: [0.22, 1, 0.36, 1] }}
      className="inline-flex"
    >
      <Badge
        variant="outline"
        className={cn(
          "gap-1.5 px-2.5 py-1 text-xs font-medium",
          config.className,
          className
        )}
      >
        <Icon className="h-3.5 w-3.5" />
        {config.label}
      </Badge>
    </motion.span>
  );
}
