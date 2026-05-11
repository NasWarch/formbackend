"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import {
  Wrench,
  Plus,
  Loader2,
  AlertTriangle,
  Building2,
  ChevronRight,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import ComplianceBadge from "@/components/dashboard/ComplianceBadge";
import api, { ApiError } from "@/lib/api";

interface EquipmentItem {
  id: number;
  name: string;
  equipment_type: string;
  status: "ok" | "pending" | "overdue";
  last_control_date: string | null;
  next_control_date: string | null;
  building_id: number;
  building_name?: string;
}

export default function EquipmentListPage() {
  const [equipment, setEquipment] = useState<EquipmentItem[]>([]);
  const [buildings, setBuildings] = useState<Record<number, string>>({});
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");

  useEffect(() => {
    async function fetchData() {
      try {
        const [equipData, buildingsData] = await Promise.all([
          api.get<EquipmentItem[]>("/equipment"),
          api.get<{ id: number; name: string }[]>("/buildings"),
        ]);
        const buildingMap: Record<number, string> = {};
        for (const b of buildingsData) {
          buildingMap[b.id] = b.name;
        }
        setBuildings(buildingMap);
        setEquipment(equipData);
      } catch (err) {
        if (err instanceof ApiError) {
          setError(err.message || "Erreur lors du chargement.");
        } else {
          setError("Impossible de contacter le serveur.");
        }
      } finally {
        setIsLoading(false);
      }
    }
    fetchData();
  }, []);

  const filtered = equipment.filter((eq) => {
    if (!search.trim()) return true;
    const q = search.toLowerCase();
    return (
      eq.name.toLowerCase().includes(q) ||
      eq.equipment_type.toLowerCase().includes(q) ||
      (buildings[eq.building_id] || "").toLowerCase().includes(q)
    );
  });

  if (isLoading) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3 }}
        className="flex items-center justify-center py-20"
      >
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </motion.div>
    );
  }

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
        </div>
      </motion.div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-card-foreground">
            Équipements
          </h1>
          <p className="mt-1 text-sm text-muted-foreground">
            {equipment.length} équipement{equipment.length !== 1 ? "s" : ""}
          </p>
        </div>
        <Link href="/dashboard/equipment/new">
          <Button className="gap-2 bg-primary hover:bg-primary/90">
            <Plus className="h-4 w-4" />
            Nouvel équipement
          </Button>
        </Link>
      </div>

      <div className="relative">
        <Input
          placeholder="Rechercher par nom, type ou immeuble…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {filtered.length > 0 ? (
        <div className="space-y-2">
          {filtered.map((eq) => (
            <Link
              key={eq.id}
              href={`/dashboard/equipment/${eq.id}`}
              className="flex items-center justify-between rounded-lg border border-border bg-card p-4 transition-colors hover:bg-muted"
            >
              <div className="flex items-center gap-3 min-w-0">
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-muted text-card-foreground">
                  <Wrench className="h-5 w-5" />
                </div>
                <div className="min-w-0">
                  <p className="text-sm font-medium text-card-foreground truncate">
                    {eq.name}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    {eq.equipment_type}
                    {buildings[eq.building_id] && ` · ${buildings[eq.building_id]}`}
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-3 shrink-0">
                <ComplianceBadge status={eq.status} />
                <ChevronRight className="h-4 w-4 text-muted-foreground/50" />
              </div>
            </Link>
          ))}
        </div>
      ) : (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
          className="flex flex-col items-center justify-center rounded-xl border border-dashed border-muted-foreground/30 bg-card py-16"
        >
          <Wrench className="h-12 w-12 text-muted-foreground/50" />
          <p className="mt-3 text-sm font-medium text-muted-foreground">
            {search ? "Aucun équipement trouvé" : "Aucun équipement enregistré"}
          </p>
        </motion.div>
      )}
    </div>
  );
}
