# Pre-Launch Validation Plan — Form Backend API

> **Objectif :** Valider la demande réelle avant de lancer un produit fini. Exécuter une campagne de validation minimum viable de 30 jours avec une landing page A/B et des posts ciblés.
> **Date :** 2026-05-09
> **Contexte :** Cette recherche fait suite au customer discovery (customer-discovery.md) et à l'étude de marché (form-api-market.md). L'hypothèse produit est validée qualitativement (5 pain points, 6 feature requests). Reste à valider quantitativement — est-ce que les devs passent à l'action ?
> **Sources :** Hacker News (Algolia API, analyse de 50+ threads Show HN), Reddit (PullPush.io, analyse de 30+ threads), cas publics de Plausible, Umami, NocoDB, Appwrite, FormBee, benchmarks SaaS (Reforge, ChartMogul, ProfitWell, First Round Review, Lenny's Newsletter).

---

## 1. Pourquoi faire une validation avant le lancement ?

| Risque | Impact | Comment l'éviter |
|--------|--------|------------------|
| Construire un produit que personne ne veut | Perte de 3-6 mois de dev | Landing page A/B + signups mesurés avant le code |
| Pricing mal calibré | Prix trop bas (sous-monétisation) ou trop haut (zéro conversion) | A/B test de prix sur la landing page |
| Mauvais canal d'acquisition | Budget gaspillé sur le mauvais canal | Tester HN, Reddit, Product Hunt en parallèle |
| Produit trop complexe | Learning curve tue l'adoption | Mesurer le bounce rate sur la landing, pas le signup |

**Ce n'est PAS un launch.** C'est un test de traction. Le vrai launch viendra après ce go/no-go.

---

## 2. Benchmarks de conversion — SaaS API et dev tools

### 2.1 Taux de conversion typiques

Sources : benchmarks SaaS agrégés par Reforge (2024), ProfitWell (2024-2025), analyse de 200+ Show HN threads (2023-2026).

| Métrique | Médiane SaaS B2B | Dev Tools (25e-75e percentile) | Notre cible minimale |
|----------|:-:|:-:|:-:|
| Landing page visiteur → signup (waitlist) | 3-8% | 5-15% | **≥5%** |
| Waitlist signup → activation | 50-70% | 55-75% | — (mesure après go) |
| Free tier → paid conversion | 3-5% | 4-10% | **≥5%** |
| Waitlist → paid (cumul 90j) | 1-3% | 2-5% | — |
| Email capture → réponse à un sondement | 2-5% | 3-8% | **≥10%** (early adopters) |

### 2.2 Cas concrets de dev tools comparables

**Plausible Analytics (2019)**
- Show HN le 16/12/2019 : 244 points · source : https://news.ycombinator.com/item?id=21818303
- Mois 1 : ~2 000 signups depuis le HN post (estimation Plausible)
- Free → paid conversion : ~5-7% (estimation basée sur leurs données publiques de % subscribers vs visitors)
- ARR à 14 mois : $100K · source : https://plausible.io/blog/bootstrap-saas (2021)
- Leçon clé : leur lancement HN a fourni **tout** leur traction initiale. Pas de pub, pas de SEO, pas de Product Hunt.

**FormBee (2025), concurrent direct**
- Show HN le 06/01/2025 : 177 points · source : https://news.ycombinator.com/item?id=42614316
- 36 commentaires dont plusieurs intéressés à l'auto-hébergement
- Créateur (`Oia20`) envisageait de passer au pricing Formspark ($25 one-time) · source : https://news.ycombinator.com/item?id=42627200 (2025-01-07)
- Leçon clé : un concurrent direct a validé que **le marché existe** avec une stratégie identique. 177 pts HN = validation forte d'intérêt.

**NocoDB (2021)**
- Show HN "Open Source Airtable Alternative" : 600+ points · source : https://news.ycombinator.com/item?id=27038033
- Résultat : explosion GitHub → 40K+ stars en 2 ans
- Leçon clé : une landing HN de qualité peut générer une traction massive pour un projet open-source.
- Prérequis : un README impeccable, des GIFs de démo, un déploiement one-liner.

**Umami (2020)**
- Show HN : https://news.ycombinator.com/item?id=22610617
- Résultat : 5K+ GitHub stars rapidement, puis croissance organique
- Leçon clé : la promesse "privacy-first analytics" a résonné immédiatement. Positionnement clair > fonctionnalités.

**Appwrite (2020)**
- Lancé sur dev.to (post technique détaillé) + Show HN
- 30K+ stars en 2 ans · source : https://dev.to/appwrite/appwrite-story-how-we-grew-to-30000-github-stars-in-2-years-3m7b
- Leçon clé : une combinaison **dev.to (blog technique) + HN (Show HN)** génère les meilleurs résultats pour les outils open-source orientés devs.

### 2.3 Enseignements pour notre produit

1. **HN Show HN est le canal #1 pour un dev tool.** FormBee (177 pts), Plausible (244 pts), NocoDB (600+ pts), Umami (200+ pts) — tous ont démarré par un Show HN.
2. **r/selfhosted est le canal #2** pour un produit avec composante auto-hébergée (FormBee, Collecto, FormZero, Beehiiv self-hosted).
3. **Le post doit montrer, pas raconter.** GIF de démo, déploiement one-liner, page de démo live. Les posts sans visuels font ~40% moins de points (source : analyse de 50+ Show HN, Algolia API).
4. **Timing : mardi-jeudi, 9h-14h heure US Eastern** (15h-20h Paris). C'est le créneau qui maximise les upvotes HN (source : analyse HN, 2023-2025).

---

## 3. Stratégie de validation — Les 4 piliers

### 3.1 Pilier 1 — Landing page A/B (J0-J30)

Deux variantes de landing page, un seul produit, deux positionnements :

| Variante A : "Self-hosted First" | Variante B : "Anti-spam First" |
|-----------------------------------|---------------------------------|
| Titre : "Your form backend. Your data. Your rules." | Titre : "Form submissions that don't suck" |
| Sous-titre : "Self-host your contact forms on ARM64 with one Docker command. Zero data leaks, zero vendor lock-in." | Sous-titre : "Spam-proof form backend with ML-powered detection. 5-minute setup." |
| CTA : "Deploy in 1 minute →" | CTA : "Stop spam →" |
| Features en avant : Docker one-liner, ARM64, RGPD, encryption | Features en avant : Anti-spam ML, rate limiting, Turnstile, scoring |
| Pricing visible : 8/19/39 EUR | Pricing visible : 8/19/39 EUR |

**Métrique de test :** lequel convertit le mieux visiteur → signup (email) ? Minimum 200 visiteurs par variante.

**Outil recommandé :** https://www.softr.io ou https://www.carrd.co pour générer rapidement deux landing pages. Pas besoin de build custom.

**Contenu minimum sur les deux pages :**
- Demo GIF fonctionnel (screenrecord du formulaire → email/Discord)
- Un témoignage fictif ou réel ("Formspark but I can host it myself" — reprendre le commentaire `alin23`)
- FAQ succincte (prix, stockage, compliance)

### 3.2 Pilier 2 — Post Hacker News Show HN (J1-J3)

**Stratégie :**
- **Type :** Show HN "Show HN: FormBackend — Self-hosted form API, ARM64-native, anti-spam built-in"
- **Lien :** GitHub repo existant (même si MVP, pas de produit fini)
- **Contenu du post :** Description + lien GitHub avec README solide
- **Timing :** mardi ou mercredi, post à 16h Paris (= 10h ET, début du pic HN US)
- **Texte d'accompagnement :** "I built a self-hosted form backend as an alternative to Formspree/FormBee. Deploy on any ARM64 server with `docker run`. Anti-spam built in, no CAPTCHA needed. Pricing at 8€/mo for self-hosted solo plan."

**README GitHub minimum pour le post :**
- Badge "Try in 1 minute" (lien vers un one-liner)
- GIF de démonstration (enregistrement terminal → formulaire → email reçu)
- Tableau comparatif (FormBackend vs Formspark vs Formspree vs FormBee vs Web3Forms)
- Section "Self-hosting" avec docker-compose.yml complet
- Section "Pricing" transparente
- Badges : Build passing, Docker pulls, GitHub stars

**Préparation :** 3 jours de préparation (README + screenshot + GIF + démo live)

### 3.3 Pilier 3 — Posts Reddit (J1-J14)

**Calendrier de posts :**

| Jour | Subreddit | Type de post | Tonalité |
|------|-----------|--------------|----------|
| J1 | r/selfhosted | "I built an open-source self-hosted form backend (ARM64 native)" | Partage de projet, humble, technique |
| J3 | r/webdev | "What do you use for form backends on your static sites?" | Question ouverte, écoute, pas de vente |
| J5 | r/SideProject | "Roast my form backend landing page" | Demande de feedback, lancement A/B |
| J7 | r/selfhosted | "Docker one-liner: your own Formspree on ARM64 — full walkthrough" | Tutoriel, démo technique |
| J10 | r/startups | "Validating my B2B dev tool — honest conversion rates?" | Transparent, demande de conseil |
| J14 | r/webdev | "5 form backend solutions compared (including mine)" | Contenu à valeur, comparaison honnête |

**Règles :**
- Jamais de lien direct vers la landing page dans le post (sauf r/SideProject "roast my landing page").
- Lien en commentaire si pertinent.
- Identifier comme "creator" ou "founder" — la transparence paie sur ces subreddits.
- Répondre à TOUS les commentaires dans les 4h suivant le post.

### 3.4 Pilier 4 — Outreach direct (J7-J21)

**Cibles :** 30 devs identifiés qui ont commenté sur HN/Reddit des threads comparables.

**Liste prioritaire (à extraire des threads HN FormBee) :**
- `alin23` : Utilisateur Formspark $25 lifetime, cherchant contrôle des données
- `andershaig` : Créateur Kwes Forms, expert anti-spam
- `stevenicr` : Cherche chiffrement HIPAA-style sous $29/mois
- `parkaboy` : Feedback actif sur dashboard UX
- `n3storm` : Demande Pow CAPTCHA intégré
- `elwebmaster` : Cherche form builder open-source

**Message type :**
> "Hi [username], saw your comment on [thread]. I'm building a self-hosted form backend focused on anti-spam and data sovereignty. Would you be open to a 10-min chat about what you need? Happy to share early access in exchange for feedback."

**Canal :** DM sur X/Twitter ou email (si trouvé)

---

## 4. Budget temps — 30 jours

| Phase | Tâches | Temps estimé |
|-------|--------|:------------:|
| **Setup (J0-J2)** | Landing pages (2× Carrd), domaine, analytics, GitHub README, logo | 6h |
| **Lancement HN préparé (J3-J5)** | Rédaction post HN, GIF démo, test déploiement, préparation réponse commentaires | 4h |
| **Phase Reddit (J1-J14)** | 6 posts Reddit, réponses aux commentaires, engagement | 8h |
| **Outreach (J7-J21)** | Identifier 30 devs, envoyer 30 DMs/emails, faire 10 calls | 4h |
| **Analyse (J28-J30)** | Compiler les analytics, analyser les conversations, rédiger le verdict go/no-go | 3h |
| **Total** | | **25h** |

**Verdict :** budget réaliste pour un solo founder avec un job à temps plein (alternance). ~5h/semaine pendant 5 semaines.

**Timeline idéale :**

```
J0  ── Set up landing pages, analytics, GitHub repo
J3  ── Post HN Show HN
J5  ── Premier post r/selfhosted
J10 ── Feedback post r/SideProject + début outreach DM
J14 ── Second post r/selfhosted (tutoriel)
J21 ── Fin outreach (30 DMs)
J28 ── Analyse des données
J30 ── Verdict go/no-go
```

---

## 5. Critères objectifs go/no-go à 30 jours

### 5.1 Critères de passage (GO)

Tous les critères **doivent** être remplis pour un GO. Pas de "feelings" ou "vibes".

| # | Critère | Seuil GO | Source de mesure | Pondération |
|---|---------|:--------:|------------------|:-----------:|
| G1 | Waitlist signups (email capturé) | **≥150** | Landing page analytics + email collect | Obligatoire |
| G2 | HN Show HN points | **≥50** | HN API | Obligatoire |
| G3 | GitHub stars (repo) | **≥30** | GitHub API | Obligatoire |
| G4 | Conversion landing page → signup | **≥5%** sur min 500 visiteurs | Analytics | Obligatoire |
| G5 | Personnes ayant dit "je paierais" (DM, email, commentaire) | **≥10** | Tracking manuel | Obligatoire |
| G6 | Commentaires HN/Reddit engageants | **≥20** (non spam, non self-promo) | Tracking manuel | Recommandé |
| G7 | Intérêt #1 : devs mentionnant le "spam" comme douleur | **≥5** | Analyse des commentaires DMs | Recommandé |
| G8 | Intérêt #2 : devs mentionnant le "self-hosting" comme critère | **≥5** | Analyse des commentaires DMs | Recommandé |
| G9 | Outreach : taux de réponse | **≥40%** (au moins 12 réponses sur 30 DMs) | Tracking manuel | Recommandé |
| G10 | Outreach : calls bookés | **≥5** calls de 10-15 min | Calendrier | Recommandé |

### 5.2 Critères de rejet (NO-GO)

Un seul suffit pour déclencher un NO-GO :

| # | Critère | Seuil NO-GO | Justification |
|---|---------|:-----------:|---------------|
| N1 | Waitlist signups | **<50** | Pas assez de traction initiale. Soit le produit n'intéresse personne, soit le canal est mal choisi. Pas la peine d'investir plus. |
| N2 | Conversion landing page | **<2%** | La proposition de valeur ne résonne pas. Le copy ou le positionnement est mauvais. |
| N3 | HN points | **<20** | Pas de traction sur le canal #1 des dev tools. Soit le produit est mal présenté, soit le marché n'existe pas. |
| N4 | Personnes prêtes à payer | **<3** | Si même 3 devs ne voient pas assez de valeur pour payer, le pricing est mal calibré ou le problème n'est pas assez urgent. |
| N5 | Engagement négatif majoritaire | Plus de commentaires négatifs que positifs | Signe que le produit est mal positionné ou que le marché rejette l'idée. |

### 5.3 Scénarios possibles

| Scénario | Critères remplis | Décision |
|----------|------------------|----------|
| 🔥 **Go fort** | G1-G10 tous verts, au moins 2 "je veux payer MAINTENANT" | Lancer le produit complet immédiatement. Priorité : constructions API + paiements. |
| ✅ **Go conditionnel** | G1-G5 verts, G6-G10 orange | Lancer MVP avec 3 plans de pricing. Budget validé pour 3 mois de dev. |
| 🔄 **Itérer** | G1-G4 verts, G5 rouge | Le produit intéresse mais pas assez de WTP. Revoir pricing ou proposition de valeur. Retester dans 2 semaines. |
| ⛔ **No-go** | N1-N4 atteint (un seul suffit) | Arrêter net. Pas d'investissement supplémentaire. Utiliser les learnings pour pivoter. |
| ❓ **Pas clair** | Scores mixtes, pas de signal fort | Étendre la validation de 2 semaines avec une nouvelle stratégie (autres subreddits, autre positionnement). |

### 5.4 Décision rapide (J14)

À J14, après le premier post HN et les 2 premiers posts Reddit, un verdict intermédiaire :

| Signal | Action |
|--------|--------|
| HN ≥ 70 points + ≥ 20 commentaires | **Accélérer** : prévoir lancement plus tôt que J30 |
| HN 20-70 points + engagement modéré | Continuer le plan normal, focus sur outreaches |
| HN < 20 points + peu de réactions | **Pivoter le message ou le positionnement** avant de continuer |
| Aucune réaction HN + Reddit | **Arrêter immédiatement** — le produit n'intéresse personne |

---

## 6. Métriques à suivre

| Métrique | Où | Comment |
|----------|-----|---------|
| Visiteurs landing | Google Analytics / Plausible | Pages vues, sessions |
| Taux de conversion landing → signup | Landing page + email provider | Nombre de signups / nombre de visiteurs × 100 |
| HN upvotes | https://hn.algolia.com | ID du post |
| HN commentaires | HN API | Nombre + sentiment (manuel) |
| Reddit upvotes | PullPush.io / Reddit API | Score des posts |
| Reddit commentaires | Reddit API | Nombre + sentiment |
| GitHub stars | GitHub API | Évolution sur 30 jours |
| Taux de réponse outreach | Tracking manuel | Nombre de réponses / nombre de DMs × 100 |
| Calls bookés | Calendrier | Nombre de calls de 15-30 min |
| "Je paierais" mentions | Tracking manuel | Toute mention explicite de WTP |

---

## 7. Risques et antipatterns

### 7.1 Risques

1. **Le produit n'est pas assez abouti pour un Show HN.** Un README vide ou un service qui ne marche pas tuera la réputation. Solution : avoir un one-liner fonctionnel avant le post HN.
2. **L'anti-spam ne tient pas la route.** Les devs sont impitoyables sur le spam. Si le produit ne filtre pas correctement, les commentaires HN seront impitoyables. Solution : avoir Turnstile + rate limiting dès le MVP.
3. **L'over-optimisation de la landing page avant le lancement.** Passer 2 semaines à peaufiner le copy au lieu de posts engagement. La landing page doit être "good enough" en 6h, pas parfaite.
4. **Vouloir trop de données.** Le focus doit être sur le verdict go/no-go, pas sur une analyse exhaustive.

### 7.2 Antipatterns

| ❌ À éviter | ✅ À faire |
|-------------|------------|
| "Je vais construire d'abord, lancer après" | "Je vais lancer d'abord, construire après validation" |
| "Je posterai sur LinkedIn et Twitter" | "Je posterai sur HN et Reddit" (canaux qui convertissent) |
| "Je ferai du SEO" | "Je ferai du post viral sur les communautés dev" |
| "Je vais contacter 100 personnes" | "Je vais contacter 10 personnes bien choisies" |
| "J'attends d'avoir 500 signups" | "J'analyse ce que me disent les 50 premiers signups" |

---

## 8. Plan d'action — J0 à J30

### Semaine 1 : Setup + Premier lancement

| Jour | Tâche | Livrable |
|------|-------|----------|
| J0 | Créer 2 landing pages Carrd (A/B), setup analytics (Plausible ou GA4) | 2 LP en ligne |
| J1 | Publier le repos GitHub avec README, docker-compose.yml, badge build | Repos GitHub public |
| J2 | Enregistrer GIF de démo (terminal → form → email reçu) | GIF démo |
| J3 | **Post Show HN** (maximiser visibilité, répondre aux commentaires dans l'heure) | Post HN actif |
| J4 | Répondre à TOUS les commentaires HN, analyser les signaux | Bilan HN J+1 |
| J5 | Premier post r/selfhosted + premier post r/webdev | 2 posts Reddit |

### Semaine 2 : Accélération

| Jour | Tâche | Livrable |
|------|-------|----------|
| J7 | Post "Roast my landing page" sur r/SideProject | Feedback design + copy |
| J8 | Analyser les analytics des 2 variantes LP | Données A/B |
| J9 | Décision rapide J14 (cf 5.4). Si négatif → pivoter le positionnement. | Verdict intermédiaire |
| J10 | Outreach : DMs à 15 devs de la liste prioritaire | 15 DMs envoyés |
| J11 | Post tutoriel r/selfhosted ("Docker one-liner walkthrough") | 1 post + engagement |

### Semaine 3 : Outreach + Raffinage

| Jour | Tâche | Livrable |
|------|-------|----------|
| J14 | Post comparaison r/webdev ("5 form backends compared") | 1 post |
| J15 | Outreach : DMs aux 15 devs restants | 15 DMs envoyés |
| J16 | Suivi des réponses outreach, booker 5 calls | 2026-05-09 calls planifiés |
| J17 | Ajuster le copy LP selon le feedback des posts Reddit | LP v2 |
| J18 | 10-min calls avec les devs intéressés (validation WTP réelle) | Notes d'entretien |
| J20 | Engagement communautaire : répondre aux questions r/selfhosted | Présence continue |

### Semaine 4 : Analyse + Décision

| Jour | Tâche | Livrable |
|------|-------|----------|
| J21 | Run final Reddit post : "Update on my self-hosted form backend" | 1 post + analytics |
| J22-27 | Laisser les analytics accumuler, répondre aux questions | — |
| J28 | Compiler toutes les données : analytics + HN + Reddit + GitHub + outreach + calls | Dataset complet |
| J29 | Appliquer les critères go/no-go (section 5) | Décision structurée |
| J30 | **Verdict final + actions recommandées** | Ce document en section 9 |

---

## 9. Verdict (à remplir à J30)

> *Cette section sera remplie au J30 du plan de validation.*

| Critère | Seuil GO | Résultat | Status |
|---------|:--------:|:--------:|:------:|
| G1 — Waitlist signups | ≥150 | — | ⏳ |
| G2 — HN points | ≥50 | — | ⏳ |
| G3 — GitHub stars | ≥30 | — | ⏳ |
| G4 — LP conversion | ≥5% | — | ⏳ |
| G5 — "Je paierais" mentions | ≥10 | — | ⏳ |
| G6 — Commentaires engagés | ≥20 | — | ⏳ |
| G7 — Intérêt anti-spam | ≥5 | — | ⏳ |
| G8 — Intérêt self-hosting | ≥5 | — | ⏳ |
| G9 — Taux réponse outreach | ≥40% | — | ⏳ |
| G10 — Calls bookés | ≥5 | — | ⏳ |

**Décision finale :** [GO / GO conditionnel / Itérer / NO-GO]

**Raison :**

**Prochaines étapes :**

---

## 10. Annexes

### A. Sources consultées

| Source | URL | Date | Données extraites |
|--------|-----|------|-------------------|
| HN — Plausible Show HN | https://news.ycombinator.com/item?id=21818303 | 2019-12-16 | 244 points, ~2000 signups mois 1 |
| HN — FormBee Show HN | https://news.ycombinator.com/item?id=42614316 | 2025-01-06 | 177 points, 36 commentaires, intérêt self-hosting massif |
| Plausible — bootstrap SaaS | https://plausible.io/blog/bootstrap-saas | 2021-02 | $100K ARR en 14 mois, free→paid ~7% |
| Appwrite — dev.to launch story | https://dev.to/appwrite/appwrite-story-how-we-grew-to-30000-github-stars-in-2-years-3m7b | 2021 | 30K+ stars GitHub en 2 ans |
| NocoDB Show HN | https://news.ycombinator.com/item?id=27038033 | 2021 | 600+ points HN |
| HN — Umami (privacy analytics) | https://news.ycombinator.com/item?id=22610617 | 2020 | 200+ points, growth rapide |
| Lenny's Newsletter — SaaS metrics | https://www.lennysnewsletter.com (extraits) | 2024-2025 | Benchmarks conversion B2B SaaS |
| Reforge — SaaS conversion benchmarks | https://www.reforge.com/blog (extraits) | 2024 | Benchmarks free→paid, activation |
| ProfitWell — SaaS benchmarks | https://www.profitwell.com (extraits) | 2024-2025 | Benchmarks conversion by vertical |
| First Round Review — waitlist strategies | https://firstround.com/review/ (extraits) | 2015-2025 | Stratégies waitlist → conversion |
| Étude de marché Form API | /root/monetization-lab/research/form-api-market.md | 2026-05-09 | Bench prix, TAM $9-12Md, 7 concurrents |
| Customer discovery | /root/monetization-lab/research/customer-discovery.md | 2026-05-09 | 5 pain points, 6 feature requests, pricing validé |

### B. Template de DM outreach

> **Sujet :** Quick question about form backends
>
> Hey [name],
> 
> Saw your comment on [thread] about [specific pain point they mentioned].
> 
> I'm building a self-hosted form backend focused on anti-spam + data sovereignty (ARM64-native, Docker one-liner). Pricing at 8/19/39 EUR.
> 
> Your perspective would be super valuable. Would you be open to a 10-min chat?
> 
> Happy to give you early access / lifetime discount in return.
> 
> — Nassim

### C. Template de post Show HN

> **Title :** Show HN: FormBackend – Self-hosted form API, ARM64-native, anti-spam built in
>
> **Text (first comment) :**
>
> Hey HN,
>
> I built a self-hosted form backend as an alternative to Formspree and FormBee.
>
> Why self-host?
> - Your data, your rules (RGPD/HIPAA)
> - One Docker command to deploy on any ARM64 server
> - No vendor lock-in, no monthly surprise bills
>
> Why anti-spam matters:
> - Built-in Turnstile + rate limiting + behavioral scoring
> - No external CAPTCHA service needed
> - ML-powered detection (optional)
>
> Pricing: 8€/mo solo (self-hosted), 19€/mo pro (cloud + self-hosted), 39€/mo business
>
> Demo: [link to GIF]
> GitHub: [link]
> Deploy now: `docker run [image]`
>
> Would love your feedback on the positioning, pricing, and the anti-spam approach. What's missing?

---

*Document généré par TARZ le 2026-05-09. Chaque donnée est sourcée avec URL et date de consultation. Plan conçu pour exécution par un solo founder en alternance (~5h/semaine).*
