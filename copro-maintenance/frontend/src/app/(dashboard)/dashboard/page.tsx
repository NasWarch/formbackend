"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import {
  Building2,
  Wrench,
  CalendarCheck2,
  AlertTriangle,
  Loader2,
  ArrowRight,
  Clock,
  CheckCircle2,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import StatsCard from "@/components/dashboard/StatsCard";
import api, { ApiError } from "@/lib/api";

interface UpcomingControl {
  equipment_id: number;
  equipment_name: string;
  equipment_type: string;
  building_name: string;
  next_control_date: string;
}

interface DashboardSummary {
  total_buildings: number;
  total_equipment: number;
  equipment_ok: number;
  equipment_pending: number;
  equipment_overdue: number;
  upcoming_controls: UpcomingControl[];
}

export default function DashboardPage() {
  const [data, setData] = useState<DashboardSummary | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchSummary() {
      try {
        const summary = await api.get<DashboardSummary>("/dashboard/summary");
        setData(summary);
      } catch (err) {
        if (err instanceof ApiError) {
          setError(err.message || "Erreur lors du chargement du tableau de bord.");
        } else {
          setError("Impossible de contacter le serveur.");
        }
      } finally {
        setIsLoading(false);
      }
    }

    fetchSummary();
  }, []);

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
            Chargement du tableau de bord…
          </p>
        </div>
      </motion.div>
    );
  }

  // Error state
  if (error || !data) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3 }}
        className="flex items-center justify-center py-20"
      >
        <div className="rounded-xl border border-red-200 bg-red-50 px-6 py-4 text-center max-w-md">
          <AlertTriangle className="mx-auto h-8 w-8 text-destructive" />
          <p className="mt-2 text-sm font-medium text-red-700">
            {error || "Données non disponibles."}
          </p>
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
    <div className="space-y-8">
      {/* Page title */}
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-card-foreground">
          Tableau de bord
        </h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Vue d&apos;ensemble de votre portefeuille de copropriétés
        </p>
      </div>

      {/* Stats grid */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatsCard
          title="Immeubles"
          value={data.total_buildings}
          description="Copropriétés gérées"
          icon={Building2}
        />
        <StatsCard
          title="Équipements"
          value={data.total_equipment}
          description="Tous types confondus"
          icon={Wrench}
        />
        <StatsCard
          title="Conformes"
          value={data.equipment_ok}
          description="Contrôles à jour"
          icon={CheckCircle2}
        />
        <StatsCard
          title="En retard"
          value={data.equipment_overdue}
          description="Actions requises"
          icon={AlertTriangle}
          variant="danger"
        />
      </div>

      {/* Upcoming controls list */}
      <Card className="border-border shadow-sm">
        <CardHeader className="flex flex-row items-center justify-between pb-3">
          <CardTitle className="text-base font-semibold text-card-foreground">
            Prochains contrôles (30 jours)
          </CardTitle>
          <Link href="/dashboard/calendar">
            <Button variant="ghost" size="sm" className="gap-1 text-muted-foreground hover:text-primary">
              Calendrier <ArrowRight className="h-3.5 w-3.5" />
            </Button>
          </Link>
        </CardHeader>
        <Separator />
        <CardContent className="pt-4">
          {data.upcoming_controls && data.upcoming_controls.length > 0 ? (
            <div className="space-y-3">
              {data.upcoming_controls.map((control) => {
                const controlDate = new Date(control.next_control_date);
                const today = new Date();
                const diffDays = Math.ceil(
                  (controlDate.getTime() - today.getTime()) /
                    (1000 * 60 * 60 * 24)
                );
                const isUrgent = diffDays <= 7;

                return (
                  <div
                    key={control.equipment_id}
                    className="flex items-center justify-between rounded-lg border border-border p-3"
                  >
                    <div className="flex items-center gap-3 min-w-0">
                      <div
                        className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-lg ${
                          isUrgent ? "bg-red-50 text-destructive" : "bg-orange-50 text-orange-600"
                        }`}
                      >
                        <Clock className="h-4 w-4" />
                      </div>
                      <div className="min-w-0">
                        <p className="truncate text-sm font-medium text-card-foreground">
                          {control.equipment_name}
                        </p>
                        <p className="truncate text-xs text-muted-foreground">
                          {control.building_name} · {control.equipment_type}
                        </p>
                      </div>
                    </div>
                    <div className="shrink-0 text-right">
                      <p
                        className={`text-xs font-semibold ${
                          isUrgent ? "text-destructive" : "text-orange-600"
                        }`}
                      >
                        {controlDate.toLocaleDateString("fr-FR", {
                          day: "numeric",
                          month: "short",
                        })}
                      </p>
                      <p className="text-xs text-muted-foreground/70">
                        {diffDays <= 0
                          ? "Aujourd'hui"
                          : diffDays === 1
                            ? "Demain"
                            : `dans ${diffDays} jours`}
                      </p>
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
              className="flex flex-col items-center justify-center py-8 text-center"
            >
              <CalendarCheck2 className="h-10 w-10 text-muted-foreground/50" />
              <p className="mt-2 text-sm text-muted-foreground/70">
                Aucun contrôle prévu dans les 30 prochains jours
              </p>
            </motion.div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
