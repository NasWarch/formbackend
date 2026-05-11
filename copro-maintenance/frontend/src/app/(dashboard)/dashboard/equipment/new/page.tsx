"use client";

import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import {
  Wrench,
  Loader2,
  ArrowLeft,
  Save,
  Building2,
  AlertTriangle,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import api, { ApiError } from "@/lib/api";

const EQUIPMENT_TYPES = [
  "Ascenseur",
  "Chaudière",
  "Porte de garage",
  "Désenfumage",
  "Électricité",
  "Porte automatique",
  "Extincteur",
  "Alarme incendie",
  "Ventilation",
  "Toiture",
  "Façade",
  "Autre",
];

interface Building {
  id: number;
  name: string;
  address: string;
  city: string;
}

export default function NewEquipmentPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const preselectedBuildingId = searchParams.get("building_id") || "";

  const [buildings, setBuildings] = useState<Building[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [submitError, setSubmitError] = useState("");

  const [formData, setFormData] = useState({
    name: "",
    equipment_type: "",
    serial_number: "",
    installation_date: "",
    building_id: preselectedBuildingId,
  });

  useEffect(() => {
    async function fetchBuildings() {
      try {
        const data = await api.get<Building[]>("/buildings");
        setBuildings(data);
      } catch (err) {
        if (err instanceof ApiError) {
          setError(err.message || "Erreur lors du chargement des immeubles.");
        } else {
          setError("Impossible de contacter le serveur.");
        }
      } finally {
        setIsLoading(false);
      }
    }

    fetchBuildings();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
    if (submitError) setSubmitError("");
  };

  const handleSelectChange = (field: string) => (value: string | null) => {
    if (value === null) return;
    setFormData((prev) => ({ ...prev, [field]: value }));
    if (submitError) setSubmitError("");
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitError("");

    if (!formData.name || !formData.equipment_type || !formData.building_id) {
      setSubmitError("Veuillez remplir les champs obligatoires.");
      return;
    }

    setIsSubmitting(true);

    try {
      const created = await api.post<{ id: number; building_id: number }>(
        "/equipment",
        {
          name: formData.name,
          equipment_type: formData.equipment_type,
          serial_number: formData.serial_number || undefined,
          installation_date: formData.installation_date || undefined,
          building_id: formData.building_id,
        }
      );

      router.push(`/dashboard/buildings/${created.building_id}`);
    } catch (err) {
      if (err instanceof ApiError) {
        setSubmitError(err.message || "Erreur lors de la création.");
      } else {
        setSubmitError("Impossible de contacter le serveur.");
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-20">
        <div className="flex flex-col items-center gap-3">
          <Loader2 className="h-8 w-8 animate-spin text-primary" />
          <p className="text-sm text-muted-foreground">
            Chargement…
          </p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center py-20">
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
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      {/* Back link */}
      <Link
        href={
          preselectedBuildingId
            ? `/dashboard/buildings/${preselectedBuildingId}`
            : "/dashboard/buildings"
        }
        className="inline-flex items-center gap-1.5 text-sm text-muted-foreground hover:text-primary transition-colors"
      >
        <ArrowLeft className="h-4 w-4" />
        Retour
      </Link>

      {/* Form card */}
      <Card className="border-border shadow-sm">
        <CardHeader>
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-accent text-primary">
              <Wrench className="h-5 w-5" />
            </div>
            <div>
              <CardTitle className="text-lg font-semibold text-card-foreground">
                Nouvel équipement
              </CardTitle>
              <p className="text-xs text-muted-foreground">
                Ajoutez un équipement à suivre dans votre carnet d&apos;entretien.
              </p>
            </div>
          </div>
        </CardHeader>

        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-5">
            {submitError && (
              <div className="rounded-lg bg-destructive/10 border border-destructive/20 px-4 py-3 text-sm text-destructive">
                {submitError}
              </div>
            )}

            {/* Building select */}
            <div className="space-y-2">
              <Label htmlFor="building_id">Immeuble *</Label>
              <Select
                value={formData.building_id}
                onValueChange={handleSelectChange("building_id")}
                disabled={isSubmitting || !!preselectedBuildingId}
              >
                <SelectTrigger id="building_id">
                  <SelectValue placeholder="Sélectionnez un immeuble" />
                </SelectTrigger>
                <SelectContent>
                  {buildings.map((building) => (
                    <SelectItem key={building.id} value={String(building.id)}>
                      {building.name} — {building.city}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Name */}
            <div className="space-y-2">
              <Label htmlFor="name">Nom de l&apos;équipement *</Label>
              <Input
                id="name"
                name="name"
                placeholder="Ascenseur principal"
                value={formData.name}
                onChange={handleChange}
                disabled={isSubmitting}
                required
              />
            </div>

            {/* Type */}
            <div className="space-y-2">
              <Label htmlFor="equipment_type">Type *</Label>
              <Select
                value={formData.equipment_type}
                onValueChange={handleSelectChange("equipment_type")}
                disabled={isSubmitting}
              >
                <SelectTrigger id="equipment_type">
                  <SelectValue placeholder="Sélectionnez un type" />
                </SelectTrigger>
                <SelectContent>
                  {EQUIPMENT_TYPES.map((type) => (
                    <SelectItem key={type} value={type}>
                      {type}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Serial number */}
            <div className="space-y-2">
              <Label htmlFor="serial_number">Numéro de série</Label>
              <Input
                id="serial_number"
                name="serial_number"
                placeholder="SN-12345-ABC"
                value={formData.serial_number}
                onChange={handleChange}
                disabled={isSubmitting}
              />
            </div>

            {/* Installation date */}
            <div className="space-y-2">
              <Label htmlFor="installation_date">Date d&apos;installation</Label>
              <Input
                id="installation_date"
                name="installation_date"
                type="date"
                value={formData.installation_date}
                onChange={handleChange}
                disabled={isSubmitting}
              />
            </div>

            {/* Actions */}
            <div className="flex justify-end gap-3 pt-4 border-t border-border">
              <Link
                href={
                  preselectedBuildingId
                    ? `/dashboard/buildings/${preselectedBuildingId}`
                    : "/dashboard/buildings"
                }
              >
                <Button type="button" variant="outline" disabled={isSubmitting}>
                  Annuler
                </Button>
              </Link>
              <Button
                type="submit"
                className="gap-2 bg-primary hover:bg-primary/90"
                disabled={isSubmitting}
              >
                {isSubmitting ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Création...
                  </>
                ) : (
                  <>
                    <Save className="h-4 w-4" />
                    Enregistrer
                  </>
                )}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
