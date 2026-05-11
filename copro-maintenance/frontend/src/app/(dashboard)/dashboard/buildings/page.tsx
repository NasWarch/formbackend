"use client";

import { useEffect, useState, useMemo } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import {
  Building2,
  Plus,
  Loader2,
  MapPin,
  Hash,
  Wrench,
  Search,
  AlertTriangle,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Card, CardContent } from "@/components/ui/card";
import api, { ApiError } from "@/lib/api";

interface Building {
  id: number;
  name: string;
  address: string;
  city: string;
  postal_code: string;
  nb_lots: number;
  equipment_count?: number;
  created_at?: string;
}

export default function BuildingsPage() {
  const [buildings, setBuildings] = useState<Building[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  // Dialog state
  const [dialogOpen, setDialogOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState("");
  const [formData, setFormData] = useState({
    name: "",
    address: "",
    city: "",
    postal_code: "",
    nb_lots: "",
  });

  // Fetch buildings
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

  // Filter buildings by search query
  const filteredBuildings = useMemo(() => {
    if (!searchQuery.trim()) return buildings;
    const q = searchQuery.toLowerCase();
    return buildings.filter(
      (b) =>
        b.name.toLowerCase().includes(q) ||
        b.address.toLowerCase().includes(q) ||
        b.city.toLowerCase().includes(q)
    );
  }, [searchQuery, buildings]);

  // Form handlers
  const handleFormChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
    if (submitError) setSubmitError("");
  };

  const handleCreateBuilding = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitError("");

    if (!formData.name || !formData.address || !formData.city) {
      setSubmitError("Veuillez remplir les champs obligatoires.");
      return;
    }

    setIsSubmitting(true);

    try {
      const created = await api.post<Building>("/buildings", {
        name: formData.name,
        address: formData.address,
        city: formData.city,
        postal_code: formData.postal_code || undefined,
        nb_lots: formData.nb_lots ? parseInt(formData.nb_lots, 10) : undefined,
      });

      setBuildings((prev) => [...prev, created]);
      setDialogOpen(false);
      setFormData({ name: "", address: "", city: "", postal_code: "", nb_lots: "" });
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
            Chargement des immeubles…
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
      {/* Page header */}
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-card-foreground">
            Immeubles
          </h1>
          <p className="mt-1 text-sm text-muted-foreground">
            {buildings.length} immeuble{buildings.length !== 1 ? "s" : ""} enregistré{buildings.length !== 1 ? "s" : ""}
          </p>
        </div>

        <Button
          onClick={() => setDialogOpen(true)}
          className="gap-2 bg-primary hover:bg-primary/90"
        >
          <Plus className="h-4 w-4" />
          Nouvel immeuble
        </Button>

        <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
          <DialogContent className="sm:max-w-md">
            <DialogHeader>
              <DialogTitle className="text-card-foreground">
                Nouvel immeuble
              </DialogTitle>
              <DialogDescription className="text-muted-foreground">
                Ajoutez une copropriété à votre portefeuille.
              </DialogDescription>
            </DialogHeader>

            <form onSubmit={handleCreateBuilding} className="space-y-4 mt-2">
              {submitError && (
                <div className="rounded-lg bg-destructive/10 border border-destructive/20 px-4 py-3 text-sm text-destructive">
                  {submitError}
                </div>
              )}

              <div className="space-y-2">
                <Label htmlFor="name">Nom de l&apos;immeuble *</Label>
                <Input
                  id="name"
                  name="name"
                  placeholder="Résidence Les Jardins"
                  value={formData.name}
                  onChange={handleFormChange}
                  disabled={isSubmitting}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="address">Adresse *</Label>
                <Input
                  id="address"
                  name="address"
                  placeholder="12 rue de la Paix"
                  value={formData.address}
                  onChange={handleFormChange}
                  disabled={isSubmitting}
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div className="space-y-2">
                  <Label htmlFor="city">Ville *</Label>
                  <Input
                    id="city"
                    name="city"
                    placeholder="Paris"
                    value={formData.city}
                    onChange={handleFormChange}
                    disabled={isSubmitting}
                    required
                  />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="postal_code">Code postal</Label>
                  <Input
                    id="postal_code"
                    name="postal_code"
                    placeholder="75000"
                    value={formData.postal_code}
                    onChange={handleFormChange}
                    disabled={isSubmitting}
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="nb_lots">Nombre de lots</Label>
                <Input
                  id="nb_lots"
                  name="nb_lots"
                  type="number"
                  placeholder="24"
                  value={formData.nb_lots}
                  onChange={handleFormChange}
                  disabled={isSubmitting}
                />
              </div>

              <div className="flex justify-end gap-3 pt-2">
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => setDialogOpen(false)}
                  disabled={isSubmitting}
                >
                  Annuler
                </Button>
                <Button
                  type="submit"
                  className="bg-primary hover:bg-primary/90"
                  disabled={isSubmitting}
                >
                  {isSubmitting ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Création...
                    </>
                  ) : (
                    "Créer"
                  )}
                </Button>
              </div>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      {/* Search */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground/70 pointer-events-none" />
        <Input
          placeholder="Rechercher par nom, adresse ou ville…"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="pl-10"
        />
      </div>

      {/* Buildings grid */}
      {filteredBuildings.length > 0 ? (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {filteredBuildings.map((building) => (
            <Link
              key={building.id}
              href={`/dashboard/buildings/${building.id}`}
              className="group"
            >
              <Card className="h-full border-border shadow-sm transition-all hover:shadow-md hover:border-primary/30">
                <CardContent className="p-5">
                  <div className="flex items-start gap-3">
                    <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-accent text-primary group-hover:bg-primary group-hover:text-primary-foreground transition-colors">
                      <Building2 className="h-5 w-5" />
                    </div>
                    <div className="min-w-0 flex-1">
                      <h3 className="font-semibold text-card-foreground group-hover:text-primary transition-colors truncate">
                        {building.name}
                      </h3>
                      <div className="mt-1.5 space-y-1">
                        <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
                          <MapPin className="h-3 w-3 shrink-0" />
                          <span className="truncate">
                            {building.address}
                            {building.postal_code && `, ${building.postal_code}`} {building.city}
                          </span>
                        </div>
                        <div className="flex items-center gap-3 text-xs text-muted-foreground/70">
                          <span className="flex items-center gap-1">
                            <Hash className="h-3 w-3" />
                            {building.nb_lots} lots
                          </span>
                          {building.equipment_count !== undefined && (
                            <span className="flex items-center gap-1">
                              <Wrench className="h-3 w-3" />
                              {building.equipment_count} équipement{building.equipment_count !== 1 ? "s" : ""}
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
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
          <Building2 className="h-12 w-12 text-muted-foreground/50" />
          <p className="mt-3 text-sm font-medium text-muted-foreground">
            {searchQuery
              ? "Aucun immeuble ne correspond à votre recherche."
              : "Aucun immeuble enregistré."}
          </p>
          <p className="mt-1 text-xs text-muted-foreground/70">
            {searchQuery
              ? "Essayez avec d&apos;autres termes."
              : "Ajoutez votre première copropriété."}
          </p>
          {!searchQuery && (
            <Button
              className="mt-4 gap-2 bg-primary hover:bg-primary/90"
              onClick={() => setDialogOpen(true)}
            >
              <Plus className="h-4 w-4" />
              Nouvel immeuble
            </Button>
          )}
        </motion.div>
      )}
    </div>
  );
}
