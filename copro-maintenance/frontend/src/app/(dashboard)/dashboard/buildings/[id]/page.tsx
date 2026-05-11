"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import {
  Building2,
  Wrench,
  Calendar,
  MapPin,
  Hash,
  Loader2,
  AlertTriangle,
  ArrowLeft,
  Plus,
  CheckCircle2,
  Clock,
  ChevronRight,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import StatsCard from "@/components/dashboard/StatsCard";
import ComplianceBadge from "@/components/dashboard/ComplianceBadge";
import api, { ApiError } from "@/lib/api";

interface EquipmentItem {
  id: number;
  name: string;
  equipment_type: string;
  status: "ok" | "pending" | "overdue";
  last_control_date: string | null;
  next_control_date: string | null;
}

interface BuildingDetail {
  id: number;
  name: string;
  address: string;
  city: string;
  postal_code: string;
  nb_lots: number;
  created_at: string;
  equipment: EquipmentItem[];
}

function computeStats(equipment: EquipmentItem[]) {
  const total = equipment.length;
  const ok = equipment.filter((e) => e.status === "ok").length;
  const pending = equipment.filter((e) => e.status === "pending").length;
  const overdue = equipment.filter((e) => e.status === "overdue").length;
  return { total, ok, pending, overdue };
}

function groupByType(
  equipment: EquipmentItem[]
): Record<string, EquipmentItem[]> {
  const groups: Record<string, EquipmentItem[]> = {};
  for (const eq of equipment) {
    const type = eq.equipment_type || "Autre";
    if (!groups[type]) groups[type] = [];
    groups[type].push(eq);
  }
  return groups;
}

function formatDate(dateStr: string | null): string {
  if (!dateStr) return "—";
  return new Date(dateStr).toLocaleDateString("fr-FR", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

export default function BuildingDetailPage() {
  const params = useParams();
  const buildingId = params.id as string;

  const [building, setBuilding] = useState<BuildingDetail | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchBuilding() {
      try {
        const data = await api.get<BuildingDetail>(`/buildings/${buildingId}`);
        setBuilding(data);
      } catch (err) {
        if (err instanceof ApiError) {
          setError(err.message || "Erreur lors du chargement de l'immeuble.");
        } else {
          setError("Impossible de contacter le serveur.");
        }
      } finally {
        setIsLoading(false);
      }
    }

    fetchBuilding();
  }, [buildingId]);

  // Loading state
  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="flex flex-col items-center gap-3">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
          <p className="text-sm text-muted-foreground">
            Chargement de l&apos;immeuble…
          </p>
        </div>
      </div>
    );
  }

  // Error state
  if (error || !building) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="rounded-xl border border-red-200 bg-red-50 px-6 py-4 text-center max-w-md">
          <AlertTriangle className="mx-auto h-8 w-8 text-destructive" />
          <p className="mt-2 text-sm font-medium text-red-700">
            {error || "Immeuble introuvable."}
          </p>
          <div className="mt-3 flex gap-2 justify-center">
            <Link href="/dashboard/buildings">
              <Button variant="outline">Retour aux immeubles</Button>
            </Link>
            <Button
              variant="outline"
              onClick={() => window.location.reload()}
            >
              Réessayer
            </Button>
          </div>
        </div>
      </div>
    );
  }

  const equipmentList = building.equipment || [];
  const stats = computeStats(equipmentList);
  const grouped = groupByType(equipmentList);

  return (
    <div className="space-y-6">
      {/* Back link */}
      <Link
        href="/dashboard/buildings"
        className="inline-flex items-center gap-1.5 text-sm text-muted-foreground hover:text-primary transition-colors"
      >
        <ArrowLeft className="h-4 w-4" />
        Retour aux immeubles
      </Link>

      {/* Building header */}
      <div className="rounded-xl border border-border bg-card p-6 shadow-sm">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
          <div className="flex items-start gap-4">
            <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-accent text-primary">
              <Building2 className="h-6 w-6" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-card-foreground">
                {building.name}
              </h1>
              <div className="mt-1.5 flex flex-wrap items-center gap-x-4 gap-y-1 text-sm text-muted-foreground">
                <span className="flex items-center gap-1.5">
                  <MapPin className="h-3.5 w-3.5" />
                  {building.address}
                  {building.postal_code && `, ${building.postal_code}`}{" "}
                  {building.city}
                </span>
                <span className="flex items-center gap-1.5">
                  <Hash className="h-3.5 w-3.5" />
                  {building.nb_lots} lots
                </span>
              </div>
            </div>
          </div>

          <Link href={`/dashboard/equipment/new?building_id=${building.id}`}>
            <Button className="gap-2 bg-primary hover:bg-primary/90 shrink-0">
              <Plus className="h-4 w-4" />
              Équipement
            </Button>
          </Link>
        </div>
      </div>

      {/* Stats */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatsCard
          title="Équipements"
          value={stats.total}
          description="Total"
          icon={Wrench}
        />
        <StatsCard
          title="Conformes"
          value={stats.ok}
          description="À jour"
          icon={CheckCircle2}
        />
        <StatsCard
          title="À prévoir"
          value={stats.pending}
          description="Contrôles à planifier"
          icon={Clock}
          variant="warning"
        />
        <StatsCard
          title="En retard"
          value={stats.overdue}
          description="Actions requises"
          icon={AlertTriangle}
          variant="danger"
        />
      </div>

      {/* Equipment list grouped by type */}
      {Object.keys(grouped).length > 0 ? (
        <div className="space-y-6">
          {Object.entries(grouped).map(([type, equipments]) => (
            <Card key={type} className="border-border shadow-sm">
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-semibold uppercase tracking-wider text-muted-foreground">
                  {type}
                </CardTitle>
              </CardHeader>
              <Separator />
              <CardContent className="p-0">
                <div className="divide-y divide-[#e2e8e6]">
                  {equipments.map((eq) => (
                    <Link
                      key={eq.id}
                      href={`/dashboard/equipment/${eq.id}`}
                      className="flex items-center justify-between px-5 py-4 transition-colors hover:bg-muted"
                    >
                      <div className="flex items-center gap-3 min-w-0">
                        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-muted text-card-foreground">
                          <Wrench className="h-4 w-4" />
                        </div>
                        <div className="min-w-0">
                          <p className="text-sm font-medium text-card-foreground truncate">
                            {eq.name}
                          </p>
                          <div className="flex items-center gap-3 mt-0.5 text-xs text-muted-foreground/70">
                            <span className="flex items-center gap-1">
                              <Calendar className="h-3 w-3" />
                              Dernier : {formatDate(eq.last_control_date)}
                            </span>
                            <span className="flex items-center gap-1">
                              <Clock className="h-3 w-3" />
                              Prochain : {formatDate(eq.next_control_date)}
                            </span>
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center gap-3 shrink-0">
                        <ComplianceBadge status={eq.status} />
                        <ChevronRight className="h-4 w-4 text-muted-foreground/50" />
                      </div>
                    </Link>
                  ))}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : (
        <Card className="border-border shadow-sm">
          <CardContent className="flex flex-col items-center justify-center py-12 text-center">
            <Wrench className="h-12 w-12 text-muted-foreground/50" />
            <p className="mt-3 text-sm font-medium text-muted-foreground">
              Aucun équipement enregistré
            </p>
            <p className="mt-1 text-xs text-muted-foreground/70">
              Ajoutez le premier équipement de cet immeuble.
            </p>
            <Link
              href={`/dashboard/equipment/new?building_id=${building.id}`}
              className="mt-4"
            >
              <Button className="gap-2 bg-primary hover:bg-primary/90">
                <Plus className="h-4 w-4" />
                Ajouter un équipement
              </Button>
            </Link>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
