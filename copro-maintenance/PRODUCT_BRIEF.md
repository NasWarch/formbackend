# CoproMaintenance — Product Brief

## Vision
Le carnet d'entretien digital pour les copropriétés françaises. SaaS B2B qui aide les syndics (professionnels et bénévoles) à gérer la maintenance réglementaire obligatoire : ascenseurs, chaudières, extincteurs, portes automatiques, etc.

## Problème
- **Obligation légale** : La loi ALUR (2014) et le décret 2016-1671 imposent un carnet d'entretien numérique à toutes les copropriétés de France.
- **Douleur** : Les syndics utilisent Excel, du papier, ou des ERP lourds (Yardi, MRI) à 200€+/mois inabordables pour les petites copropriétés.
- **Risque** : Défaut de suivi = non-conformité, litiges copropriétaires, responsabilité engagée.

## Solution
Plateforme SaaS avec :
1. **Carnet d'entretien digital** — Un équipement = une fiche avec historique des contrôles
2. **Calendrier intelligent** — Planification des visites obligatoires avec alertes email
3. **Upload documents** — Rapports de contrôle, certificats, factures attachés aux équipements
4. **Dashboard syndic** — Vue d'ensemble des immeubles gérés, conformité en temps réel

## Marché
- **TAM** : 22 Md$ (property management software mondial)
- **SAM** : France — 30 000 syndics × 50-100€/mois ≈ 25-35 M$
- **Cible** : Petits syndics professionnels (10-50 immeubles) + syndics bénévoles

## Concurrents
| Concurrent | Pricing | Position |
|---|---|---|
| Yardi, MRI | 200€+/mois | Enterprise, trop lourd |
| SyndicOne | 80€/mois | Module CRM, pas spécialisé maintenance |
| **CoproMaintenance** | **29-59€/mois** | **Low-cost, auto-service, spécialisé** |

## Pricing cible
- **Starter** 29€/mois — jusqu'à 5 lots
- **Pro** 59€/mois — jusqu'à 20 lots
- **Agence** 99€/mois — lots illimités

## Stack technique
- **Backend** : FastAPI + SQLAlchemy + SQLite (MVP) → PostgreSQL (scale)
- **Frontend** : Next.js + Tailwind CSS + shadcn/ui + lucide-react
- **Auth** : JWT
- **Déploiement** : Serveur dédié (Nginx + systemd)
- **Stockage** : Local filesystem (documents)

## Roadmap MVP (6 semaines)

### Semaine 1-2 : Fondation
- Backend API : équipements CRUD, contrôles CRUD, immeubles CRUD
- Frontend : layout, auth (login/register), dashboard basique

### Semaine 3-4 : Coeur métier
- Calendrier de maintenance avec récurrences obligatoires
- Upload de documents (rapports de contrôle, certificats)
- Système d'alertes email

### Semaine 5 : Dashboard & Compliance
- Vue conformité par immeuble
- Statuts : OK / À prévoir / En retard
- Vue calendrier (type agenda)

### Semaine 6 : Landing & Finitions
- Landing page vitrine (Next.js SSG)
- Pages pricing, fonctionnalités
- Documentation utilisateur
- Déploiement production
