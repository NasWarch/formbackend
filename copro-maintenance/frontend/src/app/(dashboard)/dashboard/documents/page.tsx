"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import {
  FileText,
  Upload,
  Loader2,
  AlertTriangle,
  Download,
  Trash2,
  Image,
  File,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import api, { ApiError, getToken } from "@/lib/api";

interface Document {
  id: number;
  original_name: string;
  content_type: string;
  size: number;
  uploaded_at: string;
}

function formatFileSize(bytes: number): string {
  if (bytes === 0) return "0 o";
  const k = 1024;
  const sizes = ["o", "Ko", "Mo", "Go"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + " " + sizes[i];
}

function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleDateString("fr-FR", {
    day: "numeric",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function getFileIcon(contentType: string) {
  if (contentType.startsWith("image/")) return Image;
  if (contentType.includes("pdf")) return FileText;
  return File;
}

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export default function DocumentsPage() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");
  const [uploadOpen, setUploadOpen] = useState(false);
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadError, setUploadError] = useState("");
  const [downloadError, setDownloadError] = useState("");

  useEffect(() => {
    fetchDocuments();
  }, []);

  async function fetchDocuments() {
    try {
      const data = await api.get<Document[]>("/documents");
      setDocuments(data);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message || "Erreur lors du chargement des documents.");
      } else {
        setError("Impossible de contacter le serveur.");
      }
    } finally {
      setIsLoading(false);
    }
  }

  async function handleUpload(e: React.FormEvent) {
    e.preventDefault();
    if (!uploadFile) return;

    setIsUploading(true);
    setUploadError("");

    try {
      const token = localStorage.getItem("token");
      const formData = new FormData();
      formData.append("file", uploadFile);

      const response = await fetch(`${API_BASE_URL}/documents/upload`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      if (!response.ok) {
        const data = await response.json().catch(() => ({}));
        throw new Error(
          (data as { detail?: string })?.detail || "Erreur lors de l'upload"
        );
      }

      setUploadOpen(false);
      setUploadFile(null);
      await fetchDocuments();
    } catch (err) {
      setUploadError(
        err instanceof Error ? err.message : "Erreur lors de l'upload."
      );
    } finally {
      setIsUploading(false);
    }
  }

  const handleDownload = async (doc: Document) => {
    const token = getToken();
    try {
      const response = await fetch(`${API_BASE_URL}/documents/${doc.id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!response.ok) throw new Error("Download failed");
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      window.open(url, "_blank");
      setTimeout(() => URL.revokeObjectURL(url), 60000);
    } catch {
      setDownloadError("Impossible de télécharger le document.");
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
            Chargement des documents…
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
            Documents
          </h1>
          <p className="mt-1 text-sm text-muted-foreground">
            {documents.length} document{documents.length !== 1 ? "s" : ""} {" "}
            importé{documents.length !== 1 ? "s" : ""}
          </p>
        </div>

        <Button
          onClick={() => setUploadOpen(true)}
          className="gap-2 bg-primary hover:bg-primary/90"
        >
          <Upload className="h-4 w-4" />
          Importer un document
        </Button>

        <Dialog open={uploadOpen} onOpenChange={setUploadOpen}>
          <DialogContent className="sm:max-w-md">
            <DialogHeader>
              <DialogTitle className="text-card-foreground">
                Importer un document
              </DialogTitle>
              <DialogDescription className="text-muted-foreground">
                Téléversez un rapport de contrôle, certificat ou facture.
              </DialogDescription>
            </DialogHeader>

            <form onSubmit={handleUpload} className="space-y-4 mt-2">
              {uploadError && (
                <div className="rounded-lg bg-destructive/10 border border-destructive/20 px-4 py-3 text-sm text-destructive">
                  {uploadError}
                </div>
              )}

              <div className="space-y-2">
                <Label htmlFor="file">Fichier</Label>
                <Input
                  id="file"
                  type="file"
                  onChange={(e) => setUploadFile(e.target.files?.[0] || null)}
                  disabled={isUploading}
                  required
                />
                <p className="text-xs text-muted-foreground/70">
                  Formats acceptés : PDF, images, documents
                </p>
              </div>

              <div className="flex justify-end gap-3 pt-2">
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => {
                    setUploadOpen(false);
                    setUploadFile(null);
                    setUploadError("");
                  }}
                  disabled={isUploading}
                >
                  Annuler
                </Button>
                <Button
                  type="submit"
                  className="bg-primary hover:bg-primary/90"
                  disabled={isUploading || !uploadFile}
                >
                  {isUploading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Importation...
                    </>
                  ) : (
                    "Importer"
                  )}
                </Button>
              </div>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      {/* Documents table */}
      {documents.length > 0 ? (
        <Card className="border-border shadow-sm">
          <CardContent className="p-0">
            <Table>
              <TableHeader>
                <TableRow className="bg-muted/50">
                  <TableHead className="text-xs font-semibold uppercase text-muted-foreground">
                    Nom
                  </TableHead>
                  <TableHead className="text-xs font-semibold uppercase text-muted-foreground">
                    Type
                  </TableHead>
                  <TableHead className="text-xs font-semibold uppercase text-muted-foreground">
                    Taille
                  </TableHead>
                  <TableHead className="text-xs font-semibold uppercase text-muted-foreground">
                    Date d&apos;import
                  </TableHead>
                  <TableHead className="w-20 text-right text-xs font-semibold uppercase text-muted-foreground">
                    Actions
                  </TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {documents.map((doc) => {
                  const Icon = getFileIcon(doc.content_type);
                  return (
                    <TableRow key={doc.id} className="hover:bg-muted/50">
                      <TableCell>
                        <div className="flex items-center gap-3">
                          <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-accent text-primary">
                            <Icon className="h-4 w-4" />
                          </div>
                          <span className="text-sm font-medium text-card-foreground truncate max-w-[300px]">
                            {doc.original_name}
                          </span>
                        </div>
                      </TableCell>
                      <TableCell className="text-sm text-muted-foreground">
                        {doc.content_type}
                      </TableCell>
                      <TableCell className="text-sm text-muted-foreground">
                        {formatFileSize(doc.size)}
                      </TableCell>
                      <TableCell className="text-sm text-muted-foreground">
                        {formatDate(doc.uploaded_at)}
                      </TableCell>
                      <TableCell className="text-right">
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleDownload(doc)}
                          className="text-muted-foreground hover:text-primary"
                          title="Télécharger"
                        >
                          <Download className="h-4 w-4" />
                        </Button>
                      </TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      ) : (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
          className="flex flex-col items-center justify-center rounded-xl border border-dashed border-muted-foreground/30 bg-card py-20"
        >
          <FileText className="h-12 w-12 text-muted-foreground/50" />
          <p className="mt-3 text-sm font-medium text-muted-foreground">
            Aucun document importé
          </p>
          <p className="mt-1 text-xs text-muted-foreground/70">
            Importez vos rapports de contrôle, certificats et factures.
          </p>
          <Button
            className="mt-4 gap-2 bg-primary hover:bg-primary/90"
            onClick={() => setUploadOpen(true)}
          >
            <Upload className="h-4 w-4" />
            Importer un document
          </Button>
        </motion.div>
      )}
    </div>
  );
}
