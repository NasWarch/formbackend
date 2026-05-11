# Monetization Lab — MVP Readiness Plan

> Proposé par TARZ, le 2026-05-07.
> Contexte : serveur ARM64 (aarch64), 4GB RAM, 10GB libre, Ubuntu 24.04.
> Infra existante : Docker, nginx (port 80 → tinystatus), PostgreSQL 15 + Redis 8.2 (Docker).

---

## 1. Stack Technique

| Couche | Choix | Justification |
|---|---|---|
| **Backend** | Python 3.11 + FastAPI | Déjà installé, excellent support async, compatible ARM64, écosystème Stripe mature. Pas de build native coûteux. |
| **Frontend** | HTMX + Jinja2 templates (FastAPI serve) | Aucun build step, pas de bundle JS, livré directement. Alternative future : Svelte 5 si besoin d'interactivité complexe. |
| **Base de données** | PostgreSQL 15 (existant via Docker) | Il tourne déjà sur l'hôte. Créer une DB `monetization` dans la même instance. |
| **Cache / Sessions** | Redis 8.2 (existant via Docker) | Déjà disponible. Utiliser pour : sessions utilisateur, rate limiting, file d'attente webhooks Stripe. |
| **ORM / Migrations** | SQLAlchemy 2.0 + Alembic | Standard FastAPI, migrations versionnées. |
| **Auth** | JWT (access + refresh) + magic links | Pas de gestion de mot de passe côté serveur. Stripe Customer Portal pour les infos de paiement. |
| **Déploiement** | Docker Compose (un conteneur backend) + nginx reverse proxy | Docker est déjà installé. Un seul conteneur à build → footprint mémoire minimal. |
| **CI** | Aucun pour le MVP — déploiement manuel via rsync + docker compose up -d | Trop tôt pour GitHub Actions. Ajouter quand le repo est sur GitHub. |

### Pourquoi pas d'autres stacks

- **Node/Express** : viable mais FastAPI a un meilleur écosystème Stripe + gestion async native.
- **Go/Rust** : overkill pour un MVP, coût de build/déploiement trop élevé.
- **Next.js** : nécessite Node runtime + build step, mémoire trop serrée (4GB RAM, 1.6GB disponible).
- **SQLite** : pas de connexions concurrentes fiables pour un SaaS, même en MVP.

---

## 2. Structure du Répertoire

```
/root/monetization-lab/
├── docker-compose.yml          # Services : backend, nginx (si standalone)
├── .env.example                 # Template de config
├── .gitignore
├── Makefile                     # Raccourcis : make dev, make migrate, make deploy
│
├── backend/
│   ├── Dockerfile               # Multi-stage, image ~200MB
│   ├── requirements.txt         # pin: fastapi, uvicorn, sqlalchemy, httpx, stripe, ...
│   ├── alembic.ini
│   ├── alembic/
│   │   ├── env.py
│   │   └── versions/           # Migrations auto-générées
│   └── app/
│       ├── __init__.py
│       ├── main.py              # App FastAPI, lifespan events
│       ├── core/
│       │   ├── __init__.py
│       │   ├── config.py        # Pydantic Settings (variables d'env)
│       │   ├── database.py      # SQLAlchemy engine + sessionmaker
│       │   ├── security.py      # JWT utils, password hashing
│       │   └── redis.py         # Redis client
│       ├── models/
│       │   ├── __init__.py
│       │   ├── user.py
│       │   └── subscription.py  # Plans, features, status
│       ├── schemas/
│       │   ├── __init__.py
│       │   ├── auth.py
│       │   └── billing.py
│       ├── api/
│       │   ├── __init__.py
│       │   ├── deps.py          # Dépendances : get_current_user, get_db
│       │   └── routes/
│       │       ├── __init__.py
│       │       ├── auth.py      # /auth/magic-link, /auth/verify, /auth/refresh
│       │       ├── users.py     # /users/me, /users/me/subscription
│       │       ├── billing.py   # /billing/portal (stripe redirect) — PAS IMPLÉMENTÉ ENCORE
│       │       └── webhooks.py  # Stripe webhook endpoint — PAS IMPLÉMENTÉ ENCORE
│       └── templates/           # Jinja2 : pages landing, dashboard, pricing
│           ├── base.html
│           ├── index.html
│           ├── dashboard.html
│           ├── pricing.html
│           └── login.html
│
├── nginx/
│   └── monetization-lab.conf.example  # Configuration nginx pour le sous-domaine
│
└── scripts/
    ├── deploy.sh                # Rsync + docker compose up -d
    ├── seed.py                  # Données de test (plans, admin user)
    └── backup-db.sh             # pg_dump vers backup dir
```

### Décisions architecturales clefs

- **Monorepo single-container backend** : Le frontend est servi par FastAPI (templates). Pas de séparation backend/frontend build → zéro complexité pour le MVP.
- **Alembic** : Migrations versionnées dès le jour 1. Impossible de faire du `Base.metadata.create_all()` en prod.
- **Pydantic Settings** : Toute la config (DB URL, Stripe keys, JWT secret) via variables d'environnement. `.env` jamais commité.
- **Pas d'async SQLAlchemy en MVP** : Sync SQLAlchemy + ThreadPoolExecutor. Asynchrone si besoin de perf plus tard — le gain en complexité ne vaut pas le coût au début.

---

## 3. Déploiement

### Architecture finale

```
Internet → nginx:443 (SSL) → backend:8000 (FastAPI/Uvicorn)
                                  ├── PostgreSQL:5432
                                  └── Redis:6379
```

### Chemin de déploiement (MVP)

1. **Configuration SSL** : Installer certbot, obtenir un certificat Let's Encrypt pour le sous-domaine.
2. **Sous-domaine** : Créer un enregistrement DNS A pointant vers l'IP du serveur.
3. **nginx** : Nouveau bloc server dans `/etc/nginx/sites-available/monetization-lab`, proxy pass vers le conteneur backend.
4. **Docker Compose** : Lancer le service backend. La DB et Redis sont déjà sur l'hôte — le backend s'y connecte via `host.docker.internal` ou l'IP du bridge Docker.
5. **Déploiement** : `rsync -avz --delete ./ backend-user@host:~/monetization-lab/ && ssh host 'cd ~/monetization-lab && docker compose up -d --build'`

**Pas de CI/CD pour le MVP.** Le script `scripts/deploy.sh` suffit. CI plus tard quand le projet est sur GitHub avec des tests.

### Considérations ARM64

- Toutes les images Docker doivent être multi-arch ou ARM64 natives.
- `python:3.11-slim-bookworm` existe en ARM64.
- Stripe SDK Python fonctionne sans build natif → aucune dépendance C problématique.

---

## 4. Analytics

**Recommandation : Umami (self-hosted).**

| Outil | Pourquoi |
|---|---|
| **Umami** | Image Docker légère (ARM64), zéro dépendance externe, respecte le RGPD, pas de cookie banner. |
| **Plausible** | Plus cher en ressources, image officielle pas toujours dispo en ARM64. |
| **Google Analytics** | Trop lourd, pas de self-hosting, obligations RGPD. |

Alternative plus légère : **Logs nginx + GoAccess** (analyse statique des logs) — zéro infrastructure supplémentaire.

Pour le MVP, ne pas déployer Umami tout de suite. Commencer par les logs nginx + GoAccess, ajouter Umami quand le trafic le justifie.

---

## 5. Auth & Payment Constraints

### Auth

- **Magic links** par email (POST `/auth/magic-link` → envoie un token par email → GET `/auth/verify?token=...` → JWT)
- **JWT** : access_token (15min) + refresh_token (7 jours, stocké en Redis)
- **Pas de mot de passe** : le mail est le seul identifiant. Simplifie la sécurité (pas de hash, pas de reset password).
- Rate limiting sur l'endpoint magic link (Redis + slowapi) : max 1 requête par email toutes les 60 secondes.

### Payment Constraints (documentation uniquement — PAS D'IMPLÉMENTATION)

Quand le moment viendra d'implémenter les paiements :

| Contrainte | Décision |
|---|---|
| **Processor** | Stripe (écosystème le plus mature, Customer Portal gère mises à jour CB). |
| **Pricing model** | Plans récurrents (Stripe Products + Prices). Pas de paiement one-shot pour le MVP. |
| **Webhooks** | Endpoint Stripe dédié, vérification HMAC. Queue Redis en cas d'échec. |
| **Customer Portal** | Rediriger l'utilisateur vers Stripe pour gérer son abonnement. Pas de UI de paiement custom. |
| **Monnaie** | EUR uniquement. Stripe convertit automatiquement pour les cartes étrangères. |
| **Trials** | Période d'essai optionnelle (Stripe trial_period_days). Stocker une date d'expiration locale. |
| **Feature gating** | Vérifier le statut abonnement à chaque requête côté backend. Modèle : `Subscription.status` (active / trialing / past_due / canceled). |
| **Taxes** | Stripe Tax ou calcul manuel selon le pays. Stripe Tax recommandé pour la simplicité. |

### Security

- **Rate limiting** sur tous les endpoints publics (SlowAPI + Redis)
- **CORS** : whitelist stricte (le domaine uniquement)
- **Headers** : helmet-style (X-Content-Type-Options, X-Frame-Options, CSP)
- **Stripe webhooks** : vérifier la signature HMAC côté serveur. Renvoyer 200 rapidement, traiter le webhook de manière asynchrone.

---

## 6. Human-Review Gates

| Gate | Condition | Qui |
|---|---|---|
| **Squelette du repo** | Structure validée, dépendances fixées | Toi (Nassim) — README relu et approuvé |
| **Route auth** | Magic link fonctionnel en local | Toi — test manuel |
| **Page pricing** | Design + contenu validé | Toi — pas de paiement derrière |
| **Staging deploy** | Premier déploiement sur sous-domaine de staging | Toi — accès vérifié |
| **Implémentation Stripe** | Architecture webhook + Customer Portal définie | Bloquant : revue de sécurité avant tout code de paiement en prod |
| **Passage en prod** | Tests manuels complets, backup DB automatisé | Toi + revue sécurité paiement |
| **Facturation réelle** | Stripe en mode live, pas en test | Toi + validation que les webhooks arrivent correctement |

### Règles strictes

1. **Aucun code Stripe en `main` sans revue.** Le branch `payment/` est isolé. Une PR est créée, et seulement toi (Nassim) la merge.
2. **Aucune clé Stripe live dans `.env`.** Uniquement les clés de test en dev. Les clés live sont injectées via une variable d'environnement sécurisée sur le serveur (ou un fichier `.env.prod` jamais commité).
3. **Backup DB obligatoire avant le premier webhook Stripe en prod.** Via `scripts/backup-db.sh` + cron.
4. **Rate limiting activé avant toute exposition publique.** Le premier lancement en dev n'en a pas besoin, mais le staging doit l'avoir.

---

## 7. Launch Assets (Templates Réutilisables)

Le dossier contient des templates de lancement prêts à l'emploi, adaptables à tout produit :

| Fichier | Contenu | Utilisation |
|---------|---------|-------------|
| `landing-page-structure.md` | Structure 7 sections + variations par objectif + tests A/B prévus | Avant d'écrire HTML — cadrer chaque section |
| `copy-checklist.md` | Checklist copy par type de contenu + anti-patterns + SEO | Avant toute rédaction de contenu public |
| `analytics-events-plan.md` | Événements par étape du cycle (acquisition → rétention) + implémentation technique | Dès la première mise en ligne — logs nginx en phase 1 |
| `outreach-channels-plan.md` | Canaux d'acquisition budget €0 + planning 4 semaines + cold email | Dès le lancement — calendrier des actions |
| `validation-experiments.md` | 8 expériences pré/post-lancement + tableau de décision | Avant d'écrire la première ligne de code |
| `pricing-test-plan.md` | Structure de plans + tests Van Westendorp + A/B pricing | Design uniquement — pas d'implémentation Stripe |
| `launch-governance.md` | Règles strictes : pas de paid ads, contrôles financiers, security gates, GDPR | Applicable immédiatement — document de référence |

### Règle clé : **No Paid Ads Before Human Approval**
Aucune dépense publicitaire sans validation explicite de Nassim. Les conditions d'approbation (PMF, unit economics, tracking) sont détaillées dans `launch-governance.md`.

---

## 8. Prochaines ÉTapes (Ordre d'Exécution)

1. [ ] **Read this plan** — Nassim valide ou ajuste
2. [ ] **Create skeleton** — `backend/app/` structure, `docker-compose.yml`, `requirements.txt`, `Makefile`
3. [ ] **Dockerfile** — Multi-stage Python 3.11-slim, ~200MB final image
4. [ ] **Config & DB** — `core/config.py` (Pydantic Settings), `core/database.py` (SQLAlchemy + Alembic init)
5. [ ] **Health endpoint** — `GET /health` → `{"status": "ok", "db": true, "redis": true}`
6. [ ] **Auth routes** — Magic link generation + JWT verify
7. [ ] **Page templates** — landing, login, dashboard with HTMX interactivity
8. [ ] **Nginx config** — Setup nginx + certbot for the domain
9. [ ] **Stripe integration design doc** — avant d'écrire une seule ligne de code de paiement
10. [ ] **Payment implementation** — dans une branche dédiée, PAS AVANT validation du design doc
