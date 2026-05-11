"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";
import type { LucideIcon } from "lucide-react";
import { TrendingUp, TrendingDown } from "lucide-react";

interface StatsCardProps {
  title: string;
  value: string | number;
  description?: string;
  icon: LucideIcon;
  trend?: { value: string; positive: boolean };
  variant?: "default" | "warning" | "danger";
}

const variantStyles = {
  default: {
    iconBg: "bg-accent",
    iconColor: "text-primary",
    valueColor: "text-card-foreground",
  },
  warning: {
    iconBg: "bg-orange-50",
    iconColor: "text-orange-600",
    valueColor: "text-orange-700",
  },
  danger: {
    iconBg: "bg-red-50",
    iconColor: "text-destructive",
    valueColor: "text-red-700",
  },
};

export default function StatsCard({
  title,
  value,
  description,
  icon: Icon,
  trend,
  variant = "default",
}: StatsCardProps) {
  const styles = variantStyles[variant];

  return (
    <motion.div
      className="rounded-xl border border-border bg-card p-5 shadow-sm transition-shadow"
      initial={{ opacity: 0, y: 12 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-40px" }}
      transition={{ duration: 0.3, ease: [0.22, 1, 0.36, 1] }}
      whileHover={{ scale: 1.02 }}
      style={{ boxShadow: "0 1px 3px 0 rgb(0 0 0 / 0.1)" }}
      onHoverStart={(e) => {
        // Add shadow on hover
      }}
    >
      <div className="flex items-start gap-4">
        {/* Icon */}
        <div
          className={cn(
            "flex h-11 w-11 shrink-0 items-center justify-center rounded-lg",
            styles.iconBg
          )}
        >
          <Icon className={cn("h-5 w-5", styles.iconColor)} />
        </div>

        {/* Content */}
        <div className="flex-1 min-w-0">
          <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground/70">
            {title}
          </p>
          <motion.p
            className={cn(
              "mt-1 text-2xl font-bold tracking-tight",
              styles.valueColor
            )}
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.4, delay: 0.15 }}
          >
            {value}
          </motion.p>
          {description && (
            <p className="mt-0.5 text-sm text-muted-foreground">{description}</p>
          )}
          {trend && (
            <div className="mt-2 flex items-center gap-1">
              {trend.positive ? (
                <TrendingUp className="h-3.5 w-3.5 text-green-600" />
              ) : (
                <TrendingDown className="h-3.5 w-3.5 text-destructive" />
              )}
              <span
                className={cn(
                  "text-xs font-medium",
                  trend.positive ? "text-green-600" : "text-destructive"
                )}
              >
                {trend.value}
              </span>
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
}
