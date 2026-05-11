# Scoring & Sélection des Opportunités Business

> Analyse produite le 7 mai 2026
> Contexte : VPS ARM64 4GB RAM, stack FastAPI + HTMX + PostgreSQL + Redis
> Méthode : 6 dimensions notées de 1 (faible) à 5 (excellent)

---

## Grille de scoring

| # | Opportunité | Urgence | Volonté payer | Concurrence | Faisabilité | Time-to-revenue | Risque légal | **Total /30** | Décision |
|---|---|---|---|---|---|---|---|---|---|
| 6 | **Monitoring Serveur Léger** | 4 | 4 | 4 | 5 | 5 | 5 | **27** | **GO** |
| 3 | **Time Tracking** | 4 | 4 | 3 | 5 | 5 | 5 | **26** | **GO** |
| 5 | **CRM Simple** | 4 | 5 | 3 | 5 | 4 | 4 | **25** | **GO** |
| 1 | **Facture & Devis Simple** | 5 | 5 | 3 | 4 | 4 | 3 | **24** | **GO** |
| 8 | **Gestion Projet Simplifiée** | 4 | 4 | 2 | 4 | 3 | 5 | **22** | CONDITIONNEL |
| 2 | **Booking & Planning** | 4 | 4 | 3 | 3 | 3 | 4 | **21** | CONDITIONNEL |
| 4 | **Newsletter/Mailing** | 4 | 4 | 3 | 3 | 4 | 3 | **21** | CONDITIONNEL |
| 7 | **Gestion de Stock** | 3 | 3 | 4 | 4 | 2 | 4 | **20** | CONDITIONNEL |

---

## Détail des scores par opportunité

### 1. Facture & Devis Simple — 24/30 — GO

| Dimension | Score | Justification |
|---|---|---|
| Urgence | 5/5 | Réforme e-invoicing obligatoire en 2026 — trigger temporel fort, deadline légale identifiée |
| Volonté de payer | 5/5 | Marché mature : 8 concurrents tous payants de 7,90 à 13,90 €/mois. Aucun doute |
| Concurrence | 3/5 | Très concurrentiel (8 acteurs listés), mais opportunité de pricing agressif à 3,99€. Marché croît de 20%/an. Positionnable |
| Faisabilité technique | 4/5 | PDF, conformité fiscale, mentions obligatoires — faisable en 3-4 semaines. La conformité fiscale française demande de l'attention |
| Time-to-revenue | 4/5 | Freemium rapide, mais certification PDP partenaire pour e-invoicing pourrait prendre du temps |
| Risque légal | 3/5 | Conformité TVA française, mentions légales obligatoires, certification PDP incertaine. Risque le plus élevé du lot |

**Décision : GO** — la réforme 2026 est un trigger unique. À builder avec un cabinet comptable partenaire pour la conformité.

---

### 2. Booking & Planning — 21/30 — CONDITIONNEL

| Dimension | Score | Justification |
|---|---|---|
| Urgence | 4/5 | Croissance post-COVID des RDV en ligne, mais pas de trigger réglementaire urgent |
| Volonté de payer | 4/5 | Calendly, SimplyBook, Wogga — tous payants. Marché validé |
| Concurrence | 3/5 | Fragmente mais Calendly domine le haut du marché. Pas de leader TPE bien-être en France |
| Faisabilité technique | 3/5 | Fuseaux horaires, disponibilités récurrentes, conflits, sync calendrier, SMS — complexité moyenne, 4-5 semaines |
| Time-to-revenue | 3/5 | Conversion freemium → payant plus lente sur ce segment. Décision d'achat réfléchie |
| Risque légal | 4/5 | RGPD standard, données de calendrier sans sensibilité particulière |

**Décision : CONDITIONNEL** — bon marché mais effort technique 4-5 semaines. À faire si Monitoring et Time Tracking échouent.

---

### 3. Time Tracking — 26/30 — GO

| Dimension | Score | Justification |
|---|---|---|
| Urgence | 4/5 | Freelance en France +12% en 2023-2024. Tendance forte, pas de trigger urgent |
| Volonté de payer | 4/5 | Toggl (9€), Clockify (3.99€), Harvest (~11€) — freelance paie déjà. Interstice à 4.99€ |
| Concurrence | 3/5 | Concurrentiel. Clockify Free 5 users est fort. Mais positionnement "entre Free et Toggl" tient |
| Faisabilité technique | 5/5 | Le + simple techniquement. Timer CRUD + rapports PDF. 2-3 semaines. Stack parfait |
| Time-to-revenue | 5/5 | Le plus rapide. MVP minimal en 2 semaines, freemium → solo 4.99€, conversion naturelle |
| Risque légal | 5/5 | Aucun. Pas de données sensibles. RGPD standard uniquement |

**Décision : GO** — meilleur quick-win technique avec le meilleur ratio effort/revenu potentiel.

---

### 4. Newsletter/Mailing — 21/30 — CONDITIONNEL

| Dimension | Score | Justification |
|---|---|---|
| Urgence | 4/5 | Exode Mailchimp en France, associations non adressées. Bon timing |
| Volonté de payer | 4/5 | MailerLite, Brevo, Mailchimp — tous payants. Marché validé |
| Concurrence | 3/5 | MailerLite à $9/mo 500 subs est solide. Brevo est cher. Niche existe |
| Faisabilité technique | 3/5 | Délivrabilité email = problème difficile (SPF/DKIM/DMARC, IP warmup, réputation). 4-6 semaines |
| Time-to-revenue | 4/5 | Prix fixe 5€/mois attractif. Conversion possible rapidement |
| Risque légal | 3/5 | RGPD, anti-spam, gestion des bounces et désabonnements. Risque réputationnel à l'échelle |

**Décision : CONDITIONNEL** — la délivrabilité est un métier. Nécessite un SMTP relay (AWS SES) ou investissement IP.

---

### 5. CRM Simple — 25/30 — GO

| Dimension | Score | Justification |
|---|---|---|
| Urgence | 4/5 | Sous-pénétration massive (12% d'adoption CRM chez TPE <10 salariés). Bon timing |
| Volonté de payer | 5/5 | HubSpot $20/mo, Pipedrive $14/seat, Zoho 14€ — catégorie où on paie. Très fort |
| Concurrence | 3/5 | Concurrentiel mais segment TPE 1-5 pers. mal adressé. HubSpot/Pipedrive trop chers. Gap à 6€ |
| Faisabilité technique | 5/5 | CRUD contacts + tags + pipelines simple. 3-4 semaines. Le + simple après Time Tracking |
| Time-to-revenue | 4/5 | Proposition de valeur claire, conversion rapide via freemium 50 contacts |
| Risque légal | 4/5 | RGPD standard sur données de contact. Risque acceptable |

**Décision : GO** — très gros marché (300M€ FR), sous-pénétration, faisable rapidement.

---

### 6. Monitoring Serveur Léger — 27/30 — GO (SÉLECTIONNÉE)

| Dimension | Score | Justification |
|---|---|---|
| Urgence | 4/5 | Explosion du self-hosting et VPS. Complexité des outils OSS existants (Nagios, Zabbix) repousse les petits porteurs |
| Volonté de payer | 4/5 | UptimeRobot (2M+ users), Better Stack (150k+ équipes). Les devs paient pour ça |
| Concurrence | 4/5 | Moins concurrentiel que SaaS généraliste. UptimeRobot $7, HetrixTools $5, Better Stack $30. Gap à 5.99€ |
| Faisabilité technique | 5/5 | HTTP/ping/TCP checks en Python/httpx/asyncio — trivial. 2-3 semaines. ARM64-friendly (< 50MB RAM) |
| Time-to-revenue | 5/5 | Les devs s'inscrivent vite. Freemium 3 monitors → Pro 5.99€. Premier mois possible |
| Risque légal | 5/5 | Aucune donnée utilisateur sensible. Aucune régulation sectorielle. Aucun PII |

**Décision : GO — SÉLECTIONNÉE** — meilleur score global. Niche peu concurrentielle, parfaite pour le stack, temps de build minimal, risque légal nul.

---

### 7. Gestion de Stock — 20/30 — CONDITIONNEL

| Dimension | Score | Justification |
|---|---|---|
| Urgence | 3/5 | Digitalisation lente des commerces de proximité. Pas de trigger urgent |
| Volonté de payer | 3/5 | Faible — Excel, papier ou rien. Zoho Inventory gratuit. Prouver la WTP sera long |
| Concurrence | 4/5 | Peu de concurrence sur micro-TPE <3 pers. Zoho limité, Odoo trop complexe |
| Faisabilité technique | 4/5 | CRUD stock + alertes. Barcode API. 4-5 semaines. Le défi est mobile UX |
| Time-to-revenue | 2/5 | Long — commerçants difficiles à convertir en ligne, cycle de vente long, besoin de mobile |
| Risque légal | 4/5 | Données de stock, pas de sensibilité particulière |

**Décision : CONDITIONNEL** — bonne niche mais le plus long time-to-revenue. À garder pour Phase 3.

---

### 8. Gestion de Projet Simplifiée — 22/30 — CONDITIONNEL

| Dimension | Score | Justification |
|---|---|---|
| Urgence | 4/5 | Trello restreint son plan gratuit, Notion/Asana chers. Timing OK |
| Volonté de payer | 4/5 | Trello, Asana, Notion — tous payants. Catégorie établie |
| Concurrence | 2/5 | Très concurrentiel. Trello (90M users), Asana, Notion, ClickUp, Monday. Différenciation difficile |
| Faisabilité technique | 4/5 | Boards/cartes/listes standard. Drag-drop avec sortable.js. 3-4 semaines |
| Time-to-revenue | 3/5 | Conversion lente — beaucoup d'alternatives gratuites ou freemium généreuses |
| Risque légal | 5/5 | Aucun — données projet standards |

**Décision : CONDITIONNEL** — trop concurrentiel pour un premier projet. L'idée du pricing fixe par équipe est bonne mais ne suffit pas face à Trello Free.

---

## Synthèse des décisions

### GO (priorité immédiate)

1. **Monitoring Serveur Léger** (27/30) ← RECOMMANDÉ
2. **Time Tracking** (26/30)
3. **CRM Simple** (25/30)
4. **Facture & Devis Simple** (24/30)

### CONDITIONNEL (à réévaluer après Phase 1)

5. Gestion de Projet Simplifiée (22/30)
6. Booking & Planning (21/30)
7. Newsletter/Mailing (21/30)
8. Gestion de Stock (20/30)

---

## Analyse des écarts avec la checklist qualité

### Check 1. Market evidence
- Toutes les opportunités ont des sources nommées, datées, vérifiables
- URLs fournies et accessibles
- Sources diversifiées (INSEE, Gartner, Statista, Grand View Research, Fortune BI)
- **PASS** — documentation complète et vérifiable

### Check 3. Monetization assumptions
- Pricing benchmarké contre 3-8 concurrents par opportunité
- Unit economics estimées mais sans CAC/LTV formel (acceptable au stade scoring)
- **PASS** avec réserve sur le calcul CAC (non disponible sans campagne marketing)

### Check 4. MVP scope & build realism
- Délais MVP estimés (2-6 semaines)
- Stack compatible
- **PASS**

### Check 10. Confidence scoring
- Niveau de confiance global : **MEDIUM-HIGH**
- Les 4 GO ont des preuves de marché solides, pricing benchmarké, faisabilité démontrée
- Faiblesse : pas de validation client directe (pas de conversations clients menées)

---

## Conclusion

**Sélection : Monitoring Serveur Léger (27/30)**

Raison du choix :
1. **Meilleur score global** — domine dans les dimensions les plus critiques (faisabilité, time-to-revenue, risque)
2. **Créneau non saturé** — les alternatives OSS sont complexes, les SaaS sont chers à l'échelle
3. **Zero risque légal** — pas de PII, pas de régulation, pas de conformité
4. **Perfect fit stack** — Python asyncio + httpx = 50MB RAM max
5. **Dogfood direct** — Nassim peut monitorer son propre VPS dès le J1
6. **Time-to-revenue le plus rapide** des 4 GO avec le Monitoring
7. **Concurrence modérée** (score 4/5) — le moins concurrentiel des 4 GO
