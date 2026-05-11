# Pricing Test Plan — Template

> Tenant : monetization-lab  
> Statut : **document de conception uniquement** — aucune implémentation Stripe avant validation humaine.  
> Voir launch-governance.md pour les gates de sécurité.

---

## 1. Principes de Pricing

- **Prix basé sur la valeur** (le coût du problème résolu pour le client) — pas sur le coût de revient
- **3 plans max** (trop de choix = paralysie)
- **Plan gratuit** seulement si l'activation (time-to-value) est rapide ET que le gratuit sert de funnel payant
- **Devise : EUR uniquement**
- **Annoncé en TTC** (TVA incluse) pour le marché français / européen

---

## 2. Structure de Plans (Exemple)

| | Starter | Pro | Enterprise |
|---|---|---|---|
| **Prix** | €9/mo | €29/mo | €99/mo |
| **Cible** | Indépendants, petits projets | Équipes, professionnels | Entreprises |
| **Limite** | 3 projets | 15 projets | Illimité |
| **Features** | Fonctionnalités de base | Starter + analytics, exports avancés | Pro + API, support prioritaire, SSO |
| **Support** | Email (48h) | Chat (24h) | Prioritaire (4h) |
| **Essai** | 14 jours gratuits | 14 jours gratuits | Sur demande |

**À adapter selon le produit réel** — cette structure est un point de départ.

---

## 3. Expériences de Pricing

### Pré-lancement

#### Test 1 : Van Westendorp (sensibilité au prix)

**Méthode :** sondage auprès de 50+ personnes du persona cible.

Questions :
- À quel prix ce produit vous semblerait-il **trop cher** pour l'acheter ?
- À quel prix semblerait-il **si bon marché** que vous douteriez de sa qualité ?
- À quel prix semblerait-il **un peu cher mais acceptable** ?
- À quel prix semblerait-il **une bonne affaire** ?

**Résultat :** gamme de prix psychologiquement acceptable → positionner le plan Pro dans cette fourchette.

#### Test 2 : Comparaison concurrentielle

- [ ] Lister 3 concurrents directs
- [ ] Noter leur prix, feature set, et positionnement
- [ ] Positionner ton produit par rapport à eux (plus cher, moins cher, équivalent ?)
- [ ] Justifier le delta : « On coûte 2x moins cher parce que… » ou « On coûte 2x plus cher parce que… »

### Post-lancement

#### Test 3 : A/B Pricing (3 cohortes)

> Nécessite ≥ 1000 visiteurs/semaine sur la page pricing.

| Cohorte | Prix Starter | Prix Pro | Prix Enterprise |
|---------|-------------|----------|----------------|
| A (contrôle) | €9 | €29 | €99 |
| B (premium) | €14 | €39 | €149 |
| C (low-cost) | €5 | €19 | €59 |

**Métriques :** conversion rate, MRR par visiteur, LTV projeté.

**Durée :** 2 semaines minimum.

#### Test 4 : Feature Gating

**Hypothèse :** « Le plan gratuit convertit mieux si une feature clé est limitée. »

- [ ] Semaine 1-2 : gratuit illimité (sauf limite de projets)
- [ ] Semaine 3-4 : gratuit avec feature X désactivée (X = feature la plus distinctive du plan Pro)
- [ ] Comparer le taux de conversion gratuit → payant entre les deux périodes

---

## 4. Métriques Pricing

| Métrique | Définition | Cible |
|----------|-----------|-------|
| **CVR free → paid** | % d'utilisateurs gratuits passant payants | ≥ 3-5% (médiane SaaS) |
| **MRR moyen par client** | Revenu total / clients payants | Variable selon pricing |
| **Taux de churn** | % d'abonnés annulant par mois | < 5% (B2B SaaS) |
| **Perte de client à la facturation** | % d'échecs de paiement récupérés | < 10% |
| **NPS par plan** | Satisfaction par niveau de prix | Starter ≥ 20, Pro ≥ 30, Enterprise ≥ 40 |
| **Délai avant upgrade** | Jours entre signup et premier paiement | < 30 jours |
| **Délai avant downgrade** | Jours entre signup et annulation | > 90 jours (bon signe) |

---

## 5. Objections Pricing Courantes (FAQ)

| Objection | Réponse |
|-----------|---------|
| « C'est trop cher » | Comparer au coût du problème (temps passé × taux horaire) |
| « Je peux le faire moi-même gratuitement » | « Combien de temps te prends cette tâche par semaine ? Multiplie par 4 semaines. » |
| « Le concurrent X est moins cher » | Lister les features que X n'a pas. Si features similaires, justifier le premium. |
| « Pas de budget » | « On a un plan gratuit / pas de CB requise pour l'essai » |
| « Je veux l'essayer d'abord » | Essai gratuit 14 jours, pas de CB |

---

## 6. Rules de Pricing

1. **Pas de promo "à vie" sans date limite** — « -50% à vie pour les 50 premiers » seulement.
2. **Prix annoncé = prix sur la carte** — pas de frais cachés (frais de mise en service, setup fees, etc.)
3. **Prix affichés en TTC** (TVA incluse) pour l'Europe. Stripe calcule la TVA automatiquement.
4. **Pas de discount "sur demande" en moyenne** — crée de l'inégalité et de l'insatisfaction.
5. **Pas de plan "Gratuit" sans limite claire** — 3 projets max, pas de exports, etc.
6. **Toute modification de prix notifiée 30 jours avant** par email.
7. **Grandfathering :** les clients existants gardent leur prix (pas d'augmentation rétroactive).

---

> **Rappel :** document de conception uniquement. Aucun code Stripe écrit sans validation humaine.
