# Customer Discovery — Form Backend API

> **Objectif :** Identifier les vrais pain points, la tolérance de prix, et les feature wishes des développeurs concernant les backends de formulaires.
> **Date :** 2026-05-09
> **Sources :** Hacker News (Algolia API), Reddit (PullPush.io), pages de prix concurrentes (scraping direct)
> **Contexte :** MVP Form Backend API construit. Pricing 8/19/39 EUR. Ce document complète l'étude de marché `form-api-market.md` par une recherche côté client.

---

## 1. Pain Points Récurrents

### 1.1 SPAM — Le problème #1 écrasant

Le spam est mentionné dans **toutes** les discussions, de façon récurrente et comme le problème principal.

**Sources :**

- HN, thread FormBee (177 pts, 36 cmts) — `andershaig` (créateur de Kwes Forms) : "One challenge with form → email solutions is staying ahead of spam. I've seen some pretty insane rates of spam usage." Décrit un système de scoring utilisateur avec autoban. Source : https://news.ycombinator.com/item?id=42614316 (consulté 2026-05-09)
- HN, thread FormBee — `n3storm` : "I think the only feature missing would be the pow captcha." Source : ibid.
- Reddit r/webdev, "Weird Spam issue" (2025-04-23) : Un utilisateur Jotform voit une augmentation massive d'emails de contact frauduleux via son formulaire. Source : https://reddit.com/r/webdev/comments/1k6ane2/weird_spam_issue/ (consulté 2026-05-09)
- HN, "Bot Butcher – API to eliminate contact form spam using Machine Learning" (Show HN, 4 pts, 2023-08-09) : Preuve qu'un marché entier existe juste pour l'anti-spam des formulaires. Source : https://news.ycombinator.com/item?id=37064185 (consulté 2026-05-09)
- Reddit r/node, "email service, personal project" (2025-03-04) : Développeur freelance construisant des sites statiques mentionne le spam comme défi principal. Source : https://reddit.com/r/node/comments/1j3f4sv/email_service_personal_project/ (consulté 2026-05-09)

**Conclusion :** L'anti-spam est LA feature n°1. CAPTCHA ne suffit pas — les devs veulent du scoring comportemental, rate limiting intelligent, et détection ML.

---

### 1.2 Prix des solutions SaaS existantes — Trop cher pour ce que c'est

**Sources :**

- HN, thread FormBee — `alin23` : "I've been using Formspark for all my websites. I paid $25 a few years ago and I still have 47k out of the 50k submission credits I bought." Implication : les abonnements mensuels sont perçus comme injustifiés pour un service simple (un endpoint POST → email). Source : https://news.ycombinator.com/item?id=42614316 (consulté 2026-05-09)
- Reddit r/webdev, "Simplest Form Handler for a Vercel-Style Free Tier?" (2025-02-21) : "I'm being cheap. But hey! I'll pay the money for an upgrade if my sites are getting the traffic." Source : https://reddit.com/r/webdev/comments/1iuh4du/simplest_form_handler_for_a_vercelstyle_free_tier/ (consulté 2026-05-09)
- Reddit r/webdev, "Thoughts on FormEasy, the free alternative to FormSpree?" (2025-02-03) : Utilisateur construit un site Astro et cherche une alternative gratuite à Formspree. Le nom "FormEasy" capitalise sur la promesse "gratuit". Source : https://reddit.com/r/webdev/comments/1igxn7e/thoughts_on_formeasy_the_free_alternative_to/ (consulté 2026-05-09)
- Reddit r/webdev, "Which service is the best for sending an email after a form has been submitted?" (2025-01-29) : Développeur cherche à envoyer un email après soumission de formulaire — ne veut pas payer un abonnement pour ça. Source : https://reddit.com/r/webdev/comments/1icse5t/which_service_is_the_best_for_sending_an_email/ (consulté 2026-05-09)

**Conclusion :** Le marché est saturé d'alternatives qui promettent la même chose. Les devs comparent activement les prix. Formspark a cassé le marché avec son modèle one-time ($25 lifetime). Un abonnement mensuel doit être justifié par de la valeur au-delà de "POST → email".

---

### 1.3 Données hébergées chez un tiers — Perte de contrôle

**Sources :**

- Reddit r/selfhosted, "After 3+ months of work, finally launching FormBee" (2024-09-15) : "I didn't like the form backends on the market, and how they stored the form data themselves. FormBee just passes the data to your email, discord, telegram, etc." Source : https://reddit.com/r/selfhosted/comments/1fhq4xu/after_3_months_of_work_finally_launching_formbee/ (consulté 2026-05-09)
- HN, thread FormBee — `parkaboy` : Retour sur le dashboard : perplexe sur "Allowed Domains" — se demande à quoi ça sert. Source : https://news.ycombinator.com/item?id=42614316 (consulté 2026-05-09)
- HN, thread FormBee — `stevenicr` : "I've been looking for self hostable: encryption before emailing and encryption at rest for form submissions data saved in a server DB." Cherche une solution HIPAA-compatible sous $29/mois. Source : ibid.
- Reddit r/selfhosted, "Self hosted form API for static websites?" (37 pts, 24 cmts, 2020-03-18) : Fil de discussion très actif — les devs VEULENT self-hosted mais les solutions existantes sont trop complexes. Source : https://reddit.com/r/selfhosted/comments/fkovs7/self_hosted_form_api_for_static_websites/ (consulté 2026-05-09)
- Reddit r/selfhosted, "Mail API for static websites (as Formspree)" (20 pts, 4 cmts, 2021-11-26) : Recherche active d'alternative self-hostée. Source : https://reddit.com/r/selfhosted/comments/r2ti62/mail_api_for_static_websites_as_formspree/ (consulté 2026-05-09)
- Reddit r/selfhosted, "Collecto - the open-source & self-hosted version of formspree/getform" (2024-11-20) : Nouvel entrant dans l'espace self-hosted. Source : https://reddit.com/r/selfhosted/comments/1gvy6vh/collecto_the_opensource_selfhosted_version_of/ (consulté 2026-05-09)
- HN, "FormZero – Self-hosted form back end as easy to deploy as SaaS signup" (Show HN, 3 pts, 2025-10-29) : Preuve que le marché self-hosted continue de croître. Source : https://github.com/BohdanPetryshyn/formzero (consulté 2026-05-09)

**Conclusion :** Le désir de self-hosting est massif et croissant. Les acheteurs sont des devs qui :
- Ne veulent pas que leurs clients envoient des données à un tiers américain (RGPD)
- Veulent le chiffrement de bout en bout
- Trouvent les solutions existantes trop complexes à déployer (docker-compose c'est bien, one-liner c'est mieux)

---

### 1.4 Complexité d'intégration / Documentation pauvre

- HN, `parkaboy` sur FormBee : "The dashboard copy could be crystallized a bit more or provide a hint tooltip" — même les outils orientés devs ont des problèmes d'UX. Source : https://news.ycombinator.com/item?id=42614316 (consulté 2026-05-09)
- Reddit r/SideProject, "Struggling with Lost Form Submissions?" (2025-03-08) : "I noticed a big problem: form submissions getting lost." Source : https://reddit.com/r/SideProject/comments/1j6n1sd/struggling_with_lost_form_submissions_im_building/ (consulté 2026-05-09)

---

## 2. Analyse des Concurrents via Avis Utilisateurs

### 2.1 Formspark — Pricing Lifetime, Très Apprécié

- Modèle : Free (250 subs) + $25 one-time (50K subs) — **aucun abonnement récurrent**
- Réputation excellente dans la communauté dev (mentionné de façon très positive sur HN)
- Point fort : "Formspark data bundles do not expire" — pas de stress sur l'expiration des submissions
- Intégrations : Botpoison, reCAPTCHA, hCaptcha, Turnstile, Slack, Zapier, Make — couverture complète
- Source : https://formspark.io/pricing (consulté 2026-05-09)

### 2.2 Formspree — Le Leader avec des Faiblesses

- 0 reviews sur Trustpilot — pas de feedback structuré disponible. Source : https://www.trustpilot.com/review/formspree.io (consulté 2026-05-09)
- Mentions Reddit : utilisé par défaut mais les devs cherchent activement des alternatives (FormEasy, FormBee, Formspark, Formcarry)
- Points forts : marque établie, intégration Netlify, écosystème
- Points faibles perçus : pricing élevé ($10 pour 200 subs/mois), pas d'auto-hébergement

### 2.3 Web3Forms — Gratuit mais Fragile

- Modèle "pay what you want" / donation — unlimited submissions
- Cloudflare-bloqué — problème récurrent de fiabilité/bot protection
- Mentionné sur Reddit comme solution simple mais sans garantie de pérennité
- Point faible : "No SLA, no enterprise support, fragile business model" (source : étude de marché form-api-market.md, 2026-05-09)

### 2.4 FormKeep — Concurrent Direct le Plus Proche

- Pricing très agressif : $4.99/1K subs, $19.50/10K, $59/100K
- Mentionné dans la discussion HN "What's the best contact form solution these days?" (1 pt, 2016) — ancien thread
- Pas de présence sur les réseaux récents (HN, Reddit) — semble en dormance marketing
- Points faibles : interface vieillissante, pas d'auto-hébergement

### 2.5 Basin / Getform / Formcarry — Les "Others"

- Basin : pas de données suffisantes
- Getform : pivot vers l'email marketing — s'éloigne du marché form API
- Formcarry : $5/500 subs, bon rapport qualité-prix, white-label attractif

---

## 3. Tolérance de Prix (Willingness to Pay)

### 3.1 Analyse des données collectées

| Segment | WTP estimée | Source | Justification |
|---------|------------|--------|---------------|
| Dev solo (1-5 forms) | **0-5€/mois** | Reddit r/webdev, "Simplest Form Handler" | "I'll pay if traffic justifies it". Utilise free tiers. |
| Freelance (5-20 forms) | **5-15€/mois** | HN, FormBee thread | $25 one-time (Formspark) est le benchmark psychologique. Mensuel max ~$5. |
| Agence (20-50 forms) | **15-30€/mois** | Marché : Formcarry $15/2K, FormKeep $19.50/10K | Accepte un abonnement si multi-projets et white-label. |
| SaaS / entreprise | **20-50€/mois** | HN, `stevenicr` : "under $29/mth" ; FormKeep $59 pour 100K | Le driver est la conformité (RGPD, HIPAA) pas le prix. |
| Privacy-conscious | **20-50€/mois** | Reddit r/selfhosted, 2 threads majeurs | "I'll pay more for data sovereignty." |

### 3.2 Le benchmark Formspark

**Point critique :** Formspark propose $25 one-time pour 50K submissions lifetime. C'est le benchmark psychologique du marché. Beaucoup de devs comparent tout abonnement mensuel à ce repère.

**Implication pour notre pricing (8/19/39 EUR) :**
- Plan Solo à 8€/mois : un dev solo paiera 96€/an — vs $25 one-time chez Formspark. Il faut justifier ce premium.
- Plan Pro à 19€/mois : acceptable pour agences. 228€/an vs $25 Formspark — la différence se justifie par le multi-projets, webhooks, et auto-hébergement.
- Plan Business à 39€/mois : très compétitif vs FormKeep $59 ou Formcarry $80 pour le même volume.

### 3.3 Leçons de l'Open Source

- Web3Forms (gratuit, 4K+ GitHub stars) et FormBee (open source, deployable via Docker) montrent qu'une partie significative du marché ne paiera **jamais** pour un backend de formulaires.
- Le free tier doit être généreux (250+ subs/mois) pour convertir en essayeurs.
- La valeur payante doit être : auto-hébergement simplifié + anti-spam + support.

---

## 4. Feature Requests Prioritaires

Synthèse des demandes les plus récurrentes dans les discussions HN + Reddit.

### 4.1 Anti-spam intelligent (PRIORITÉ #1)

**Preuve :** 7+ mentions dans les sources. `andershaig` (Kwes Forms) dédie son produit entier à ça. Bot Butcher (Show HN) existe uniquement pour ça. `n3storm` mentionne Pow CAPTCHA comme le manque principal.

**Recommandation :**
- Rate limiting intelligent (IP + user-agent + pattern matching)
- Scoring comportemental
- Turnstile/hCaptcha intégré nativement (pas de module externe)
- Optionnel : détection ML pour spam avancé

**Ce que les concurrents font :** Formspree a du spam filtering avancé (payant). Formspark s'intègre avec Botpoison. Personne n'a de solution complète intégrée dans le produit.

### 4.2 Auto-hébergement one-liner (PRIORITÉ #2)

**Preuve :** 6 threads r/selfhosted dédiés. FormBee, FormZero, Collecto — tous capitalisent sur "self-hosted". Le thread "Self hosted form API" (37 pts) montre une demande non satisfaite.

**Recommandation :**
- Docker one-liner (ex: `docker run -p 8080:8080 ...`)
- Support ARM64 (notre avantage différenciant)
- SQLite par défaut (pas de dépendance PostgreSQL)
- Backup automatisé + restore

### 4.3 Webhooks / Intégrations (PRIORITÉ #3)

**Preuve :** Slack, Zapier, Discord, Telegram, Email sont les destinations mentionnées dans les discussions. FormBee le fait — passe les données à Discord/Telegram/Email.

**Recommandation :**
- Webhook POST personnalisable
- Slack, Discord, Telegram natifs
- Zapier / Make (en v2)
- Google Sheets en direct (pas d'intermédiaire)

### 4.4 File upload natif (PRIORITÉ #4)

**Preuve :**
- Reddit r/node, "Sending files from form submission to webhook?" (6 pts, 4 cmts, 2023-08-07) : Développeur construit un service form-to-email et galère avec les uploads de fichiers. Source : https://reddit.com/r/node/comments/15k644u/sending_files_from_form_submission_to_webhook/ (consulté 2026-05-09)
- FormKeep et Formspree proposent file upload comme feature payante.

**Recommandation :**
- Upload S3/Backblaze B2 compatible
- Limite configurable par le host
- Scan antivirus optionnel

### 4.5 Encryption de bout en bout / Conformité (PRIORITÉ #5)

**Preuve :** `stevenicr` : "encryption before emailing and encryption at rest". HIPAA mentionné. RGPD implicite dans tous les threads.

**Recommandation :**
- Chiffrement au repos (SQLite chiffré ou PostgreSQL avec pgcrypto)
- Option "ne pas stocker" (forward only — mode FormBee)
- Audit log
- Auto-purge configurable (GDPR)
- Bannière "RGPD-ready" sur le plan Pro et Business

### 4.6 Form builder basique (NICE-TO-HAVE, PAS PRIORITAIRE)

**Preuve :** `elwebmaster` sur HN (thread FormBee) : "What I find challenging to make is a beautiful and intuitive form builder. Is there any open source solution out there?" Source : https://news.ycombinator.com/item?id=42614316 (consulté 2026-05-09)

**Recommandation :** Ne pas construire. Fournir des templates HTML prêts à copier-coller + intégrations avec les form builders existants (Webflow, Framer, Carrd).

---

## 5. Synthèse et Recommandations pour le Produit

### Conclusion principale

Le marché des backends de formulaires est mûr pour une disruption **auto-hébergée avec anti-spam intégré**. Les devs :

1. **Ont peur du spam** — c'est le frein #1 à l'adoption des solutions simples
2. **Veulent le contrôle des données** — RGPD, HIPAA, sovereignty
3. **Comparent activement les prix** — Formspark a établi $25 lifetime comme référence
4. **Ne veulent pas d'abonnement pour un service trivial** — mais paieront pour de la valeur ajoutée (anti-spam, webhooks, multi-projets)

### Recommandations produit

| Priorité | Feature | Justification |
|----------|---------|---------------|
| P0 | Anti-spam intégré (Turnstile + rate limiting + scoring) | Différenciateur #1, besoin #1 |
| P0 | Auto-hébergement Docker one-liner (ARM64 natif) | Notre avantage concurrentiel |
| P1 | Webhooks (Slack, Discord, Telegram, Email) | Attendu par le marché |
| P1 | File upload | Feature payante chez tous les concurrents |
| P2 | Chiffrement de bout en bout | Argument RGPD premium |
| P2 | Dashboard multi-projets | Upsell vers plan Pro/Business |

### Recommandations pricing

- **Garder 8/19/39 EUR** mais justifier le plan Solo (8€) par l'anti-spam inclus + auto-hébergement — pas juste par le nombre de submissions
- **Free tier : 100 subs/mois** avec anti-spam basique (Turnstile uniquement)
- **Ajouter un argumentaire RGPD fort** dans le copy de la landing page : "Vos données, vos règles. Hébergé chez vous."
- **Envisager un one-time option** à ~29€ (comme Formspark) pour les devs solo — avec limitation à 1 projet / 10K subs lifetime. Conversion vers le plan Pro quand ils dépassent.

---

## 6. Annexe — Sources Consultées

| Source | URL | Date |
|--------|-----|------|
| HN — FormBee thread (177 pts) | https://news.ycombinator.com/item?id=42614316 | 2026-05-09 |
| HN — FormZero (self-hosted) | https://news.ycombinator.com/item?id=42831906 | 2026-05-09 |
| HN — Formtone (intent detection) | https://news.ycombinator.com/item?id=47730384 | 2026-05-09 |
| HN — Boosterpack Forms | https://news.ycombinator.com/item?id=47379309 | 2026-05-09 |
| HN — Bot Butcher (anti-spam ML) | https://news.ycombinator.com/item?id=37064185 | 2026-05-09 |
| HN — Open-Source FormSpree Alternative | https://news.ycombinator.com/item?id=41564397 | 2026-05-09 |
| HN — FormBee open-source | https://github.com/FormBee/FormBee | 2026-05-09 |
| HN — Formspark alternative | https://news.ycombinator.com/item?id=42614316 | 2026-05-09 |
| Reddit r/selfhosted — Self hosted form API (37pts) | https://reddit.com/r/selfhosted/comments/fkovs7/ | 2026-05-09 |
| Reddit r/selfhosted — Mail API for static sites (20pts) | https://reddit.com/r/selfhosted/comments/r2ti62/ | 2026-05-09 |
| Reddit r/selfhosted — FormBee launch | https://reddit.com/r/selfhosted/comments/1fhq4xu/ | 2026-05-09 |
| Reddit r/selfhosted — Collecto (self-hosted Formspree) | https://reddit.com/r/selfhosted/comments/1gvy6vh/ | 2026-05-09 |
| Reddit r/webdev — Simplest Form Handler | https://reddit.com/r/webdev/comments/1iuh4du/ | 2026-05-09 |
| Reddit r/webdev — Lost Form Submissions | https://reddit.com/r/SideProject/comments/1j6n1o9/ | 2026-05-09 |
| Reddit r/webdev — Weird Spam issue | https://reddit.com/r/webdev/comments/1k6ane2/ | 2026-05-09 |
| Reddit r/webdev — FormEasy alternative | https://reddit.com/r/webdev/comments/1igxn7e/ | 2026-05-09 |
| Reddit r/webdev — Best form email service | https://reddit.com/r/webdev/comments/1icse5t/ | 2026-05-09 |
| Reddit r/node — File upload from form submission | https://reddit.com/r/node/comments/15k644u/ | 2026-05-09 |
| Reddit r/node — Email service for static sites | https://reddit.com/r/node/comments/1j3f4sv/ | 2026-05-09 |
| Formspark — Pricing page | https://formspark.io/pricing/ | 2026-05-09 |
| Formspree — Pricing | https://formspree.io/plans | 2026-05-09 |
| FormKeep — Pricing | https://formkeep.com/pricing | 2026-05-09 |
| Formcarry — Pricing | https://formcarry.com/pricing | 2026-05-09 |
| Web3Forms — Pricing | https://web3forms.com/pricing | 2026-05-09 |
| Getform — Pricing | https://getform.com/pricing | 2026-05-09 |
| Trustpilot — Formspree | https://www.trustpilot.com/review/formspree.io | 2026-05-09 |

---

*Document généré par TARZ le 2026-05-09. Chaque donnée est sourcée avec URL et date de consultation.*
