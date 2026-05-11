# Phase 2 Execution Plan — Form Backend API

> **Synthèse des 3 recherches :** Customer Discovery (pain points + pricing), Channel Validation (acquisition), Pre-Launch Validation Plan (campagne 30 jours)
> **Date :** 2026-05-09
> **Contexte :** MVP construit. Marché validé qualitativement (5 pain points, 6 feature requests, pricing 8/19/39 EUR). Reste à valider quantitativement — l'exécution commence maintenant.
> **Contrainte :** Solo founder en alternance (~5h/semaine). 30 jours max pour le verdict go/no-go.

---

## 1. Synthèse des Insights Clés

### Ce qu'on sait (certitudes après recherche)

| Insight | Source | Impact sur Phase 2 |
|---------|--------|-------------------|
| Le spam est le #1 pain point, mentionné dans TOUTES les discussions | Customer Discovery | Anti-spam intégré est le différenciateur #1. Ne pas lancer sans. |
| Formspark ($25 lifetime) est le benchmark psychologique du marché | Customer Discovery | Plan Solo à 8€/mois doit être justifié par anti-spam + self-hosting, pas par le nombre de submissions |
| Le self-hosting est une demande massive et croissante (6+ threads Reddit) | Customer Discovery | Docker one-liner ARM64 est notre avantage concurrentiel |
| HN Show HN est le canal #1 pour un dev tool (FormBee 177pts, Plausible 244pts) | Channel Validation + Pre-Launch | Le lancement HN est l'événement central de Phase 2 |
| Reddit r/selfhosted + r/webdev = 12+ threads actifs en 2025-2026 | Channel Validation | Canal de traction immédiate, à exploiter en parallèle de HN |
| SEO /formspree-alternative : faible volume (300-900/mois) mais intention d'achat max | Channel Validation | Créer la page MAINTENANT (le SEO met 3-6 mois) |
| Budget temps réaliste : 25h sur 30 jours (~5h/semaine) | Pre-Launch Plan | Le plan est faisable pour un alternant |

### Ce qu'on ne sait pas encore (ce que Phase 2 doit valider)

| Question | Comment on la valide | Seuil de validation |
|----------|---------------------|-------------------|
| Est-ce que les devs passent à l'action (pas seulement commentent) ? | Waitlist signups ≥ 150 | GO si ≥150, NO-GO si <50 |
| Est-ce que le pricing 8/19/39 EUR convertit ? | Landing page A/B, conversion ≥ 5% | GO si ≥5%, NO-GO si <2% |
| Est-ce que le positionnement "self-hosted first" ou "anti-spam first" gagne ? | A/B test des 2 variantes de landing page | La variante gagnante devient le positionnement principal |
| Est-ce que HN valide le produit ? | HN points ≥ 50 | GO si ≥50, NO-GO si <20 |
| Est-ce que des devs veulent vraiment payer ? | Mentions "je paierais" ≥ 10 | GO si ≥10, NO-GO si <3 |

---

## 2. Priorisation des Actions (ROI Décroissant)

### 🔴 P0 — Faire cette semaine (J0-J7)

| # | Action | Justification | Temps |
|---|--------|--------------|:-----:|
| **P0.1** | **Anti-spam MVP dans le produit** : Turnstile + rate limiting IP + scoriing basique | Sans ça, le lancement HN sera impitoyable. Les devs testent le spam filtering avant tout. Risque #1 du plan de validation. | 4-6h |
| **P0.2** | **Docker one-liner fonctionnel + test ARM64** : `docker run -p 8080:8080 formbackend/api` qui marche sur un VPS ARM64 de zéro | La promesse #1 du produit. Doit marcher PARFAITEMENT avant Show HN. | 2-3h |
| **P0.3** | **Landing page A/B (2 variantes)** : Carrd/Softr, domain, analytics (Plausible), email capture | Sans landing page, pas de waitlist. Les 2 variantes testent le positionnement. | 4-6h |
| **P0.4** | **Landing page SEO /formspree-alternative** : tableau comparatif, captures, CTA | Le SEO met 3-6 mois à porter ses fruits. Lancer MAINTENANT ou ne pas le faire du tout. | 2h |
| **P0.5** | **GitHub README complet + GIF démo + docker-compose.yml** | Requis pour le Show HN. README = la landing page des devs. | 3-4h |

**Total P0 : 15-21h** (étalable sur 7 jours à ~3h/jour)

### 🟡 P1 — Semaine 2-3 (J7-J21)

| # | Action | Justification | Temps |
|---|--------|--------------|:-----:|
| **P1.1** | **Post Show HN** (mardi, 16h Paris = 10h ET) | L'événement central. Timing optimal, préparation README + GIF faite en P0. | 1h post + 3h réponses |
| **P1.2** | **6 posts Reddit** (calendrier : r/selfhosted, r/webdev, r/SideProject) | Traction immédiate, complément HN. Calendrier détaillé dans le plan de validation. | 8h (étalé sur 14 jours) |
| **P1.3** | **Outreach 30 devs** (DMs/emails aux commentateurs HN/Reddit identifiés) | Validation WTP réelle. Les commentaires ne suffisent pas — il faut des conversations. | 4h |
| **P1.4** | **Blog post #1** : "Form to Email API: Complete Guide 2026" (SEO) | Capture le trafic informationnel, backlinks naturels depuis Reddit/HN | 2-3h |

**Total P1 : 16-19h**

### 🟢 P2 — Semaine 4 (J21-J30)

| # | Action | Justification | Temps |
|---|--------|--------------|:-----:|
| **P2.1** | **Analyser les données** : analytics LP, HN points, Reddit engagement, GitHub stars, outreach responses | Compiler le dataset pour la décision go/no-go | 2h |
| **P2.2** | **Appliquer les critères go/no-go** (10 critères GO, 5 critères NO-GO) | Décision structurée, pas de "feelings" | 1h |
| **P2.3** | **Rédiger le verdict + recommandations** | Output livrable dans ce document section 9 | 1h |

**Total P2 : 4h**

---

## 3. Calendrier Détaillé (30 Jours)

```
Semaine 1 : Setup produit + landing pages
  J0  (lun) - Anti-spam MVP : Turnstile + rate limiting basique
  J1  (mar) - Docker one-liner : test sur VPS ARM64, corriger les bugs
  J2  (mer) - Landing page Var A "Self-hosted First" + SEO /formspree-alternative
  J3  (jeu) - Landing page Var B "Anti-spam First" + setup analytics Plausible
  J4  (ven) - GitHub README : badges, docker-compose.yml, GIF démo, tableau comparatif
  J5  (sam) - Test complet : le one-liner marche-t-il de zéro ? Corriger.
  J6  (dim) - Repos OU finaliser les assets (logo, screenshots)

Semaine 2 : Lancement HN + Reddit
  J7  (lun) - Préparer le post Show HN, pré-engagement HN (commenter 3-5 threads dev)
  J8  (mar) - POST SHOW HN (16h Paris). Répondre à TOUS les commentaires dans l'heure.
  J9  (mer) - Post r/selfhosted "I built an open-source self-hosted form backend"
  J10 (jeu) - Bilan HN J+2 : analyser les signaux, appliquer décision rapide J14
  J11 (ven) - Post r/webdev "What do you use for form backends?" (question ouverte)
  J12 (sam) - Engagement HN/Reddit : répondre aux questions, suivre les threads
  J13 (dim) - Repos

Semaine 3 : Outreach + Raffinage
  J14 (lun) - DÉCISION RAPIDE (cf critères J14). Post r/SideProject "Roast my LP"
  J15 (mar) - Outreach : DMs à 15 devs prioritaires (alin23, andershaig, etc.)
  J16 (mer) - Outreach : DMs aux 15 devs restants
  J17 (jeu) - Post tutoriel r/selfhosted "Docker one-liner walkthrough"
  J18 (ven) - Suivi réponses outreach + 10-min calls avec intéressés
  J19 (sam) - Engagement communautaire : répondre aux questions, présence continue
  J20 (dim) - Repos

Semaine 4 : Analyse + Décision
  J21 (lun) - Post comparaison r/webdev "5 form backends compared"
  J22-26     - Laisser les analytics accumuler, répondre aux questions
  J27 (dim)  - Compiler toutes les données (cf section 5)
  J28 (lun)  - Appliquer les critères go/no-go
  J29 (mar)  - Rédiger le verdict final
  J30 (mer)  - LIVRABLE : Verdict + Kanban tasks Phase 3
```

---

## 4. Ressources Nécessaires

### Déjà disponibles

| Ressource | Statut | Détail |
|-----------|--------|--------|
| MVP Form Backend API | ✅ Construit | ~1500 lignes Python, 6 templates, 395 tests, Docker, Alembic |
| Recherche marché | ✅ 3 documents | Customer discovery, Channel validation, Pre-launch plan |
| Pricing | ✅ Défini | 8/19/39 EUR |
| GitHub repo | ⚠️ À préparer | README, GIF démo, docker-compose.yml à créer |
| Domaine | ❓ À confirmer | Nécessaire pour les landing pages |

### À acquérir / configurer

| Ressource | Coût estimé | Pourquoi |
|-----------|:-----------:|----------|
| Carrd Pro ou Softr | 9-19€/mois | Landing pages A/B (pas de build custom) |
| Plausible Analytics | Gratuit (self-hosted) ou 9€/mois | Analytics légers, privacy-first |
| Domaine landing page | 10-15€/an | ex: formbackend.dev ou formspree-alternative.com |
| VPS ARM64 de test | 3-5€/mois (Hetzner CX22) | Pour valider le one-liner de zéro |
| Compte X/Twitter (DM) | Gratuit | Outreach aux devs |
| Outil GIF/screencast | Gratuit (Kap, OBS) | Démo pour HN et Reddit |

**Budget Phase 2 : ~30-40€** (hors VPS existant)

### Compétences requises

| Compétence | Disponible ? | Sinon, comment ? |
|------------|:------------:|------------------|
| Dev Python/FastAPI | ✅ Oui | MVP déjà construit |
| Docker / ARM64 | ✅ Oui | Produit déjà dockerisé |
| Rédaction technique (FR/EN) | ✅ Oui | Pour posts HN + Reddit |
| Design landing page | ⚠️ Partiel | Utiliser Carrd templates (pas de custom CSS) |
| SEO technique | ⚠️ Basique | Suffisant pour /formspree-alternative |
| Outreach / vente | ⚠️ À développer | Template de DM fourni dans pre-launch plan |

---

## 5. Métriques Clés et Seuils de Décision

### Tableau de bord Phase 2

| Métrique | Où | Cible S1 | Cible S2 | Cible S3 | Cible J30 |
|----------|-----|:--------:|:--------:|:--------:|:---------:|
| Waitlist signups | Landing page analytics | 20 | 80 | 120 | **≥150** |
| Conversion LP → signup | Analytics | — | ≥3% | ≥4% | **≥5%** |
| HN Show HN points | HN API | — | **≥50** (J8) | — | **≥50** |
| GitHub stars | GitHub API | 5 | 15 | 25 | **≥30** |
| Posts Reddit | Reddit API | 2 | 4 | 6 | **6 posts** |
| DMs outreach envoyés | Tracking manuel | — | 15 | 30 | **30 DMs** |
| Taux réponse outreach | Tracking manuel | — | — | ≥30% | **≥40%** |
| Calls bookés | Calendrier | — | — | 3 | **≥5 calls** |
| "Je paierais" mentions | Tracking manuel | — | 3 | 5 | **≥10** |

### Décision rapide J14

| Signal HN à J+1 | Action |
|-----------------|--------|
| ≥ 70 points + ≥ 20 commentaires | **Accélérer** : préparer le lancement produit avant J30 |
| 20-70 points + engagement modéré | Continuer le plan normal, focus outreach |
| < 20 points + peu de réactions | **Pivoter le message ou le positionnement** |
| Aucune réaction (HN + Reddit) | **Arrêter immédiatement** |

### Décision finale J30

**GO si TOUS les critères obligatoires sont remplis :**
- G1 : Waitlist signups ≥ 150
- G2 : HN points ≥ 50
- G3 : GitHub stars ≥ 30
- G4 : Conversion LP ≥ 5% sur min 500 visiteurs
- G5 : "Je paierais" mentions ≥ 10

**NO-GO si UN SEUL critère NO-GO est atteint :**
- N1 : Waitlist signups < 50
- N2 : Conversion LP < 2%
- N3 : HN points < 20
- N4 : Personnes prêtes à payer < 3
- N5 : Engagement négatif majoritaire

---

## 6. Go/No-Go Checkpoints

### Checkpoint 1 — J7 (Fin Semaine 1)
**Vérification :** Le produit est-il prêt pour Show HN ?

- [ ] Anti-spam MVP fonctionnel (Turnstile + rate limiting)
- [ ] Docker one-liner testé sur VPS ARM64 vierge (marche du premier coup)
- [ ] Landing page Var A en ligne + analytics
- [ ] Landing page Var B en ligne
- [ ] Page /formspree-alternative en ligne
- [ ] GitHub repo public avec README complet + GIF démo

**Si non :** Décaler le Show HN de 1 semaine. Ne pas lancer avec un produit cassé.

### Checkpoint 2 — J9 (J+1 Show HN)
**Vérification :** Le lancement HN a-t-il fonctionné ?

- [ ] HN points ≥ 70 → ACCÉLÉRER
- [ ] HN points 20-70 → Continuer plan normal
- [ ] HN points < 20 → Pivoter le message
- [ ] HN + Reddit = aucune réaction → ARRÊTER

### Checkpoint 3 — J14 (Fin Semaine 2)
**Vérification :** Les premiers signaux justifient-ils de continuer ?

- [ ] Waitlist ≥ 50 signups
- [ ] Conversion LP ≥ 3%
- [ ] GitHub stars ≥ 15
- [ ] Au moins 1 post Reddit avec > 20 upvotes
- [ ] Au moins 3 personnes ont dit "je paierais"

### Checkpoint 4 — J21 (Fin Semaine 3)
**Vérification :** L'outreach valide-t-il la WTP ?

- [ ] ≥ 15 DMs envoyés
- [ ] Taux de réponse ≥ 30%
- [ ] ≥ 3 calls bookés
- [ ] Témoignages positifs des calls

### Checkpoint 5 — J30 (Décision Finale)
**Vérification :** Go ou No-Go ?

- [ ] G1-G5 tous verts → **GO** (lancer le produit complet)
- [ ] G1-G4 verts, G5 orange → **GO conditionnel** (lancer MVP, valider pricing en cours de route)
- [ ] G1-G4 verts, G5 rouge → **ITÉRER** (revoir pricing, retester 2 semaines)
- [ ] N1-N4 atteint → **NO-GO** (arrêter, pivoter)

---

## 7. Recommandations de Kanban Tasks (Phase 3)

À créer après GO (ou GO conditionnel) :

### Si GO (Phase 3A — Construction produit)

| Task | Assignee proposé | Description |
|------|-----------------|-------------|
| **Implémenter webhooks Slack/Discord/Telegram/Email** | dev | P1 features attendues par le marché. Priorité après validation. |
| **Système de paiement (Stripe)** | fullstack-dev | Intégration Stripe + gestion abonnements + factures. |
| **Dashboard multi-projets** | fullstack-dev | Interface web pour gérer plusieurs forms, voir les submissions. |
| **File upload S3/Backblaze** | dev | Feature payante chez tous les concurrents. Upsell. |
| **Landing page finale (production)** | designer | LP définitive basée sur la variante A/B gagnante. |

### Si GO conditionnel (Phase 3B — MVP launch)

| Task | Assignee proposé | Description |
|------|-----------------|-------------|
| **Déploiement production + monitoring** | devops | Infrastructure stable pour les premiers clients payants. |
| **Anti-spam v2 (ML scoring)** | ml-dev | Au-delà du Turnstile, scoring comportemental ML. |
| **Page de documentation API** | tech-writer | Docs complètes pour l'intégration développeur. |
| **Support client setup** | growth | Email support, FAQ, knowledge base. |

### Si Itérer (Phase 3C — Repositionnement)

| Task | Assignee proposé | Description |
|------|-----------------|-------------|
| **A/B test du pricing** | growth | Tester un one-time à 29€ (comme Formspark), ou un free tier plus généreux. |
| **Interview 10 non-convertis** | researcher | Comprendre pourquoi les visiteurs n'ont pas signup. |
| **Pivoter le positionnement** | strategist | Changer le message produit selon les retours HN/Reddit. |

---

## 8. Risques et Mitigations

| Risque | Probabilité | Impact | Mitigation |
|--------|:-----------:|:------:|------------|
| Anti-spam MVP insuffisant (devs HN impitoyables) | Moyenne | Critique | Tester avec des formulaires publics 48h avant Show HN. Avoir un plan B (désactiver le scoring si bug). |
| Docker one-liner cassé sur ARM64 | Faible | Critique | Tester sur Hetzner CX22 (ARM64) avant le lancement. Pas de "marche sur ma machine". |
| Pas assez de temps (alternance 5h/semaine) | Haute | Élevé | Prioriser P0 uniquement. Sacrifier P1/P2 si nécessaire. Le produit doit être prêt pour HN, pas parfait. |
| HN ignore le post (< 20 points) | Moyenne | Élevé | Préparer 2 semaines d'engagement HN avant. Soigner le titre. Timing optimal. Plan B : Reddit uniquement. |
| Landing page A/B pas concluante | Faible | Faible | Les 2 variantes sont assez proches. L'important est d'avoir UNE landing page qui convertit, pas de savoir laquelle gagne. |
| Budget > 40€ | Faible | Faible | Tout est gratuit ou presque (Carrd $9/mois, domaine $10/an, VPS $3/mois). |

---

## 9. Verdict Final

> *Cette section sera remplie à J30 après application des critères go/no-go.*

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

**Prochaines étapes :** (créer les Kanban tasks recommandés section 7)

---

## 10. Prochains Kanban Tasks Recommandés (À Créer)

### Immédiats (cette semaine)

| # | Titre | Assignee | Description |
|---|-------|----------|-------------|
| 1 | **Implémenter anti-spam MVP dans Form Backend API** | dev | Turnstile + rate limiting IP + scoring comportemental basique. Bloquant pour Show HN. |
| 2 | **Créer landing page A/B (Self-hosted vs Anti-spam)** | growth | 2 pages Carrd/Softr, analytics Plausible, capture email. |
| 3 | **Créer page SEO /formspree-alternative** | growth | Tableau comparatif + captures + CTA. Mise en ligne immédiate. |
| 4 | **Finaliser GitHub README + GIF démo** | dev | README complet, badges, docker-compose.yml, GIF de démonstration. |

### Semaine 2

| # | Titre | Assignee | Description |
|---|-------|----------|-------------|
| 5 | **Exécuter le lancement Show HN** | growth | Post Show HN mardi 16h Paris. Répondre à tous les commentaires. |
| 6 | **Exécuter le calendrier Reddit (6 posts)** | growth | Posts r/selfhosted, r/webdev, r/SideProject selon le planning. |
| 7 | **Outreach 30 devs prioritaires** | growth | DMs/emails aux commentateurs HN/Reddit identifiés. |

### Semaine 3-4

| # | Titre | Assignee | Description |
|---|-------|----------|-------------|
| 8 | **Compiler les données et appliquer go/no-go** | analyst | Analyse des métriques, décision structurée. |
| 9 | **Rédiger le verdict Phase 2** | analyst | Document final avec recommandation Phase 3. |

---

*Document généré par TARZ le 2026-05-09. Synthèse de 3 recherches : customer-discovery.md, channel-validation.md, prelaunch-validation-plan.md.*
