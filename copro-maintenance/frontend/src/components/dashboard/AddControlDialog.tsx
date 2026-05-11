"use client";

import { useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Plus, Loader2 } from "lucide-react";
import api, { ApiError } from "@/lib/api";

interface AddControlDialogProps {
  equipmentId: number | string;
  onSuccess?: () => void;
}

export default function AddControlDialog({
  equipmentId,
  onSuccess,
}: AddControlDialogProps) {
  const [open, setOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [formData, setFormData] = useState({
    control_date: "",
    provider_name: "",
    result: "",
    notes: "",
  });

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
    if (error) setError("");
  };

  const handleSelectChange = (value: string | null) => {
    if (value === null) return;
    setFormData((prev) => ({ ...prev, result: value }));
    if (error) setError("");
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!formData.control_date || !formData.result) {
      setError("Veuillez remplir les champs obligatoires.");
      return;
    }

    setIsLoading(true);

    try {
      await api.post("/maintenance", {
        equipment_id: equipmentId,
        control_date: formData.control_date,
        provider_name: formData.provider_name || undefined,
        result: formData.result,
        notes: formData.notes || undefined,
      });

      setOpen(false);
      setFormData({
        control_date: "",
        provider_name: "",
        result: "",
        notes: "",
      });
      onSuccess?.();
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message || "Une erreur est survenue.");
      } else {
        setError("Impossible de contacter le serveur.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <Button onClick={() => setOpen(true)} className="gap-2 bg-primary hover:bg-primary/90">
        <Plus className="h-4 w-4" />
        Ajouter un contrôle
      </Button>
      <Dialog open={open} onOpenChange={setOpen}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle className="text-card-foreground">
            Nouveau contrôle
          </DialogTitle>
          <DialogDescription className="text-muted-foreground">
            Enregistrez un contrôle de maintenance pour cet équipement.
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-4 mt-2">
          {error && (
            <div className="rounded-lg bg-destructive/10 border border-destructive/20 px-4 py-3 text-sm text-destructive">
              {error}
            </div>
          )}

          {/* Date du contrôle */}
          <div className="space-y-2">
            <Label htmlFor="control_date">Date du contrôle *</Label>
            <Input
              id="control_date"
              name="control_date"
              type="date"
              value={formData.control_date}
              onChange={handleChange}
              required
              disabled={isLoading}
            />
          </div>

          {/* Prestataire */}
          <div className="space-y-2">
            <Label htmlFor="provider_name">Prestataire</Label>
            <Input
              id="provider_name"
              name="provider_name"
              type="text"
              placeholder="Nom du prestataire"
              value={formData.provider_name}
              onChange={handleChange}
              disabled={isLoading}
            />
          </div>

          {/* Résultat */}
          <div className="space-y-2">
            <Label htmlFor="result">Résultat *</Label>
            <Select
              value={formData.result}
              onValueChange={handleSelectChange}
              disabled={isLoading}
            >
              <SelectTrigger id="result">
                <SelectValue placeholder="Sélectionnez un résultat" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="ok">Conforme</SelectItem>
                <SelectItem value="issue">Anomalie détectée</SelectItem>
                <SelectItem value="partial">Partiellement conforme</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Notes */}
          <div className="space-y-2">
            <Label htmlFor="notes">Notes</Label>
            <Textarea
              id="notes"
              name="notes"
              placeholder="Observations, recommandations..."
              value={formData.notes}
              onChange={handleChange}
              rows={3}
              disabled={isLoading}
            />
          </div>

          <div className="flex justify-end gap-3 pt-2">
            <Button
              type="button"
              variant="outline"
              onClick={() => setOpen(false)}
              disabled={isLoading}
            >
              Annuler
            </Button>
            <Button
              type="submit"
              className="bg-primary hover:bg-primary/90"
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Enregistrement...
                </>
              ) : (
                "Enregistrer"
              )}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
    </>
  );
}
