# Plan d'Acquisition — Form Backend API

> Mise à jour : 2026-05-09 — Adapté de Monitoring Serveur Léger vers Form Backend API
> Contrainte budgétaire : < 20 €/mois en coûts récurrents
> Pas de paid ads avant validation produit-marché
> Canaux gratuits ou quasi-gratuits prioritaires

---

## Stratégie d'Acquisition en Deux Phases

### Phase 1 : Launch Spike (J1 — J30)
**Objectif : 200 inscriptions Free, premières conversions Starter**

Le lancement repose sur 3 canaux synergiques qui s'activent le même jour :

#### Canal Primaire : Product Hunt + Hacker News (coût : 0 €)

| Action | Détail | Timing |
|--------|--------|--------|
| **Product Hunt Launch** | Catégorie Developer Tools. Maker = Nassim. Préparer : démo GIF d'intégration HTML + description + first comment technique | Jour 1, 00:01 PT |
| **Hacker News (Show HN)** | "Show HN: I built a self-hosted form backend API that runs on a €4 VPS" | Jour 1, 15:00 CET (pic HN) |
| **Thread Twitter/X** | Fil technique : "J'ai codé une API de formulaires en 3 semaines. Stack, erreurs et leçons." | Jour 1, 09:00 CET |
| **Cross-post Reddit** | r/webdev + r/selfhosted + r/nextjs | Jour 1, après le spike HN |

**Préparation pré-lancement (J-14 à J-1) :**
- [ ] Page d'attente / landing "Coming Soon" avec collecte d'emails (optionnel)
- [ ] Rédiger le post Product Hunt (description, 5 screenshots/GIF, first comment)
- [ ] Rédiger le post Show HN (accroche technique, lien vers démo live)
- [ ] Préparer le thread Twitter/X avec code snippets (HTML form → endpoint)
- [ ] Vérifier que le produit tourne sur le VPS Nassim pour la démo
- [ ] Avoir 3-5 beta testeurs prêts à commenter sur PH/HN
- [ ] Publier le README GitHub avec déploiement one-liner Docker

**Gestion du lancement :**
- Jour J : Nassim disponible 6h pour répondre aux commentaires PH + HN
- Répondre à TOUT le monde sur PH (le premier commentaire fait le classement)
- Surveiller r/webdev et r/selfhosted pour cross-poster naturellement

#### Canal Secondaire : Communautés Web Dev + No-Code (coût : 0 €)

| Communauté | Type de post | Fréquence | Impact estimé |
|-----------|-------------|-----------|---------------|
| r/webdev | "I switched from Formspree to this self-hosted API — here's why" | 1x au lancement, puis 1x/mois | 200-500 vues par post |
| r/selfhosted | "Self-hosted form backend: Docker one-liner, no external service" | 1x au lancement | 200-400 vues |
| r/nextjs | "Add a contact form to your Next.js site without Formspree" | 1x au lancement | 100-300 vues |
| r/webflow | "Form backend for Webflow without paying $15/mo extra" | 1x | 100-200 vues |
| r/france | "J'ai monté une API de formulaires auto-hébergée pour remplacer Formspree" | 1x au lancement | 100-200 vues |
| HackerNews France | Post technique similaire au Show HN | 1x | 100-200 vues |
| Discord dev français (BetaGouv, FrenchDevs) | Partage informel | 1x | 50-100 vues |
| Communauté no-code (Webflow, Carrd) | Tutoriel intégration | 1x/mois après lancement | 200-500 vues |

---

### Phase 2 : Croissance Organique (J31 — J180)
**Objectif : 10-15 nouveaux utilisateurs Free/semaine, 5-10 conversions Starter/mois**

#### Canal Primaire : SEO & Contenu Technique (coût : 0 €)

| Contenu | Mot-clé cible | Volume estimé | Délai indexation | Trafic mensuel estimé |
|---------|--------------|---------------|------------------|----------------------|
| "Self-hosted form backend API: deploy in 5 minutes" | [self hosted form backend] | 200-500/mois | 1 mois | 200-500 |
| "Formspree alternative self-hosted 2026" | [formspree alternative] | 1 000-3 000/mois | 2-3 mois | 400-800 |
| "How to add a contact form to Next.js without a service" | [contact form nextjs without service] | 500-1 000/mois | 1-2 mois | 300-600 |
| "Form API for static sites (Hugo, Jekyll, Astro)" | [form api static site] | 200-500/mois | 2 mois | 150-300 |
| "Top 5 form backend APIs compared in 2026" | [best form backend api] | 500-1 500/mois | 2-3 mois | 300-500 |
| "RGPD-compliant form handling for European websites" | [rgpd form handling] | 100-300/mois | 3 mois | 50-150 |

**Calendrier éditorial (1 article/semaine) :**

| Semaine | Article | Type |
|---------|---------|------|
| S1 post-launch | "Comment j'ai migré de Formspree vers ma propre API de formulaires" | Témoignage technique |
| S2 | "Form Backend API vs Formspree vs FormKeep : le vrai comparatif 2026" | Comparatif |
| S3 | "Déployer une API de formulaires avec Docker Compose en 5 minutes" | Tutoriel |
| S4 | "Pourquoi les devs passent au form backend auto-hébergé (et pas que pour le prix)" | Analyse |
| S5 | "Gérer les formulaires de 20 sites clients avec une seule API" | Cas d'usage agence |
| S6 | "Formspree vs alternatives open-source : ce qui a changé en 2026" | Comparatif |
| S7 | "Comment traiter 15 000 soumissions/mois sans se ruiner" | Guide scaling |
| S8 | "API de formulaires et RGPD : le guide complet pour sites français" | Guide conformité |

**Stratégie SEO :**
- Blog hébergé sur `/blog` du même domaine (pas de sous-domaine — consolidation SEO)
- Articles en français + anglais (marché francophone et international)
- Schema.org Article + FAQ pour les extraits enrichis
- Backlinks : commenter sur HN/Reddit avec liens vers le blog
- **Cibler les mots-clés "Formspree alternative"** — trafic existant élevé, concurrence faible sur le segment "self-hosted"

#### Canal Secondaire : GitHub / Open Source Community (coût : 0 €)

| Action | Fréquence | Objectif |
|--------|-----------|----------|
| README bien écrit avec badge "Deploy to Railway/Coolify" | Unique | Conversion des devs qui trouvent le repo |
| GitHub Discussions ouvertes pour feedback | Permanent | Engagement communauté |
| Répondre aux issues GitHub | Hebdomadaire | Support et visibilité |
| Publier des "Show and tell" sur r/selfhosted | Mensuel | Trafic organique |
| Release notes publiques (GitHub Releases) | À chaque release | Transparence = trust |

**Influenceurs/comptes à engager :**
- @levelsio (Pieter Levels) — build in public référence
- @shadcn — dev tools, design systems
- @mfts0 (Marc) — build in public SaaS, form-related projects
- Communauté #buildspace / #wip.chat

#### Canal Tertiaire : Marketplaces d'Hébergement (coût : 0 €, ROI élevé)

| Marketplace | Action | Impact |
|-------------|--------|--------|
| **Coolify** | Proposer comme "one-click service" | Accès à la base installée Coolify (~20K devs) |
| **Railway** | Template "Form Backend API" | Découverte via le template marketplace |
| **Netlify** | Guides d'intégration "Deploy your own form backend" | SEO + trafic qualifié |
| **Vercel** | Documentation "Add form handling to your Next.js deployment" | SEO + intégration naturelle |
| **CapRover** | One-click app | Communauté self-hosting |

---

## Budget par Canal

| Canal | Coût cash/mois | Coût temps/mois | Justification |
|-------|---------------|-----------------|---------------|
| Product Hunt + HN | 0 € | 8h (prépa) + 6h (J) | Lancement unique |
| SEO / Blog | 0 € | 4h/semaine (16h/mois) | Canal primaire en phase 2 |
| GitHub / OSS | 0 € | 2h/semaine (8h/mois) | Acquisition technique qualifiée |
| Reddit / Communautés | 0 € | 1h/semaine (4h/mois) | Trafic qualifié |
| Marketplaces hébergement | 0 € | 2h (one-time setup) | ROI élevé, one-shot |
| **Total Phase 1** | **0 €** | **~34h (mois 1)** | |
| **Total Phase 2** | **0 €** | **~28h/mois** | |

> Le budget cash est à 0 €. Le seul investissement est le temps de Nassim.
> Avec son rythme (10-15h/semaine de code), il faudra 6-7h/semaine d'acquisition en parallèle.

---

## Funnel : Traffic → Sign-up → Paid → Retained

### Benchmarks par étape

| Étape | Taux | Benchmark SaaS similaire |
|-------|------|-------------------------|
| **Landing → Sign-up** (free) | 5-15% | Indie SaaS médian : 7% |
| **Sign-up Free → Activation** (créer 1er formulaire) | 60-80% | Formspree : ~65% |
| **Activé → Paid** (conversion) | 5-15% | Freemium SaaS médian : 8% |
| **Paid → Retained** (mois 2) | 95% (5% churn) | SaaS SMB médian : 5-7%/mois |

### Volume estimé par canal (Phase 1 — Launch)

| Canal | Visiteurs | Sign-up (7%) | Activés (70%) | Payants (8%) | MRR généré (blended) |
|-------|-----------|-------------|---------------|--------------|----------------------|
| Product Hunt | 1 500 | 105 | 73 | 6 | 48 € |
| Hacker News | 800 | 56 | 39 | 3 | 24 € |
| Twitter/X | 500 | 35 | 24 | 2 | 16 € |
| Reddit + communautés | 300 | 21 | 15 | 1 | 8 € |
| **Total Launch** | **3 100** | **217** | **151** | **12** | **~96 € MRR** |

### Volume estimé par canal (Phase 2 — Mensuel)

| Canal | Visiteurs/mois | Sign-up (5%) | Activés (65%) | Payants (7%) | MRR brut |
|-------|---------------|-------------|---------------|--------------|----------|
| SEO Blog | 800 | 40 | 26 | 2 | 16 € |
| GitHub (organique) | 400 | 20 | 13 | 1 | 8 € |
| Reddit cross-posts | 200 | 10 | 7 | 1 | 8 € |
| Marketplaces hébergement | 150 | 8 | 5 | 1 | 8 € |
| Bouche-à-oreille | 100 | 20 | 15 | 1 | 8 € |
| **Total mensuel** | **1 650** | **98** | **66** | **6** | **~48 € MRR/mois** |

> Hypothèse réaliste pour un SaaS solo avec acquisition 100% organique.
> L'effet Compound : 48 €/mois de nouveau MRR × 12 mois = ~576 € MRR additionnel brut en fin d'année.

---

## Time to First Paying Customer

| Étape | Délai estimé |
|-------|-------------|
| Mise en ligne du produit (v1) | J0 |
| Pic de trafic PH + HN | J1 |
| Premières inscriptions Free | J1 (dans l'heure) |
| Premier formulaire créé (activation) | J1-J2 |
| Première soumission reçue | J2 |
| Premier dépassement limite Free (50 soumissions) | J7-J30 (selon trafic) |
| **Première conversion Starter** | **J7-J30** |
| Première conversion Pro | J15-J60 |

Le premier client payant devrait arriver dans les **1 à 4 premières semaines** suivant le lancement. Le déclencheur principal sera le dépassement des 50 soumissions gratuites (besoin réel — formulaire de contact qui commence à recevoir du trafic).

---

## Risques & Mitigation

| Risque | Impact | Mitigation |
|--------|--------|-----------|
| Product Hunt flop (top < 20) | Trafic faible | Préparer un post HN de backup solide. Le PH n'est pas essentiel — le vrai canal long-terme est le SEO |
| HN ignore le post | Pas de spike | Cross-poster sur Reddit le même jour. Le SEO prendra 1-2 mois |
| Pas de conversions payantes | MRR = 0 | Relancer les inactifs par email. Ajouter une limite plus agressive (30 soumissions/mois au lieu de 50) |
| Trop de trafic, serveur qui tombe | Mauvaise première impression | Rate limiting déjà en place (60/min). Redis + VPS tient les spikes |
| Churn élevé (>7%/mois) | MRR stagne | Enquête de sortie (Stripe, pourquoi annulez-vous ?). Ajouter features les plus demandées |
| Web3Forms gratuit cannibalise le marché | Pression sur le pricing | Miser sur la qualité : support, uptime, RGPD, auto-hébergement. Ne pas concourir sur le prix pur |
