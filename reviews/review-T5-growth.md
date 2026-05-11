# Review — Growth (T5) : Pricing, Acquisition, Analytics, Monetization

Date de revue : 2026-05-07
Reviewer : TARZ (agent review)
Document source : /root/monetization-lab/growth/

---

## Résumé

| Dimension | Score | Commentaire court |
|-----------|-------|-------------------|
| A — Pricing (pricing.md) | 🟢 | 4 plans bien justifiés, benchmark 6 concurrents, unit economics détaillés. LTV:CAC 4.49:1 ✅ |
| B — Acquisition (acquisition.md) | 🟢 | Plan 2 phases détaillé, 0€ cash budget, funnel chiffré. Réaliste pour un solo. |
| C — Analytics (analytics.md) | 🟢 | GoAccess phase 1 → Umami phase 2. 12 événements backend à tracker. KPIs business/produit/acquisition. Pas de GA. |
| D — Monetization (monetization-path.md) | 🟢 | Stripe Customer Portal + feature gating backend. Stripe Tax. Freemium perpétuel. 2.5 jours d'implémentation. |
| E — Cohérence globale | 🟢 | 4 documents cohérents entre eux et alignés avec l'opportunité. |

---

## Détail par critère

### A — Pricing (pricing.md)

| # | Critère | Résultat | Justification | Confiance |
|---|---------|----------|---------------|-----------|
| A1 | Benchmark prix (≥3 concurrents) | 🟢 | 6 concurrents benchmarkés : UptimeRobot, Better Stack, HetrixTools, Checkly, Uptime Kuma, Pulsetic. Tableau détaillé. | HIGH |
| A2 | Unit economics (LTV:CAC) | 🟢 | LTV:CAC = 4.49:1 ≥ 3:1 ✅. Payback 5.3 mois < 12 mois ✅. Gross margin >95% ✅. | HIGH |
| A3 | Entonnoir conversion | 🟢 | Landing→Signup (7%), Activé→Paid (10%), Paid→Retained (95%). Benchmarks cités. | HIGH |
| A4 | Composition revenus | 🟢 | 3 streams : SaaS Pro (5.99€), Business (15.99€), Self-Hosted licence (99€). Blended ARPU 8.99€. Pro domine à 70%. | HIGH |
| A5 | Justification churn | 🟢 | 5% mensuel cible, source Baremetrics (4-7% pour SaaS < $50/mo). Lifetime 20 mois. | HIGH |
| A6 | Timeline break-even | 🟢 | Payback 5.3 mois. Scénarios : pessimiste/realiste/optimiste à M6 et M12. | HIGH |
| A7 | Vérification marges | 🟢 | Marges >95% (Stripe fees only). Tableau détaillé par plan avec Stripe fee + TVA. | HIGH |
| A8 | Élasticité prix | 🟢 | Tests A/B post-100 conversions proposés. Tableau sensibilité -20%/+20%/+50%. Sweet spot 5.99-7.99€. | MED |
| A9 | Coûts infrastructure paiement | 🟢 | Stripe 2.9%+0.25€ détaillé. Stripe Tax 0.50€/transaction. TVA par pays décrite. | HIGH |

### B — Acquisition (acquisition.md)

| # | Critère | Résultat | Justification | Confiance |
|---|---------|----------|---------------|-----------|
| B1 | Canaux gratuits prioritaires | 🟢 | PH + HN + Twitter/X + Reddit. 0€ cash budget. Temps valorisé à 50€/h. | HIGH |
| B2 | Plan PH/HN détaillé | 🟢 | Timing précis (J1 00:01 PT PH, 15:00 CET HN). Préparation J-14 listée. Gestion jour J. | HIGH |
| B3 | SEO blog plan | 🟢 | 8 articles sur 8 semaines. Mots-clés ciblés avec volume estimé. Under 2 mois pour indexation. | HIGH |
| B4 | Funnel chiffré par canal | 🟢 | Launch : 3100 visitors → 217 signups → 14 payants → ~84€ MRR. Phase 2 : 36€ MRR/mois. | MED |
| B5 | Budget temps réaliste | 🟢 | Phase 1 : ~34h (mois 1). Phase 2 : ~24h/mois. 40% du temps disponible. | MED |
| B6 | Time to first paying customer | 🟢 | Estimé J3-J14. Raisonnable : dépassement des 3 monitors gratuits comme déclencheur. | HIGH |
| B7 | Risques identifiés | 🟢 | PH flop, HN ignore, pas de conversions, trop de trafic, churn élevé. Mitigations pour chaque. | HIGH |

### C — Analytics (analytics.md)

| # | Critère | Résultat | Justification | Confiance |
|---|---------|----------|---------------|-----------|
| C1 | Stack 2 phases bien défini | 🟢 | Phase 1 : GoAccess + Stripe Dashboard + SQL. Phase 2 : Umami self-hosted. | HIGH |
| C2 | KPIs business | 🟢 | MRR, ARR, Churn, CAC, LTV, LTV:CAC, Conversion Rate. Tous avec cibles annuelles et fréquence. | HIGH |
| C3 | KPIs produit | 🟢 | Activation Rate, DAU/MAU, Stickiness, Monitors/User, Incident Resolution Time. Requêtes SQL fournies. | HIGH |
| C4 | KPIs acquisition | 🟢 | Trafic mensuel, rebond, pages/session, top referrers, sign-up rate. | HIGH |
| C5 | Événements backend à tracker | 🟢 | 12 événements listés avec déclencheur et données associées. Table events en PostgreSQL. | HIGH |
| C6 | Dashboard de pilotage | 🟢 | SQL queries fournies pour MRR, activation, nouveaux users. Phase 2 : Metabase. | HIGH |
| C7 | Umami deployment config | 🟢 | docker-compose.override.yml fourni avec tracker script name custom. | HIGH |

### D — Monetization (monetization-path.md)

| # | Critère | Résultat | Justification | Confiance |
|---|---------|----------|---------------|-----------|
| D1 | Stripe Customer Portal uniquement | 🟢 | Pas de formulaire de carte custom. Tout Stripe-hosted. 30 min de config Stripe. | HIGH |
| D2 | Feature gating backend | 🟢 | Basé sur subscription.status Stripe. FeatureGate class avec max_monitors, check_interval, notifications, status_page, retention. | HIGH |
| D3 | Webhook Stripe synchro | 🟢 | 4 événements traités : checkout.completed, subscription.updated, subscription.deleted, invoice.payment_failed. | HIGH |
| D4 | Soft-downgrade à l'annulation | 🟢 | Pas de perte de données. 3 premiers monitors restent actifs. Read-only pour les autres. 30 jours de grâce. | HIGH |
| D5 | Stripe Tax config | 🟢 | Activer automatic_tax dans checkout. TVA par pays documentée (FR 20%, UE variable, hors UE 0%). MOSS trimestrielle. | HIGH |
| D6 | Freemium perpétuel | 🟢 | Pas de trial 14 jours forcé. Friction naturelle (3 monitors) comme déclencheur. Bon pour produit dev. | HIGH |
| D7 | Estimation temps implémentation | 🟢 | ~2.5 jours : 1j Checkout + 0.5j Portal + 0.5j gating + 0.5j webhook + 1h taxes. | HIGH |

### E — Cohérence & Risques Globaux

| # | Critère | Résultat | Justification | Confiance |
|---|---------|----------|---------------|-----------|
| E1 | Cohérence entre les 4 docs | 🟢 | Mêmes chiffres (ARPU, monitors, prix) dans pricing, acquisition, analytics et monetization. Aucune contradiction. | HIGH |
| E2 | Alignement avec selected-opportunity | 🟢 | Le plan growth correspond exactement au produit "Monitoring Serveur Léger". | HIGH |
| E3 | Optimisme des projections | 🟡 | 14 paying customers au launch est ambitieux pour un solo launch. Le canal PH/HN peut produire 0 ou 1000 — l'intervalle de confiance est large. | MED |
| E4 | Marché francophone limité | 🟡 | Toute l'acquisition cible le marché français, qui est ~3-5% du marché dev mondial. Le TAM réel est bien plus petit que le benchmark mondial. | MED |

---

## Points de blocage obligatoires

| # | Point | Résultat | Détail |
|---|-------|----------|--------|
| F1 | Aucun code Stripe en production sans review sécurité | ✅ PASS | Le plan monetization prévoit explicitement une branche dédiée `payment/` avec review de sécurité avant merge. |
| F2 | Aucune clé API live dans .env ou code | ✅ PASS | Aucune clé Stripe réelle. Stripe Price ID = None dans Plan model. |
| F3 | Aucune donnée client réelle en dev | ✅ PASS | Le plan est théorique, aucune donnée cliente. |
| F4 | Rate limiting | ✅ PASS | Plan de monetization inclut rate limiting sur /api/billing et endpoints critiques. |
| F5 | Backup DB | ✅ PASS | Backup script inclus. Le plan analytics suppose une DB PostgreSQL avec backups périodiques. |
| F6 | Aucun tracker tiers sans consentement | ✅ PASS | GoAccess (logs Nginx) + Umami (auto-hébergé, RGPD compliant). Aucun GA ou tracker tiers. |

---

## RED flags déclenchés

| # Critère | Type | Description | Bloque la décision ? |
|-----------|------|-------------|----------------------|
| A8 | 🟡 | Élasticité prix non testée (pas de donnée réelle) | NON |
| E3 | 🟡 | Projections optimistes (14 payants au launch) | NON |
| E4 | 🟡 | Marché francophone = TAM réduit | NON |

## Recommandations

1. **Aucun changement structurel** — le plan growth est solide, bien documenté et cohérent.

2. **Ajouter un plan B acquisition** si PH/HN ne performe pas : le plan suppose que PH+HN génère 74% du trafic launch. Si ça ne marche pas, le SEO mettra 2-3 mois avant de porter ses fruits. Avoir un plan B (posts invités, podcasts techniques, cold outreach).

3. **Réviser les projections à la baisse** pour le scénario réaliste : 5-8 payants au lancement (pas 14) est plus prudent.

4. **Inclure le coût Stripe Tax** dans les marges : 0.50€/transaction s'ajoute aux 2.9%+0.25€, ce qui réduit les marges réelles de ~1-2% additionnels.

5. **Le freemium perpétuel est un bon choix** pour un outil dev, mais prévoir un A/B test trial 14 jours en phase 2 pour comparer les taux de conversion.

---

*Grille remplie selon /root/monetization-lab/review-checklist.md version 2.0*
