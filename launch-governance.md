# Launch Governance Rules

> Tenant : monetization-lab  
> Ces règles s'appliquent à tout le projet, sans exception.  
> Enfreindre une règle = rollback et revue.

---

## 1. No Paid Ads Without Human Approval

### Règle
**Aucune dépense publicitaire payante (ads) n'est autorisée sans approbation humaine explicite de Nassim.**

### Ce qui est couvert
- Google Ads, Facebook Ads, LinkedIn Ads, Twitter Ads
- Sponsoring de newsletter, podcasts, événements
- Influenceurs payants
- Promotions sponsorisées
- Tout achat de trafic

### Ce qui n'est PAS couvert
- Posts organiques sur Twitter, LinkedIn, Reddit
- Cold email manuel (personnalisé, pas automatisé)
- Participation à des communautés (gratuite)
- Content marketing (blog, SEO)
- Product Hunt (gratuit)
- Bouche-à-oreille

### Condition d'approbation
Avant d'autoriser les ads, Nassim doit valider que :
1. Le produit a un PMF prouvé (≥ 10 clients payants actifs, NPS ≥ 30, churn < 5%)
2. L'unité économique est positive (LTV > 3× CAC estimé)
3. Une campagne test est définie : budget, durée, métriques de succès, stop condition
4. Le tracking de conversion est opérationnel

### Budget Max (si approuvé)
- Phase test : €200 max, 2 semaines, 1 canal
- Post-validation : budget mensuel défini par Nassim, revu chaque mois

---

## 2. Financial Controls

### Stripe (Paiements)
- Aucune clé Stripe live (production) dans le repository
- Seules les clés de test sont autorisées en développement
- Les clés live sont injectées via variables d'environnement sur le serveur (fichier `.env.prod` jamais commité)
- Toute implémentation Stripe est faite dans une branche `payment/` isolée, mergée via PR par Nassim uniquement
- Backup DB obligatoire avant le premier webhook Stripe en production

### Seuils Financiers
- Revenu mensuel < €100 : tout traitement manuel (pas d'automatisation comptable)
- Revenu mensuel ≥ €100 : déclaration obligatoire (auto-entrepreneur ou freelance)
- Revenu mensuel ≥ €1k : consultation d'un expert-comptable
- Revenu mensuel ≥ €10k : structure juridique adaptée (SARL, SASU)

---

## 3. Security Gates

### Rate Limiting
- Tous les endpoints publics : rate limit via SlowAPI + Redis
- Endpoint magic link : max 1 requête / 60s par email
- Endpoint webhook Stripe : IP whitelist Stripe uniquement

### CORS
- En production : whitelist stricte (le domaine du produit uniquement)
- En développement : localhost:8000 autorisé

### Headers
```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Content-Security-Policy: default-src 'self'; script-src 'self'
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

### Données
- Aucune donnée utilisateur stockée en clair en production
- Aucun log contenant des PII (email, IP intégrale, nom)
- Backup DB automatique quotidien (scripts/backup-db.sh)
- Retention data : 24 mois max (purge automatique)

---

## 4. Deployment Gates

### Condition pour aller en production
1. [ ] Health endpoint fonctionnel (`GET /health` → `{"status":"ok"}`)
2. [ ] Rate limiting activé sur les endpoints publics
3. [ ] Backup DB automatisé
4. [ ] Monitoring : logs nginx + alerte erreurs 5xx
5. [ ] SSL Let's Encrypt actif
6. [ ] Domaine DNS configuré
7. [ ] `.env.prod` avec clés de production (exclu du repo)
8. [ ] Revue humaine de Nassim

### CI (quand ajouté)
- Aucune PR mergée sans revue humaine
- Tests unitaires sur les routes auth, webhook, pricing
- Lint Python (ruff) obligatoire
- Vérification sécurité : pas de clé API hardcodée, pas d'injection SQL

---

## 5. Data Retention & Privacy

### GDPR Compliance (même pour un petit projet)
- [ ] Privacy Policy accessible depuis toutes les pages (footer)
- [ ] Cookie consent banner (si analytics non-null)
- [ ] Droit à l'oubli : endpoint de suppression de compte + données
- [ ] Export des données utilisateur sur demande
- [ ] Registre des traitements : documenter quelles données sont stockées où et pourquoi

### Données stockées
| Type | Stockage | Retention | Justification |
|------|----------|-----------|---------------|
| Email | PostgreSQL | Jusqu'à suppression compte | Auth, facturation |
| Hash JWT refresh | Redis | 7 jours | Session management |
| Logs nginx | Disque | 90 jours rolling | Sécurité, monitoring |
| Événements analytics | Umami/PostHog | 24 mois | Analyse produit |
| Stripe customer ID | PostgreSQL | Jusqu'à suppression compte | Facturation Stripe |

---

## 6. Decision Log

| Date | Décision | Raison | Auteur |
|------|----------|--------|--------|
| — | — | — | — |

*Les décisions clés sont consignées ici de manière durable.*

---

Ce document évolue avec le projet. Toute modification est soumise à validation de Nassim.
