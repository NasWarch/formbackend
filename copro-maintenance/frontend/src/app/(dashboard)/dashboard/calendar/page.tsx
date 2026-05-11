"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import {
  Calendar as CalendarIcon,
  Loader2,
  AlertTriangle,
  Clock,
  Building2,
  Wrench,
  ChevronRight,
  CalendarDays,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import ComplianceBadge from "@/components/dashboard/ComplianceBadge";
import api, { ApiError } from "@/lib/api";

interface EquipmentItem {
  id: number;
  name: string;
  equipment_type: string;
  serial_number: string | null;
  installation_date: string | null;
  last_control_date: string | null;
  next_control_date: string | null;
  status: "ok" | "pending" | "overdue";
  building_id: number;
}

interface Building {
  id: number;
  name: string;
}

function formatDate(dateStr: string | null): string {
  if (!dateStr) return "—";
  return new Date(dateStr).toLocaleDateString("fr-FR", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });
}

function daysUntil(dateStr: string): number {
  const target = new Date(dateStr);
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  target.setHours(0, 0, 0, 0);
  return Math.ceil((target.getTime() - today.getTime()) / (1000 * 60 * 60 * 24));
}

function getWeekNumber(date: Date): number {
  const start = new Date(date.getFullYear(), 0, 1);
  const diff = date.getTime() - start.getTime();
  return Math.ceil((diff / (1000 * 60 * 60 * 24) + start.getDay() + 1) / 7);
}

export default function CalendarPage() {
  const [equipment, setEquipment] = useState<EquipmentItem[]>([]);
  const [buildings, setBuildings] = useState<Record<number, string>>({});
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchData() {
      try {
        const [equipData, buildingsData] = await Promise.all([
          api.get<EquipmentItem[]>("/equipment"),
          api.get<Building[]>("/buildings"),
        ]);

        const buildingMap: Record<number, string> = {};
        for (const b of buildingsData) {
          buildingMap[b.id] = b.name;
        }
        setBuildings(buildingMap);

        // Filter: only equipment with next_control_date within 30 days
        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const thirtyDaysFromNow = new Date(today);
        thirtyDaysFromNow.setDate(thirtyDaysFromNow.getDate() + 30);

        const upcoming = equipData
          .filter((eq) => {
            if (!eq.next_control_date) return false;
            const nextDate = new Date(eq.next_control_date);
            nextDate.setHours(0, 0, 0, 0);
            return nextDate >= today && nextDate <= thirtyDaysFromNow;
          })
          .sort((a, b) => {
            const dateA = new Date(a.next_control_date!).getTime();
            const dateB = new Date(b.next_control_date!).getTime();
            return dateA - dateB;
          });

        setEquipment(upcoming);
      } catch (err) {
        if (err instanceof ApiError) {
          setError(err.message || "Erreur lors du chargement du calendrier.");
        } else {
          setError("Impossible de contacter le serveur.");
        }
      } finally {
        setIsLoading(false);
      }
    }

    fetchData();
  }, []);

  // Group by week
  const groupedByWeek: Record<number, EquipmentItem[]> = {};
  for (const eq of equipment) {
    const date = new Date(eq.next_control_date!);
    const week = getWeekNumber(date);
    if (!groupedByWeek[week]) groupedByWeek[week] = [];
    groupedByWeek[week].push(eq);
  }

  // Loading state
  if (isLoading) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3 }}
        className="flex items-center justify-center py-20"
      >
        <div className="flex flex-col items-center gap-3">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
          <p className="text-sm text-muted-foreground">
            Chargement du calendrier…
          </p>
        </div>
      </motion.div>
    );
  }

  // Error state
  if (error) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3 }}
        className="flex items-center justify-center py-20"
      >
        <div className="rounded-xl border border-red-200 bg-red-50 px-6 py-4 text-center max-w-md">
          <AlertTriangle className="mx-auto h-8 w-8 text-destructive" />
          <p className="mt-2 text-sm font-medium text-red-700">{error}</p>
          <Button
            variant="outline"
            className="mt-3"
            onClick={() => window.location.reload()}
          >
            Réessayer
          </Button>
        </div>
      </motion.div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Page title */}
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-card-foreground">
          Calendrier des contrôles
        </h1>
        <p className="mt-1 text-sm text-muted-foreground">
          {equipment.length} contrôle{equipment.length !== 1 ? "s" : ""} prévu{equipment.length !== 1 ? "s" : ""} dans les 30 prochains jours
        </p>
      </div>

      {equipment.length > 0 ? (
        Object.entries(groupedByWeek).map(([week, items]) => {
          const firstDate = new Date(items[0].next_control_date!);

          return (
            <Card key={week} className="border-border shadow-sm">
              <CardHeader className="pb-3">
                <CardTitle className="flex items-center gap-2 text-sm font-semibold text-card-foreground">
                  <CalendarDays className="h-4 w-4 text-primary" />
                  Semaine {week} — à partir du{" "}
                  {firstDate.toLocaleDateString("fr-FR", {
                    weekday: "long",
                    day: "numeric",
                    month: "long",
                  })}
                </CardTitle>
              </CardHeader>
              <Separator />
              <CardContent className="p-0">
                <div className="divide-y divide-border">
                  {items.map((eq) => {
                    const days = daysUntil(eq.next_control_date!);
                    const isToday = days === 0;
                    const isTomorrow = days === 1;
                    const isUrgent = days <= 7;

                    return (
                      <Link
                        key={eq.id}
                        href={`/dashboard/equipment/${eq.id}`}
                        className="flex items-center justify-between px-5 py-4 transition-colors hover:bg-muted"
                      >
                        <div className="flex items-center gap-3 min-w-0">
                          <div
                            className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-lg ${
                              isUrgent
                                ? "bg-red-50 text-destructive"
                                : "bg-orange-50 text-orange-600"
                            }`}
                          >
                            <Clock className="h-4 w-4" />
                          </div>
                          <div className="min-w-0">
                            <p className="text-sm font-medium text-card-foreground truncate">
                              {eq.name}
                            </p>
                            <div className="flex items-center gap-2 mt-0.5 text-xs text-muted-foreground">
                              <span className="flex items-center gap-1">
                                <Building2 className="h-3 w-3" />
                                {buildings[eq.building_id] || `Immeuble #${eq.building_id}`}
                              </span>
                              <span>·</span>
                              <span>{eq.equipment_type}</span>
                            </div>
                          </div>
                        </div>
                        <div className="flex items-center gap-3 shrink-0">
                          <div className="text-right">
                            <p
                              className={`text-xs font-semibold ${
                                isUrgent ? "text-destructive" : "text-orange-600"
                              }`}
                            >
                              {new Date(eq.next_control_date!).toLocaleDateString(
                                "fr-FR",
                                { day: "numeric", month: "short" }
                              )}
                            </p>
                            <p className="text-xs text-muted-foreground/70">
                              {isToday
                                ? "Aujourd'hui"
                                : isTomorrow
                                  ? "Demain"
                                  : `dans ${days} jours`}
                            </p>
                          </div>
                          <ComplianceBadge status={eq.status} />
                          <ChevronRight className="h-4 w-4 text-muted-foreground/50" />
                        </div>
                      </Link>
                    );
                  })}
                </div>
              </CardContent>
            </Card>
          );
        })
      ) : (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
        >
          <Card className="border-border shadow-sm">
            <CardContent className="flex flex-col items-center justify-center py-16 text-center">
              <CalendarIcon className="h-12 w-12 text-muted-foreground/50" />
              <p className="mt-3 text-sm font-medium text-muted-foreground">
                Aucun contrôle prévu dans les 30 prochains jours
              </p>
              <p className="mt-1 text-xs text-muted-foreground/70">
                Tous vos équipements sont à jour ou n&apos;ont pas encore de prochaine échéance.
              </p>
            </CardContent>
          </Card>
        </motion.div>
      )}
    </div>
  );
}
