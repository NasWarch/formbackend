# Grille de Pricing — Form Backend API

> Produit : API backend de traitement de formulaires (réception, validation, stockage, notification, réponse personnalisée)
> Persona : Développeur web, créateur de landing page, agence web, SaaS (1-20 pers.)
> Budget cible : 0-39 €/mois (freemium + 3 plans payants)

---

## Plans Tarifaires

| Plan | Prix | Soumissions/mois | Formulaires | Notifications | Fonctionnalités clés |
|------|------|-----------------|-------------|---------------|----------------------|
| **Gratuit** | **0 €** | 50 | 1 | Email (pas de notification) | Dashboard, historique 30 jours, API REST de base |
| **Starter** | **8 €/mois** | 500 | 5 | Email uniquement | Dashboard, historique 90 jours, anti-spam basique, API REST, webhook vers votre site |
| **Pro** | **19 €/mois** | 2 000 | 20 | Email / Slack / Discord / Webhook | Anti-spam avancé (reCAPTCHA, honeypot), réponses personnalisées, redirections, logs 365 jours |
| **Business** | **39 €/mois** | 10 000 | Illimité | Tout Pro + SMS (1er palier) | Marque blanche, domaine personnalisé, export CSV/JSON, équipe (jusqu'à 5 membres), API complète, webhooks sortants, intégrations Zapier/Make |

### Justification des plans

**Gratuit** — Hook d'entrée zéro friction. 50 soumissions/mois suffisent pour tester l'API, un prototype ou un petit formulaire de contact perso. Convertit par friction quand le user atteint la limite ou a besoin de plusieurs formulaires.

**Starter** — Premier plan payant, 10× plus de soumissions que le Gratuit pour 8 €. Vise le développeur solo ou le blogueur technique avec un trafic modeste. Prix psychologiquement sous les 10 € pour maximiser la conversion.

**Pro** — Plan principal, coeur du MRR. 2 000 soumissions couvrent une PME, une agence avec plusieurs landing pages, ou un petit SaaS. Notifications multicanal (Slack/Discord) = valeur forte pour les leads entrants.

**Business** — Pour les agences et SaaS qui traitent des volumes importants. Marque blanche = différentiateur : le client utilise son propre domaine, le service est invisible. Intégrations Zapier/Make = vendu en upsell pour les workflows complexes.

---

## Benchmark Concurrentiel

| Concurrent | Gratuit | Plan entrée | Milieu de gamme | Haut de gamme | Notre position |
|-----------|---------|-------------|-----------------|---------------|----------------|
| **Formspree** | $0 (50 sub.) | $8/mois (50 sub.) | $18/mois (500) | $55/mois (2 500) | Starter 8€/500 = 10× plus de sub. que Formspree entrée |
| **FormKeep** | ✗ (pas de gratuit) | $5/mois (50 sub.) | $19/mois (1 000) | $49/mois (4 000) | Pro 19€/2000 = 2× plus que FormKeep au même prix |
| **Web3Forms** | $0 (100 sub.) | $9/mois (1 000) | — | $29/mois (5 000) | Pro 19€/2000 vs 29$/5000 — moins cher, moins de volume |
| **Getform** | $0 (50 sub.) | — | $15/mois (2 000) | $25/mois (5 000) | Pro au même prix mais moins de fonctionnalités |
| **Formcarry** | $0 (100 sub.) | $12/mois (1 000) | — | $24/mois (3 000) | Business 39€/10000 = 3× plus de volume pour +60% |
| **Basin** | $0 (100 sub.) | — | $19/mois (3 000) | $39/mois (10 000) | Business au même prix mais avec plus de features |
| **Paperform** | ✗ | $24/mois (100 sub.) | $36/mois (1 000) | $48/mois (10 000) | Beaucoup plus cher, cible créateurs de contenu |

### Différentiation clé

| Dimension | Nous | Concurrents |
|-----------|------|-------------|
| Gratuit fonctionnel | ✅ 50 sub./mois, 1 formulaire | Web3Forms/Formcarry : 100 sub. Formspree : 50 sub. OK, mais pas de gratuit chez FormKeep/Basin |
| Starter 500 sub. à 8 € | ✅ | Formspree : 50 sub. à $8. **Nous = 10× plus au même prix** |
| Pro 2000 sub. à 19 € | ✅ 2 000 sub., notifications multicanal | FormKeep : 1 000 sub. à $19. **Nous = 2× plus** |
| Business 10000 sub. à 39 € | ✅ Volume pro accessible | Formspree : 2 500 sub. à $55. FormKeep : 4 000 sub. à $49 |
| Anti-spam avancé en Pro | ✅ reCAPTCHA + honeypot | Formcarry et Web3Forms n'ont que le captcha basique |
| Domaines personnalisés Business | ✅ Inclus dans 39 € | Formspree facture $12/mois *supplémentaires* pour domaine perso |
| Prix en euros | ✅ 8 / 19 / 39 € | Tous en USD — avantage psychologique France/UE |
| Marque blanche | ✅ Business (39 €) | Formspree : $55/mois. FormKeep : $49/mois |
| Support multi-canal dès le Pro | ✅ Email + Slack + Discord + Webhook | Beaucoup ne font qu'email |
| Notification SMS | ✅ Business (palier) | Aucun concurrent ne propose SMS |

---

## Unit Economics — Estimations

### Hypothèses de base

| Métrique | Valeur | Source |
|----------|--------|--------|
| Prix moyen pondéré (blended ARPU) | 18,60 €/mois | 40% Gratuit (0€) + 40% Starter × 8€ + 15% Pro × 19€ + 5% Business × 39€ — le Gratuit dilue le ratio d'utilisateurs mais pas le MRR |
| ARPU clients payants | 14,20 €/mois | 66% Starter × 8€ + 25% Pro × 19€ + 9% Business × 39€ |
| Marge brute | ~94 % | Coûts serveur fixes (VPS déjà payé). Coût variable : stockage + emails transactionnels + reCAPTCHA (~0,70 € par utilisateur Pro/Business) |
| Churn mensuel cible | 5 % | Benchmark SaaS SMB (Baremetrics : 4-7%/mois pour SaaS < $50/mois) |
| Durée de vie moyenne client | 20 mois | 1 / 0.05 |
| Nombre de paiements sur la vie | 20 | 20 mois × 1 paiement/mois |

### CAC estimé

**Phase 1 — Launch (Mois 1-3)** : Acquisition 100% organique

| Canal | Temps/mois | Coût (temps valorisé à 50€/h) | Période |
|-------|-----------|-------------------------------|---------|
| Contenu SEO (blog) | 4 h | 200 € | Permanent |
| Social media (Twitter/X, LinkedIn dev) | 2 h | 100 € | Permanent |
| Communautés (Reddit, HN, Discord devs) | 2 h | 100 € | Permanent |
| **Total** | **8 h/mois** | **400 €/mois** | |

Nouveaux utilisateurs payants estimés : 15/mois (boosté par le plan Gratuit qui attire du trafic organique et convertit une partie en payant)
**CAC = 400 € / 15 = ~27 € par client payant**

### LTV estimée

| Métrique | Calcul | Valeur |
|----------|--------|--------|
| LTV brute | ARPU × Lifetime | 14,20 € × 20 mois = **284 €** |
| LTV nette (coûts variables déduits) | ~13,50 € × 20 mois = **270 €** | |
| **Ratio LTV:CAC** | 284 / 27 | **10,5:1 ✅ (≥ 3:1)** |

### Payback Period

| Métrique | Valeur |
|----------|--------|
| CAC | 27 € |
| Marge mensuelle par client | ~12,50 € |
| **Payback** | **~2,2 mois** |

Benchmark SaaS sain : payback < 12 mois. ✅

### Gross Margin par plan

| Plan | Prix | Stripe fee | Coûts variables (stockage, email, captcha) | Taxe (VAT FR 20%) | Marge nette/mois |
|------|------|-----------|-------------------------------------------|-------------------|------------------|
| Gratuit | 0,00 € | 0 € | ~0,05 € (stockage minimal) | 0 € | -0,05 € (perte technique, compensée par acquisition) |
| Starter | 8,00 € | ~0,35 € | ~0,10 € | ~1,33 € | 6,22 € (78%) |
| Pro | 19,00 € | ~0,55 € | ~0,40 € | ~3,17 € | 14,88 € (78%) |
| Business | 39,00 € | ~0,83 € | ~1,40 € | ~6,50 € | 30,27 € (78%) |

Note : les taxes sont collectées et reversées — elles n'impactent pas la marge brute au sens strict. Les marges réelles hors taxes sont >78%. Le plan Gratuit est une perte technique négligeable (~0,05€/utilisateur/mois) compensée par l'acquisition de leads qualifiés.

### Scénarios de croissance

| Scénario | MRR Mois 6 | MRR Mois 12 | LTV:CAC |
|----------|-----------|-------------|---------|
| **Pessimiste** (3% churn, 8 nouveaux payants/mois) | 450 € | 1 100 € | 5,8:1 |
| **Réaliste** (5% churn, 15 nouveaux payants/mois) | 750 € | 1 600 € | 10,5:1 |
| **Optimiste** (3% churn, 22 nouveaux payants/mois) | 1 400 € | 3 100 € | 15,2:1 |

---

## Élasticité du Pricing — Notes

### Tests de pricing post-lancement

1. **Gratuit → Starter** : Tester si 50 sub./mois est le bon seuil de friction. Trop généreux (100 sub.) et la conversion freemium→payant chute. Trop restrictif (25 sub.) et l'adoption initiale plafonne.
2. **Test A/B Starter** : Essayer 8 € vs 10 € après 100 conversions. Si conversion rate ne baisse pas significativement, monter à 10 € avec 1 000 soumissions.
3. **Test Pro / Business** : La fourchette 19-39 € est validée par le benchmark mais un palier intermédiaire à 29 € (5 000 sub.) peut être testé après 200 clients payants.
4. **Annual discount** : Pro à 190 €/an (économie de 17%), Business à 390 €/an (économie de 17%) — les annualisations réduisent le churn.
5. **Seuil psychologique** : 8 € < 10 €. Le palier Starter est délibérément accessible pour maximiser l'adoption initiale.

### Sensibilité

| Variation de prix | Impact estimé sur conversions | Impact sur MRR |
|------------------|------------------------------|----------------|
| -20% (6,40 € Starter) | +15% conversions | -8% MRR |
| +25% (10 € Starter) | -20% conversions | 0% MRR (neutre) |
| +50% (12 € Starter avec 1 000 sub.) | -30% conversions | +5% MRR |

Le sweet spot semble être entre 8 € et 10 € pour le Starter. Recommandation : lancer à 8 € pour maximiser l'adoption initiale face à Web3Forms et FormKeep, remonter après validation à 10 € avec 1 000 sub.

---

## Résumé

| Métrique | Cible | Notre estimation |
|----------|-------|-----------------|
| ARPU (payants) | — | 14,20 € |
| CAC | — | 27 € |
| LTV | — | 284 € |
| LTV:CAC | ≥ 3:1 | **10,5:1** ✅ |
| Payback period | < 12 mois | **2,2 mois** ✅ |
| Churn mensuel | < 5% | 5% (cible) |
| Gross margin | > 80% | >78% ✅ |
