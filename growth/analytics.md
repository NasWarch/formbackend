# Plan Analytics — Form Backend API

> Mise à jour : 2026-05-09 — Adapté de Monitoring Serveur Léger vers Form Backend API
> Pas de Google Analytics (RGPD + poids)
> Priorité : léger, RGPD-compliant, auto-hébergé
> Budget : 0 € (sur l'infra existante)

---

## Stack Recommandé en Deux Phases

### Phase 1 — MVP (J1 à J90) : nginx + GoAccess

**GoAccess** est déjà installé et fonctionnel sur le serveur.

| Outil | Setup | Coût | Données |
|-------|-------|------|---------|
| **GoAccess** (rapports temps réel) | Lit les logs nginx. Rapport HTML généré en temps réel | 0 € | Pages vues, visiteurs uniques, referrers, user agents, 404, temps de réponse |
| **Stripe Dashboard** | Intégré Stripe — 0 setup supplémentaire | 0 € | MRR, churn, nouveaux paiements, revenus |
| **Custom DB Queries** (PostgreSQL) | Requêtes SQL directes sur la base produit | 0 € | Utilisateurs, formulaires créés, soumissions, conversions |

**Configuration GoAccess recommandée :**

```nginx
# Dans /etc/nginx/sites-available/formapi
location /analytics {
    auth_basic "Analytics";
    auth_basic_user_file /etc/nginx/.htpasswd-analytics;
    alias /var/www/html/report.html;
}
```

GoAccess en mode real-time :
```bash
goaccess /var/log/nginx/formapi.access.log \
    --log-format=COMBINED \
    -o /var/www/html/report.html \
    --real-time-html \
    --daemonize
```

### Phase 2 — Post-MVP (J90+) : Umami Self-Hosted

| Outil | Setup | Coût | Données supplémentaires |
|-------|-------|------|------------------------|
| **Umami** (auto-hébergé) | Docker + PostgreSQL (DB existante ou SQLite) | 0 € | Sessions, pages vues, durées, appareils, pays, referrers, événements custom |

**Pourquoi Umami :**
- RGPD-compliant sans cookie banner (pas de tracking personnel)
- ~40 MB de RAM, tient sur le même VPS sans impact
- Événements custom : sign_up, form_created, submission_received, upgrade
- Alternative à Plausible (payant) et Fathom (payant)

**Déploiement :**
```yaml
# docker-compose.override.yml (dans le même stack que le produit)
umami:
  image: ghcr.io/umami-software/umami:postgresql-latest
  ports:
    - "3000:3000"
  environment:
    DATABASE_URL: postgresql://umami:***@db:5432/umami
    TRACKER_SCRIPT_NAME: js/form-track.js
  depends_on:
    - db
```

---

## KPIs à Suivre

### KPIs Business (Stripe + DB)

| KPI | Définition | Source | Cible (an 1) | Fréquence |
|-----|-----------|--------|-------------|-----------|
| **MRR** | Monthly Recurring Revenue | Stripe | 500-1 000 € | Hebdomadaire |
| **ARR** | MRR × 12 | Calculé | 6 000-12 000 € | Mensuelle |
| **Churn Rate** | % clients partis / total début de mois | Stripe | < 5%/mois | Mensuelle |
| **CAC** | Coût d'acquisition client (temps valorisé) | Manuel | < 30 € | Mensuelle |
| **LTV** | Chiffre d'affaires moyen sur durée de vie | Stripe + churn | > 200 € | Trimestrielle |
| **LTV:CAC** | Ratio viabilité | Calculé | ≥ 3:1 | Trimestrielle |
| **Conversion Rate** | Free → Payant | Stripe + DB | ≥ 8% | Mensuelle |
| **Blended ARPU** | MRR / nb clients payants | Calculé | 14-18 € | Mensuelle |
| **Pricing Page → Sign-up** | % visiteurs pricing → création compte | GoAccess + DB | > 3% | Hebdomadaire |

### KPIs Produit (DB)

| KPI | Définition | Requête SQL | Cible |
|-----|-----------|------------|-------|
| **Activation Rate** | % d'inscrits qui créent ≥ 1 formulaire en 24h | `COUNT(DISTINCT user_id) WHERE form_count > 0 AND created_at < signup_at + interval '24h'` | ≥ 65% |
| **Formulaires par utilisateur** | Nb moyen de formulaires | `AVG(form_count) WHERE active = true` | ≥ 2 |
| **Soumissions par formulaire** | Volume moyen | `AVG(submission_count) WHERE is_active = true` | — |
| **Soumissions reçues (total)** | Volume total traité | `SUM(submission_count)` | — |
| **Taux de blocage limite** | % d'utilisateurs atteignant leur limite | `COUNT(*) WHERE submissions >= limit` | — (indicateur de friction) |
| **Temps avant premier dépassement** | Délai entre signup et blocage par limite | `AVG(blocked_at - signup_at)` | 7-30 jours (idéal) |
| **Conversion post-blocage** | % d'utilisateurs qui upgradent après avoir atteint la limite | `COUNT(upgraded) / COUNT(blocked)` | ≥ 15% |
| **Soumissions bloquées** | Nb de soumissions rejetées pour dépassement de limite | `COUNT(*) WHERE blocked = true` | — |

### KPIs Acquisition (GoAccess / Umami)

| KPI | Source | Cible |
|-----|--------|-------|
| **Trafic mensuel** (visiteurs uniques) | GoAccess | > 1 500/mois en phase 2 |
| **Taux de rebond** | GoAccess | < 60% |
| **Pages vues par session** | GoAccess | > 2.5 |
| **Top referrers** | GoAccess | GitHub, HN, PH, Reddit, organique |
| **Taux de sign-up** (visiteur → compte) | GoAccess + DB | > 5% |
| **Taux d'installation Docker** | GitHub releases / Docker pulls | > 100 pulls/mois |
| **Stars GitHub / mois** | GitHub API | > 50/mois |

---

## Événements à Tracker

### Événements Backend (logs applicatifs)

Ces événements sont loggés côté backend (format JSON dans `/var/log/formapi/events.log`).

| Événement | Déclencheur | Données associées |
|-----------|------------|-------------------|
| `user.signed_up` | Inscription complétée | email, referrer, signup_method |
| `user.first_form_created` | Premier formulaire créé | form_name, elapsed_since_signup |
| `user.form_created` | Nouveau formulaire | form_name, form_id |
| `user.form_deleted` | Formulaire supprimé | form_id, submission_count (perdu) |
| `user.first_submission_received` | Première soumission reçue | form_id, elapsed_since_creation |
| `user.submission_received` | Nouvelle soumission | form_id, field_count, size_bytes |
| `user.submission_blocked` | Soumission rejetée (limite atteinte) | form_id, current_count, limit |
| `user.webhook_configured` | Webhook activé sur formulaire | form_id, target_url, event_type |
| `user.plan.upgraded` | Free → Starter ou Starter → Pro | old_plan, new_plan, trigger_reason |
| `user.plan.downgraded` | Pro → Starter ou résiliation | old_plan, reason (enquête sortie) |
| `user.plan.cancelled` | Annulation complète | reason, days_active, form_count, submission_count |
| `user.plan.reactivated` | Réabonnement suite à résiliation | days_gone, reactivation_trigger |
| `form.spam_detected` | Soumission marquée comme spam | form_id, spam_score, rule_triggered |
| `form.export_requested` | Export CSV déclenché | form_id, submission_count_exported |

### Stockage des Événements

**Phase 1 (MVP) :** Table `events` dans PostgreSQL (même DB que le produit)

```sql
CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    event_name VARCHAR(128) NOT NULL,
    event_data JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_events_name ON events(event_name);
CREATE INDEX idx_events_user ON events(user_id);
CREATE INDEX idx_events_created ON events(created_at);
```

**Phase 2 :** Si volumétrie > 100K événements/mois, migrer vers une table séparée ou TimescaleDB (extension PostgreSQL).

### Tracking Côté Frontend (Phase 2 avec Umami)

Quand Umami sera installé (phase 2), ajouter ces événements custom côté frontend :

```javascript
umami.track('sign_up', { referrer: document.referrer });
umami.track('form_created', { name: formName });
umami.track('pricing_page_viewed', { plan_focused: 'Pro' });
umami.track('upgrade_clicked', { current_plan: 'free' });
umami.track('checkout_started', { plan: 'pro', price: 19 });
umami.track('checkout_completed', { plan: 'pro', price: 19 });
umami.track('embed_code_copied', { form_name: formName });
```

---

## Dashboard de Pilotage

### Minimum Viable Dashboard (requête hebdomadaire)

```sql
-- MRR actuel
SELECT SUM(price_cents / 100.0) AS mrr
FROM subscriptions s
JOIN plans p ON s.plan_id = p.id
WHERE s.status = 'active';

-- Nouveaux utilisateurs de la semaine
SELECT COUNT(*) AS new_users
FROM users
WHERE created_at > NOW() - INTERVAL '7 days';

-- Taux d'activation (ont créé au moins 1 formulaire)
SELECT 
    COUNT(*) FILTER (WHERE form_count > 0) AS activated,
    COUNT(*) AS total,
    ROUND(100.0 * COUNT(*) FILTER (WHERE form_count > 0) / COUNT(*), 1) AS activation_rate
FROM users
WHERE created_at > NOW() - INTERVAL '30 days';

-- Nouveaux formulaires créés
SELECT COUNT(*) AS new_forms
FROM forms
WHERE created_at > NOW() - INTERVAL '7 days';

-- Soumissions reçues cette semaine
SELECT COUNT(*) AS weekly_submissions
FROM submissions
WHERE created_at > NOW() - INTERVAL '7 days';

-- Taux de conversion post-blocage (utilisateurs qui ont atteint leur limite puis upgradé)
SELECT
    COUNT(DISTINCT u.id) AS users_blocked,
    COUNT(DISTINCT CASE WHEN s.status = 'active' AND p.price_cents > 0 THEN u.id END) AS converted_after_block,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN s.status = 'active' AND p.price_cents > 0 THEN u.id END) / NULLIF(COUNT(DISTINCT u.id), 0), 1) AS conversion_rate
FROM users u
JOIN forms f ON f.user_id = u.id
JOIN submissions sub ON sub.form_id = f.id
LEFT JOIN subscriptions s ON s.user_id = u.id
LEFT JOIN plans p ON s.plan_id = p.id
WHERE sub.created_at > NOW() - INTERVAL '30 days'
AND f.submission_count >= (CASE 
    WHEN s.plan_id IS NULL THEN 50 
    ELSE (SELECT json_array_length(p.features::json) FROM plans p2 WHERE p2.id = s.plan_id) 
END);
```

### Dashboard idéal (phase 2, outil de BI)

| Composant | Outil | Coût |
|-----------|-------|------|
| Business KPIs (MRR, churn) | Stripe Dashboard | 0 € |
| Trafic web | Umami | 0 € |
| Produit (utilisateurs, formulaires, soumissions) | Metabase (auto-hébergé sur VPS) | 0 € |
| Dashboard global | Metabase + Stripe + PostgreSQL + Umami data | 0 € |

Mettre en place Metabase seulement si besoin d'un dashboard consolidé. Le Stripe Dashboard + Umami + une requête SQL hebdomadaire suffisent au début.

---

## Checklist Mise en Oeuvre

- [ ] Configurer GoAccess sur les logs nginx de l'API Form (phase 1)
- [ ] Créer la table `events` dans PostgreSQL
- [ ] Instrumenter le backend : loguer les événements clés (user.signed_up, user.form_created, user.submission_received, user.submission_blocked, user.plan.upgraded)
- [ ] Connecter Stripe (intégration déjà prévue dans l'architecture billing)
- [ ] Configurer une tâche cron hebdomadaire qui envoie les KPIs par email (via `psql` + `mail`)
- [ ] Créer le script de dashboard CLI (optionnel — afficher les KPIs dans le terminal)
- [ ] Planifier Umami quand le trafic dépasse 500 visiteurs/mois (phase 2)
- [ ] Mettre en place l'enquête de sortie Stripe (raison d'annulation)
- [ ] Ajouter une métrique "conversion post-blocage" pour valider le déclencheur Freemium
