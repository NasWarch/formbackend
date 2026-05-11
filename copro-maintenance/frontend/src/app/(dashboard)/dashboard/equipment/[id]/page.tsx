"use client";

import { useEffect, useState, useCallback } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import {
  Wrench,
  Calendar,
  ClipboardList,
  Loader2,
  ArrowLeft,
  Building2,
  AlertTriangle,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import ComplianceBadge from "@/components/dashboard/ComplianceBadge";
import AddControlDialog from "@/components/dashboard/AddControlDialog";
import api, { ApiError } from "@/lib/api";

interface EquipmentDetail {
  id: number;
  name: string;
  equipment_type: string;
  serial_number: string | null;
  installation_date: string | null;
  last_control_date: string | null;
  next_control_date: string | null;
  status: "ok" | "pending" | "overdue";
  notes: string | null;
  building_id: number;
  building_name: string;
}

interface MaintenanceRecord {
  id: number;
  control_date: string;
  next_control_date: string | null;
  provider_name: string | null;
  result: string;
  notes: string | null;
  document_id: number | null;
  created_at: string;
}

function formatDate(dateStr: string | null): string {
  if (!dateStr) return "—";
  return new Date(dateStr).toLocaleDateString("fr-FR", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });
}

function formatDateShort(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString("fr-FR", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

const resultLabels: Record<string, string> = {
  ok: "Conforme",
  issue: "Anomalie",
  partial: "Partiel",
};

const resultColors: Record<string, string> = {
  ok: "text-[#16a34a] bg-[#e8f5ee]",
  issue: "text-[#dc2626] bg-red-50",
  partial: "text-[#d97706] bg-orange-50",
};

export default function EquipmentDetailPage() {
  const params = useParams();
  const equipmentId = params.id as string;

  const [equipment, setEquipment] = useState<EquipmentDetail | null>(null);
  const [records, setRecords] = useState<MaintenanceRecord[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [recordsLoading, setRecordsLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchEquipment = useCallback(async () => {
    try {
      const data = await api.get<EquipmentDetail>(
        `/equipment/${equipmentId}`
      );
      setEquipment(data);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message || "Erreur lors du chargement.");
      } else {
        setError("Impossible de contacter le serveur.");
      }
    } finally {
      setIsLoading(false);
    }
  }, [equipmentId]);

  const fetchRecords = useCallback(async () => {
    try {
      const data = await api.get<MaintenanceRecord[]>(
        `/equipment/${equipmentId}/records`
      );
      setRecords(data);
    } catch {
      // Records may be empty — not a fatal error
    } finally {
      setRecordsLoading(false);
    }
  }, [equipmentId]);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchEquipment();
     
    fetchRecords();
  }, [fetchEquipment, fetchRecords]);

  const handleControlAdded = useCallback(() => {
    fetchEquipment();
    fetchRecords();
  }, [fetchEquipment, fetchRecords]);

  // Loading state
  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="flex flex-col items-center gap-3">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
          <p className="text-sm text-muted-foreground">
            Chargement de l&apos;équipement…
          </p>
        </div>
      </div>
    );
  }

  // Error state
  if (error || !equipment) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="rounded-xl border border-red-200 bg-red-50 px-6 py-4 text-center max-w-md">
          <AlertTriangle className="mx-auto h-8 w-8 text-destructive" />
          <p className="mt-2 text-sm font-medium text-red-700">
            {error || "Équipement introuvable."}
          </p>
          <div className="mt-3 flex gap-2 justify-center">
            <Link href="/dashboard/buildings">
              <Button variant="outline">Retour aux immeubles</Button>
            </Link>
            <Button variant="outline" onClick={() => window.location.reload()}>
              Réessayer
            </Button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Back link */}
      <Link
        href={`/dashboard/buildings/${equipment.building_id}`}
        className="inline-flex items-center gap-1.5 text-sm text-muted-foreground hover:text-primary transition-colors"
      >
        <ArrowLeft className="h-4 w-4" />
        Retour à {equipment.building_name}
      </Link>

      {/* Equipment header */}
      <div className="rounded-xl border border-border bg-card p-6 shadow-sm">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
          <div className="flex items-start gap-4">
            <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-accent text-primary">
              <Wrench className="h-6 w-6" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-card-foreground">
                {equipment.name}
              </h1>
              <div className="mt-1 flex flex-wrap items-center gap-x-4 gap-y-1 text-sm text-muted-foreground">
                <span>{equipment.equipment_type}</span>
                {equipment.serial_number && (
                  <span>S/N : {equipment.serial_number}</span>
                )}
                <Link
                  href={`/dashboard/buildings/${equipment.building_id}`}
                  className="flex items-center gap-1 text-primary hover:underline"
                >
                  <Building2 className="h-3.5 w-3.5" />
                  {equipment.building_name}
                </Link>
              </div>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <ComplianceBadge status={equipment.status} />
            <AddControlDialog
              equipmentId={equipment.id}
              onSuccess={handleControlAdded}
            />
          </div>
        </div>
      </div>

      {/* Detail cards */}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Card className="border-border shadow-sm">
          <CardContent className="p-4">
            <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground/70">
              Installation
            </p>
            <p className="mt-1 text-sm font-medium text-card-foreground">
              {formatDate(equipment.installation_date)}
            </p>
          </CardContent>
        </Card>
        <Card className="border-border shadow-sm">
          <CardContent className="p-4">
            <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground/70">
              Dernier contrôle
            </p>
            <p className="mt-1 text-sm font-medium text-card-foreground">
              {formatDate(equipment.last_control_date)}
            </p>
          </CardContent>
        </Card>
        <Card className="border-border shadow-sm">
          <CardContent className="p-4">
            <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground/70">
              Prochain contrôle
            </p>
            <p
              className={`mt-1 text-sm font-medium ${
                equipment.status === "overdue"
                  ? "text-destructive"
                  : "text-card-foreground"
              }`}
            >
              {formatDate(equipment.next_control_date)}
            </p>
          </CardContent>
        </Card>
        <Card className="border-border shadow-sm">
          <CardContent className="p-4">
            <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground/70">
              Historique
            </p>
            <p className="mt-1 text-sm font-medium text-card-foreground">
              {records.length} contrôle{records.length !== 1 ? "s" : ""}
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Maintenance history */}
      <Card className="border-border shadow-sm">
        <CardHeader className="pb-3">
          <CardTitle className="text-base font-semibold text-card-foreground flex items-center gap-2">
            <ClipboardList className="h-4 w-4" />
            Historique de maintenance
          </CardTitle>
        </CardHeader>
        <Separator />

        {recordsLoading ? (
          <CardContent className="flex items-center justify-center py-8">
            <Loader2 className="h-5 w-5 animate-spin text-muted-foreground/70" />
          </CardContent>
        ) : records.length > 0 ? (
          <CardContent className="p-0">
            <div className="divide-y divide-border">
              {records.map((record) => (
                <div
                  key={record.id}
                  className="flex items-center justify-between px-5 py-4"
                >
                  <div className="flex items-center gap-3 min-w-0">
                    <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-muted text-card-foreground">
                      <Calendar className="h-4 w-4" />
                    </div>
                    <div className="min-w-0">
                      <p className="text-sm font-medium text-card-foreground">
                        {formatDateShort(record.control_date)}
                      </p>
                      {record.provider_name && (
                        <p className="text-xs text-muted-foreground truncate">
                          {record.provider_name}
                        </p>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center gap-3 shrink-0">
                    {record.notes && (
                      <span
                        className="hidden sm:block text-xs text-muted-foreground/70 truncate max-w-[180px]"
                        title={record.notes}
                      >
                        {record.notes}
                      </span>
                    )}
                    <span
                      className={`inline-flex rounded-full px-2.5 py-0.5 text-xs font-medium ${
                        resultColors[record.result] || "text-muted-foreground bg-muted"
                      }`}
                    >
                      {resultLabels[record.result] || record.result}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        ) : (
          <CardContent className="flex flex-col items-center justify-center py-12 text-center">
            <ClipboardList className="h-10 w-10 text-muted-foreground/50" />
            <p className="mt-2 text-sm text-muted-foreground">
              Aucun historique de maintenance
            </p>
            <p className="mt-1 text-xs text-muted-foreground/70">
              Ajoutez un premier contrôle avec le bouton ci-dessus.
            </p>
          </CardContent>
        )}
      </Card>
    </div>
  );
}
