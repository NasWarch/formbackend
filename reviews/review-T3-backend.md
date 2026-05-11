# Review — Backend (T3) : Squelette FastAPI

Date de revue : 2026-05-07
Reviewer : TARZ (agent review)
Document source : /root/monetization-lab/backend/

---

## Résumé

| Dimension | Score | Commentaire court |
|-----------|-------|-------------------|
| A — Architecture & Organisation | 🟢 | Clean separation core/models/api/schemas. Bonne structure modulaire. |
| B — Sécurité & Authentification | 🟢 | JWT + magic links sans password stocké. Rate limiting slowapi + Redis. |
| C — Base de données & Modèles | 🟡 | SQLAlchemy sync bien structuré, mais Form data en mémoire FORMS_DB (pas persisté). |
| D — Code Quality & Tests | 🟡 | 2 fichiers de test (auth + health). Backend buildable via Docker. |
| E — Docker & Déploiement | 🟢 | Multi-stage ARM64, HEALTHCHECK, non-root user, build OK. |
| F — Contraintes RGPD/Sécurité | 🟡 | secret_key par défaut, cookies secure=False en dev. |
| G — **Adéquation produit** | 🔴 | **Le backend implémente une Form Backend API, pas le Monitoring Serveur Léger.** |

## Détail par critère

### A — Architecture & Organisation

| # | Critère | Résultat | Justification | Confiance |
|---|---------|----------|---------------|-----------|
| A1 | Structure FastAPI clean | 🟢 | main.py avec lifespan, limiter, CORS, routers montés proprement. | HIGH |
| A2 | Séparation core/models/api/schemas | 🟢 | 4 dossiers distincts, chaque module a une responsabilité unique. | HIGH |
| A3 | API router organisation | 🟢 | auth, users, billing, webhooks, health séparés. | HIGH |
| A4 | Configuration centralisée | 🟢 | Pydantic Settings avec .env support. | HIGH |
| A5 | Dépendances FastAPI propres | 🟢 | get_db, get_current_user bien factorisés dans api/deps.py. | HIGH |

### B — Sécurité & Authentification

| # | Critère | Résultat | Justification | Confiance |
|---|---------|----------|---------------|-----------|
| B1 | Magic link auth (no password) | 🟢 | Aucun mot de passe stocké. Magic link JWT 15 min. | HIGH |
| B2 | JWT access + refresh tokens | 🟢 | Access 15 min, refresh 7 jours. Types distincts (access/refresh/magic_link). | HIGH |
| B3 | Rate limiting global | 🟢 | Slowapi à 60 requêtes/minute. Redis backend. | HIGH |
| B4 | Rate limiting form submission | 🟡 | Fonctionne via attribut de fonction Python (submit_form._rate_cache) — fonctionnel mais non persistant et non distribué. | MED |
| B5 | CORS configurable | 🟢 | Via settings.cors_origins_list. | HIGH |
| B6 | Cookie secure=False (dev) | 🟡 | Commenté "True en production" — OK pour dev, mais peut être oublié en prod. | MED |

### C — Base de données & Modèles

| # | Critère | Résultat | Justification | Confiance |
|---|---------|----------|---------------|-----------|
| C1 | SQLAlchemy sync bien configuré | 🟢 | Engine + SessionLocal + get_db yield pattern. pool_pre_ping activé. | HIGH |
| C2 | Modèles : User, Plan, Subscription, Form, Submission | 🟢 | Relations FK, indexes, contraintes d'unicité. | HIGH |
| C3 | Alembic migration initiale | 🟢 | 5 tables créées, indexes, FK, enum SubscriptionStatus. | HIGH |
| C4 | **FORMS_DB in-memory dict** | 🔴 | Toute la logique métier des formulaires utilise un dict global en mémoire. Perte des données au redémarrage. FORMS_DB contourne complètement SQLAlchemy. | HIGH |
| C5 | JSONB pour submissions.data | 🟢 | Bon choix pour données hétérogènes. | HIGH |
| C6 | after_insert listener sur Submission | 🟡 | Élégant mais peut causer des surprises avec l'auto-commit. | MED |

### D — Code Quality & Tests

| # | Critère | Résultat | Justification | Confiance |
|---|---------|----------|---------------|-----------|
| D1 | Tests unitaires | 🟡 | 2 fichiers : test_auth.py (104 lignes), test_health.py (35 lignes). Coverage partiel. | MED |
| D2 | Test coverage auth | 🟢 | Magic link flow : création, existing, email invalide, verify, expired, refresh, protected endpoint. Bonne couverture. | HIGH |
| D3 | Tests health endpoint | 🟢 | 4 tests : status 200, fields, db check, status logic. | HIGH |
| D4 | Pas de test sur forms/endpoints métier | 🔴 | Aucun test pour les endpoints /api/forms, create, delete, submissions, embed. | HIGH |
| D5 | Code commenté (docstrings) | 🟢 | Tous les modules et endpoints ont des docstrings en français. | HIGH |
| D6 | Type hints | 🟢 | Usage systématique de type hints. | HIGH |

### E — Docker & Déploiement

| # | Critère | Résultat | Justification | Confiance |
|---|---------|----------|---------------|-----------|
| E1 | Docker build successful | 🟢 | `docker compose build` passe sans erreur. | HIGH |
| E2 | Multi-stage ARM64 | 🟢 | Python 3.11-slim-bookworm, builder pattern. | HIGH |
| E3 | Non-root user | 🟢 | appuser:appuser (UID 1001). | HIGH |
| E4 | HEALTHCHECK | 🟢 | curl http://localhost:8000/health, interval 30s. | HIGH |
| E5 | docker-compose avec healthcheck | 🟢 | Défini, host.docker.internal pour DB/Redis. | HIGH |
| E6 | Pas de service DB/Redis dans docker-compose | 🟡 | Dépend de PostgreSQL et Redis sur l'hôte via host.docker.internal. Fonctionnel mais pas self-contained. | MED |
| E7 | Makefile complet | 🟢 | dev, build, up, down, migrate, migration, backup, clean. | HIGH |

### F — Points de blocage obligatoires

| # | Point | Résultat | Détail |
|---|-------|----------|--------|
| F1 | Aucun code Stripe en prod | ✅ PASS | billing.py et webhooks.py sont des stubs (commentés, "PAS IMPLÉMENTÉ"). Stripe n'est pas importé dans main.py. |
| F2 | Aucune clé API live dans .env/code | ✅ PASS | .env.example contient des valeurs par défaut "change-me", *** pour les mots de passe. Aucune clé réelle. |
| F3 | Aucune donnée client réelle en dev | ✅ PASS | Pas de seed data, pas de données réelles. |
| F4 | Rate limiting activé | ✅ PASS | Slowapi à 60/min + rate limiting custom sur form submission. |
| F5 | Backup DB automatisé | ⚠️ CONDITIONNEL | Script scripts/backup-db.sh existe (pg_dump + retention 30j). Makefile a target `backup`. Mais PAS de cron configuré : le script dit "À mettre en cron" sans confirmation. |
| F6 | Backend buildable et démarrable | ✅ PASS | Docker build réussi. Image produite sans erreur. |
| F7 | Aucun tracker tiers sans consentement | ✅ PASS | Aucun tracker tiers dans le backend. Pas de GA, pas de scripts externes. |

### G — **Problème Critique : Scope Mismatch**

| # | Point | Résultat | Détail |
|---|-------|----------|--------|
| G1 | **Produit implémenté vs produit sélectionné** | 🔴 CRITICAL FAIL | **L'opportunité sélectionnée est "Monitoring Serveur Léger"** (checks uptime/HTTP/ping/TCP, notifications), **mais le backend implémente une "Form Backend API"** (form builder, submissions, embed). |
| G2 | Preuve | — | `main.py` L2 : `"""MVP product: Form Backend API (form backend as a service)."""` Le code entier (FORMS_DB, /api/forms, /api/f/{endpoint}) est dédié aux formulaires, pas au monitoring. |
| G3 | Composants manquants | — | Aucun modèle Monitor/Check/Incident. Aucun moteur de checks asynchrone (Redis + asyncio). Aucune notification (email/Slack/Telegram). Aucun endpoint de check HTTP/ping/TCP. RIEN de ce qui est spécifié dans selected-opportunity.md §MVP Scope. |
| G4 | Contradiction frontend | — | Les templates HTML parlent de "Monito — Monitoring Serveur Léger" mais le backend sert des formulaires. Les utilisateurs verraient un monitoring dashboard contenant des formulaires. |

## RED flags déclenchés

| # Critère | Type | Description | Bloque la décision ? |
|-----------|------|-------------|----------------------|
| G1 | 🔴 Scope Mismatch | Backend implémente le mauvais produit (Form Backend API au lieu de Monitoring Serveur Léger) | OUI |
| C4 | 🟡 Data Loss | FORMS_DB in-memory : perte totale des données au redémarrage | NON (MVP) |
| D4 | 🟡 Test Coverage | Aucun test sur les endpoints métier forms | NON |

## Contre-mesures anti-bullshit appliquées

| Pattern | Présent ? | Détail |
|---------|-----------|--------|
| "Selon une étude récente" sans nom | Non | N/A |
| "Marché estimé à X milliards" sans source | Non | N/A |
| "Notre seul concurrent" faux | Non | N/A |
| Aucune date sur les chiffres | Non | N/A |
| Courbe exponentielle sur marché mature | Non | N/A |
| "Aucun risque" ou "risque faible" | Non | N/A |
| MVP 12+ mois sans justification | Non | N/A |
| "On fera du ML" vague | Non | N/A |
| Partenariat Big Tech non confirmé | Non | N/A |
| "Parlé à 50 clients" sans détails | Non | N/A |
| "1% du marché suffit" (fallacie) | Non | N/A |
| Aucun concurrent listé | Non | N/A |
| Viralité supposée sans mécanique | Non | N/A |

## Recommandations

1. **CRITIQUE — Corriger le scope** : Le backend doit implémenter le Monitoring Serveur Léger (checks HTTP/Ping/TCP, notifications, incident timeline). Le code Form Backend API existant (FORMS_DB, /api/forms) est un dead end — soit supprimé, soit déplacé dans une branche séparée.

2. **Persister les données en base** : Remplacer FORMS_DB in-memory par des écritures SQLAlchemy dans la table `submissions` correctement modélisée.

3. **Tester les endpoints métier** : Ajouter des tests pour les routes /api/forms et /api/f/{endpoint}.

4. **Configurer le cron de backup** : Ajouter la tâche cron pour scripts/backup-db.sh dans le Makefile ou un playbook d'install.

5. **Sécuriser les cookies** : Rendre secure=True conditionnel via environment variable plutôt qu'un commentaire.

---

*Grille remplie selon /root/monetization-lab/review-checklist.md version 2.0*
