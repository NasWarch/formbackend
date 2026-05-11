"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import {
  Building2,
  Wrench,
  ShieldCheck,
  CalendarCheck,
  FileText,
  Bell,
  ArrowRight,
  CheckCircle2,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const features = [
  {
    icon: Building2,
    title: "Gestion multi-immeubles",
    description:
      "Centralisez tous vos immeubles dans un tableau de bord unique. Accédez aux données de chaque copropriété en un clic.",
    tint: "bg-primary/5",
    iconColor: "text-primary",
  },
  {
    icon: Wrench,
    title: "Suivi des équipements",
    description:
      "Inventaire complet de vos équipements avec statuts de conformité : conforme, à prévoir, en retard. Filtrez par type, marque ou localisation.",
    tint: "bg-amber-50",
    iconColor: "text-amber-600",
  },
  {
    icon: CalendarCheck,
    title: "Planning intelligent",
    description:
      "Calendrier des maintenances préventives avec alertes anticipées. Anticipez les contrôles obligatoires et gérez les interventions.",
    tint: "bg-blue-50",
    iconColor: "text-blue-600",
  },
  {
    icon: FileText,
    title: "Documents centralisés",
    description:
      "Stockez et retrouvez tous vos documents réglementaires : contrats, PV d'AG, rapports de contrôle, factures. Classement automatique par équipement.",
    tint: "bg-purple-50",
    iconColor: "text-purple-600",
  },
  {
    icon: Bell,
    title: "Alertes & notifications",
    description:
      "Recevez des alertes par email avant chaque échéance réglementaire. Ne manquez plus un contrôle obligatoire ou une date butoir.",
    tint: "bg-primary/5",
    iconColor: "text-primary",
  },
  {
    icon: ShieldCheck,
    title: "Conformité réglementaire",
    description:
      "Suivez les obligations légales : ascenseurs, chaudières, extincteurs, contrôle d'accès. Générez votre carnet d'entretien obligatoire.",
    tint: "bg-amber-50",
    iconColor: "text-amber-600",
  },
];

const steps = [
  {
    number: "01",
    title: "Créez votre compte",
    description:
      "Inscrivez-vous en 30 secondes. Ajoutez votre première copropriété et commencez à inventorier vos équipements.",
  },
  {
    number: "02",
    title: "Importez vos données",
    description:
      "Ajoutez vos équipements, contrats et échéances. Notre assistant vous guide pas à pas pour structurer votre carnet d'entretien.",
  },
  {
    number: "03",
    title: "Pilotez votre maintenance",
    description:
      "Visualisez l'état de conformité en temps réel. Recevez des alertes automatiques et gardez l'esprit tranquille.",
  },
];

const container = {
  hidden: {},
  show: { transition: { staggerChildren: 0.1 } },
};
const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 },
};
const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 },
};

const EASE = [0.22, 1, 0.36, 1] as const;
const DURATION = 0.4;

export default function LandingPage() {
  return (
    <>
      {/* ===== HERO SECTION ===== */}
      <section className="relative overflow-hidden bg-gradient-to-b from-gray-950 via-primary to-gray-950">
        {/* Subtle pattern overlay */}
        <div
          className="absolute inset-0 opacity-[0.03]"
          style={{
            backgroundImage:
              "radial-gradient(circle at 1px 1px, #ffffff 1px, transparent 0)",
            backgroundSize: "40px 40px",
          }}
        />

        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, ease: EASE }}
          className="relative container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-24 sm:py-32 lg:py-40"
        >
          <div className="mx-auto max-w-3xl text-center">
            <Badge
              variant="outline"
              className="mb-6 border-amber-600/40 text-amber-600 bg-amber-600/5 px-4 py-1 text-xs font-medium tracking-wider uppercase"
            >
              Carnet d&apos;entretien digital
            </Badge>

            <h1 className="text-4xl font-medium tracking-tight text-white sm:text-5xl lg:text-6xl leading-[1.05]">
              La gestion de maintenance
              <br />
              <span className="text-amber-600">simplifiée et conforme</span>
            </h1>

            <p className="mt-6 text-lg leading-relaxed text-muted-foreground/70 max-w-2xl mx-auto">
              Centralisez le suivi des équipements, la planification des contrôles
              obligatoires et la conformité réglementaire de vos copropriétés sur
              une plateforme unique, pensée pour les syndics professionnels et
              bénévoles.
            </p>

            <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
              <Button
                size="lg"
                className="w-full sm:w-auto h-12 px-8 text-base bg-primary hover:bg-primary/90"
                render={<Link href="/register" />}
              >
                Démarrer gratuitement
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
              <Button
                variant="secondary"
                size="lg"
                className="w-full sm:w-auto h-12 px-8 text-base bg-white/10 hover:bg-white/15 text-white border-white/20"
                render={<Link href="#features" />}
              >
                Découvrir les fonctionnalités
              </Button>
            </div>

            <p className="mt-6 text-sm text-muted-foreground">
              Essai gratuit de 14 jours · Sans engagement · Sans carte bancaire
            </p>
          </div>
        </motion.div>
      </section>

      {/* ===== FEATURES SECTION ===== */}
      <section id="features" className="py-20 sm:py-28 bg-white">
        <div className="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-2xl text-center mb-16">
            <Badge
              variant="secondary"
              className="mb-4 bg-accent text-primary hover:bg-accent/80 px-3 py-1 text-xs font-medium"
            >
              Fonctionnalités
            </Badge>
            <h2 className="text-3xl font-semibold tracking-tight text-card-foreground sm:text-4xl">
              Tout ce dont vous avez besoin pour
              <br />
              gérer vos copropriétés
            </h2>
            <p className="mt-4 text-base text-muted-foreground leading-relaxed">
              De l&apos;inventaire des équipements à la conformité réglementaire,
              CoproMaintenance couvre l&apos;ensemble des besoins des syndics.
            </p>
          </div>

          <motion.div
            variants={container}
            initial="hidden"
            whileInView="show"
            viewport={{ once: true, margin: "-80px" }}
            className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3"
          >
            {features.map((feature) => (
              <motion.div key={feature.title} variants={item}>
                <Card className="group border border-border hover:border-muted-foreground/30 transition-all duration-200 hover:shadow-md">
                  <CardContent className="p-6 sm:p-8">
                    <div
                      className={`inline-flex h-12 w-12 items-center justify-center rounded-xl ${feature.tint} mb-5 group-hover:scale-105 transition-transform`}
                    >
                      <feature.icon className={`h-6 w-6 ${feature.iconColor}`} />
                    </div>
                    <h3 className="text-lg font-semibold text-foreground mb-2">
                      {feature.title}
                    </h3>
                    <p className="text-sm text-muted-foreground leading-relaxed">
                      {feature.description}
                    </p>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* ===== HOW IT WORKS SECTION ===== */}
      <section id="how-it-works" className="py-20 sm:py-28 bg-muted/30">
        <div className="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-2xl text-center mb-16">
            <Badge
              variant="secondary"
              className="mb-4 bg-accent text-primary hover:bg-accent/80 px-3 py-1 text-xs font-medium"
            >
              Démarrage
            </Badge>
            <h2 className="text-3xl font-semibold tracking-tight text-card-foreground sm:text-4xl">
              Opérationnel en trois étapes
            </h2>
            <p className="mt-4 text-base text-muted-foreground leading-relaxed">
              Pas de formation complexe, pas de déploiement lourd.
              Vous êtes prêt en moins de 10 minutes.
            </p>
          </div>

          <motion.div
            variants={container}
            initial="hidden"
            whileInView="show"
            viewport={{ once: true, margin: "-80px" }}
            className="grid grid-cols-1 gap-8 lg:grid-cols-3"
          >
            {steps.map((step, idx) => (
              <motion.div key={step.number} variants={item} className="relative flex flex-col items-center text-center">
                {/* Step connector line (desktop) */}
                {idx < steps.length - 1 && (
                  <div className="hidden lg:block absolute top-9 left-[calc(50%+3rem)] w-[calc(100%-6rem)] h-px bg-border" />
                )}

                <div className="inline-flex h-16 w-16 items-center justify-center rounded-2xl bg-primary text-white text-xl font-semibold mb-6 shadow-lg shadow-primary/20">
                  {step.number}
                </div>

                <h3 className="text-lg font-semibold text-foreground mb-3">
                  {step.title}
                </h3>
                <p className="text-sm text-muted-foreground leading-relaxed max-w-xs">
                  {step.description}
                </p>
              </motion.div>
            ))}
          </motion.div>

          {/* Trust indicators */}
          <div className="mt-16 flex flex-wrap items-center justify-center gap-6 text-sm text-muted-foreground">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-primary" />
              <span>Conforme à la loi ALUR</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-primary" />
              <span>Hébergé en France (Scaleway)</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-primary" />
              <span>Support téléphonique dédié</span>
            </div>
          </div>
        </div>
      </section>

      {/* ===== FINAL CTA SECTION ===== */}
      <section className="py-20 sm:py-28 bg-gradient-to-b from-background to-muted">
        <div className="container mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: "-80px" }}
            transition={{ duration: DURATION, ease: EASE }}
            className="mx-auto max-w-2xl text-center"
          >
            <Badge
              variant="secondary"
              className="mb-4 bg-accent text-primary hover:bg-accent/80 px-3 py-1 text-xs font-medium"
            >
              Prêt à commencer ?
            </Badge>
            <h2 className="text-3xl font-semibold tracking-tight text-card-foreground sm:text-4xl">
              Prenez le contrôle de vos
              <br />
              maintenances dès aujourd&apos;hui
            </h2>
            <p className="mt-4 text-base text-muted-foreground leading-relaxed">
              Rejoignez les syndics qui font confiance à CoproMaintenance pour la
              gestion de leurs copropriétés. Essai gratuit de 14 jours, sans
              engagement.
            </p>

            <div className="mt-10">
              <Button
                size="lg"
                className="h-12 px-10 text-base bg-primary hover:bg-primary/90 shadow-lg shadow-primary/25"
                render={<Link href="/register" />}
              >
                Créer mon compte gratuit
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
              <p className="mt-4 text-sm text-muted-foreground">
                Déjà inscrit ?{" "}
                <Link
                  href="/login"
                  className="font-medium text-primary hover:text-primary/80 underline underline-offset-2"
                >
                  Connectez-vous
                </Link>
              </p>
            </div>
          </motion.div>
        </div>
      </section>
    </>
  );
}
