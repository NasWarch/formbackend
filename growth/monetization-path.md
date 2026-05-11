# Chemin de Monétisation — Form Backend API

> Mise à jour : 2026-05-09 — Adapté de Monitoring Serveur Léger vers Form Backend API
> Stack : Stripe Customer Portal (seule interface paiement) + Feature gating backend
> Pas de UI custom pour la gestion d'abonnement
> Taxes : Stripe Tax

---

## Plans Tarifaires (code)

| Plan | Prix | Soumissions/mois | Formulaires | Fonctionnalités clés |
|------|------|-----------------|-------------|----------------------|
| **Free** | **0 €** | 50 | 1 | Endpoint API, notifications email |
| **Starter** | **8 €/mois** | 500 | 5 | Email + anti-spam + webhooks + CORS |
| **Pro** | **19 €/mois** | 3 000 | Illimité | + Upload fichiers + CSV export + templates email + domaine personnalisé |
| **Scale** | — | 15 000 | Illimité | + API complète + support dédié |
| **Enterprise** | Sur devis | Illimité | Illimité | SLA, SSO, support dédié |

> Source : `app/main.py` (ligne 430 : `limits = {"free": 50, "starter": 500, "pro": 3000, "scale": 15000, "business": 10000}`) et `app/templates/pricing.html` (tableau comparatif)

---

## Déclencheurs Free → Payant

Le passage du plan Free au plan Starter ne doit pas être forcé mais **naturellement incité** par la friction du Free.

### Déclencheurs automatiques (back-end)

| Déclencheur | Seuil Free | Action |
|-------------|-----------|--------|
| **Dépassement soumissions** | > 50 soumissions/mois | Blocage des nouvelles soumissions + message d'upgrade |
| **Limite formulaires** | > 1 formulaire | Blocage création nouveau formulaire + proposition Starter |
| **Anti-spam** | Non disponible en Free | Message "Activer l'anti-spam → passer au plan Starter" |
| **Webhooks** | Non disponible en Free | Feature masquée + badge "Starter" |
| **Upload de fichiers** | Non disponible en Free | Badge "Pro" dans l'interface |
| **Domaine personnalisé** | Non disponible en Free | Badge "Pro" |

### Déclencheurs temporels (front-end)

- **J+7** : Banner subtil "Vous avez reçu {N} soumissions. Passez à Starter pour 500 soumissions/mois à 8€."
- **J+14** : Notification email "Vous utilisez notre service depuis 2 semaines ! Le plan Pro (19€/mois) débloque les uploads de fichiers et les webhooks."
- **J+30** : Bannière plus visible + comparaison côte à côte
- **À chaque blocage de soumission** : "Cette soumission a été bloquée car vous avez atteint votre limite de 50/mois. Passez à Starter pour continuer à collecter."

### Déclencheurs contextuels (in-app)

| Page | Message |
|------|---------|
| Dashboard | "Soumissions 50/50 utilisées ce mois. Passez à Starter pour 500 soumissions." |
| Création de formulaire | "1/1 formulaires utilisés. Passez à Starter pour 5 formulaires." |
| Paramètres formulaire | "Webhooks disponibles sur le plan Starter et supérieur." |
| Upload de fichier | "Upload de fichiers disponible sur le plan Pro." |
| Export CSV | "Export CSV disponible sur le plan Pro et supérieur." |
| Code d'intégration | "Domaine personnalisé disponible sur le plan Pro." |

### Design des messages upgrade

Les messages doivent être informatifs, pas agressifs. Style :

> **"Vous avez utilisé 50 soumissions sur 50 ce mois-ci."**
> Pour continuer à recevoir des soumissions, passez au plan Starter (8€/mois — 500 soumissions, anti-spam, webhooks).
> [Voir les plans →] (lien vers Stripe Customer Portal)

Pas de popup modale bloquante, pas de compteur intrusif. Un dev qui se sent forcé partira.

---

## Stripe Customer Portal — Seule Interface de Paiement

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                       Produit (FastAPI)                         │
│                                                                 │
│  [Upgrade to Starter] → redirect to Stripe Customer Portal      │
│  [Manage Subscription] → redirect to Stripe Customer Portal     │
│                                                                 │
│  Feature gating backend : check plan via Subscription table     │
│  Usage tracking via Form.submission_count                       │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                  Stripe Customer Portal                         │
│  (Stripe héberge toute l'interface : paiement, changement plan, │
│   annulation, factures, infos carte)                            │
│                                                                 │
│  Langue : français (paramétré dans Stripe)                      │
│  Marque : logo + couleurs du produit (customisation portal)     │
└─────────────────────────────────────────────────────────────────┘
```

### Implémentation (à faire dans branche `payment/`)

```python
# FastAPI — Créer Stripe Checkout Session (paiement)
@app.post("/api/billing/create-checkout")
async def create_checkout(user_id: str, price_id: str):
    session = stripe.checkout.Session.create(
        customer=customer.stripe_id,
        mode="subscription",
        line_items=[{"price": price_id, "quantity": 1}],
        success_url="https://formapi.example.com/billing/success",
        cancel_url="https://formapi.example.com/billing/cancel",
    )
    return {"url": session.url}

# FastAPI — Créer Stripe Customer Portal (gestion abonnement)
@app.post("/api/billing/portal")
async def billing_portal(user_id: str):
    session = stripe.billing_portal.Configuration.create(
        customer=customer.stripe_id,
        return_url="https://formapi.example.com/settings/billing",
    )
    return {"url": session.url}
```

**Important :** L'URL du portal doit être la même que le `return_url`. L'utilisateur clique "Retour au site" et revient à la gestion du compte.

### Points clés

- **Pas de form de carte dans l'application** — tout se passe sur Stripe.com
- **Pas de gestion d'abonnement custom** — annulation, changement de plan, mise à jour CB : Stripe gère
- **Stripe Customer Portal est déjà prêt** — 30 min de config dans le dashboard Stripe
- **Configuration Stripe Portal** : activer "Update subscription", "Cancel subscription", "View invoices", "Update payment method"
- **Mettre le logo et la marque** dans Stripe Branding pour une expérience cohérente

---

## Feature Gating Backend

### Principe

Le gating se fait côté backend via la table `Subscription` + `Plan`. Le frontend affiche ce que le backend autorise.

### Modèle de données (déjà en place)

```python
# Voir app/models/subscription.py
class Plan(Base):
    id: UUID
    name: str           # "Free", "Starter", "Pro", "Scale"
    slug: str           # "free", "starter", "pro", "scale"
    price_cents: int    # 0, 800, 1900, ...
    features: str       # JSON list: ["50_submissions", "1_form", ...]
    is_active: bool

class Subscription(Base):
    user_id: UUID
    plan_id: UUID
    status: SubscriptionStatus  # active | canceled | past_due | trialing
    stripe_subscription_id: str
```

### Règles de gating

```python
class FeatureGate:
    @staticmethod
    def max_submissions(plan_slug: str) -> int:
        limits = {
            "free": 50,
            "starter": 500,
            "pro": 3000,
            "scale": 15000,
            "enterprise": 999999,
        }
        return limits.get(plan_slug, 50)

    @staticmethod
    def max_forms(plan_slug: str) -> int:
        limits = {
            "free": 1,
            "starter": 5,
            "pro": 999,    # illimité en pratique
            "scale": 999,
            "enterprise": 9999,
        }
        return limits.get(plan_slug, 1)

    @staticmethod
    def has_feature(plan_slug: str, feature: str) -> bool:
        features_by_plan = {
            "free": ["50_submissions", "1_form", "basic_endpoint", "email_notifications"],
            "starter": ["500_submissions", "5_forms", "basic_endpoint", "email_notifications",
                        "spam_filtering", "webhooks", "cors"],
            "pro": ["3000_submissions", "unlimited_forms", "basic_endpoint", "email_notifications",
                    "spam_filtering", "webhooks", "cors", "file_uploads", "csv_export",
                    "email_templates", "custom_domain", "priority_support"],
            "scale": ["15000_submissions", "unlimited_forms", "basic_endpoint", "email_notifications",
                      "spam_filtering", "webhooks", "cors", "file_uploads", "csv_export",
                      "email_templates", "custom_domain", "priority_support", "api_access",
                      "dedicated_support"],
        }
        return feature in features_by_plan.get(plan_slug, [])

    @staticmethod
    def data_retention_days(plan_slug: str) -> int:
        return {"free": 30, "starter": 90, "pro": 365, "scale": 730}.get(plan_slug, 30)
```

### Cas d'usage : dépassement de limite de soumissions

```python
# Réception d'une soumission
@app.post("/api/f/{endpoint}")
async def receive_submission(endpoint: str, request: Request):
    form = await db.get_form_by_endpoint(endpoint)
    user = await db.get_user(form.user_id)
    sub = await db.get_subscription(user.id)
    plan_slug = sub.plan.slug if sub and sub.plan else "free"

    max_subs = FeatureGate.max_submissions(plan_slug)
    current = form.submission_count

    if current >= max_subs:
        return JSONResponse(
            status_code=403,
            content={
                "error": "submission_limit_reached",
                "message": f"Limite de {max_subs} soumissions/mois atteinte.",
                "upgrade_url": generate_stripe_checkout_url(user, "starter"),
                "current_plan": plan_slug,
                "max_allowed": max_subs,
                "current_count": current,
            },
        )

    # ... accepter la soumission
```

### Résiliation — Gestion des données

Quand un utilisateur résilie son abonnement (via Stripe Portal) :

1. **Plan repasse en Free** immédiatement (webhook `customer.subscription.deleted`)
2. **Tous ses formulaires restent en place** (read-only — pas de perte)
3. **Les soumissions continuent dans la limite Free** (50/mois)
4. **1 seul formulaire reste actif** ; les formulaires supplémentaires sont désactivés avec message "Réactive ton abonnement pour réactiver ce formulaire"
5. **Les fonctionnalités Pro** (webhooks, anti-spam, upload fichiers) sont désactivées
6. **Données historiques conservées** 30 jours après résiliation, puis purge

Cette approche "soft downgrade" est cruciale : un utilisateur insatisfait aujourd'hui peut revenir demain sans perdre sa configuration.

---

## Période d'Essai Recommandée

### Approche choisie : Freemium perpétuel (pas de trial limité dans le temps)

**Pourquoi pas de trial 14 jours classique :**

| Approche | Avantages | Inconvénients |
|----------|-----------|---------------|
| Trial 14 jours Starter | Démontre la valeur complète | Pression temporelle — les devs détestent ça |
| Freemium perpétuel (limité) | Pas de stress, l'utilisateur découvre à son rythme | Convertit plus lentement |
| **Mix recommandé** | **Freemium perpétuel + 50 soumissions** | **Si besoin > 50 soumissions = besoin réel → conversion naturelle** |

Pour un outil dev, le freemium perpétuel est plus efficace qu'un trial :
- Un développeur prend son temps avant de payer (parfois 30-90 jours)
- Le trial crée de l'anxiété ("je perds mes données dans 14 jours")
- La friction naturelle du Free (50 soumissions, 1 formulaire) est un meilleur déclencheur qu'un timer

### Si trial nécessaire (phase 2 — A/B test)

| Paramètre | Valeur |
|-----------|--------|
| Durée | 14 jours |
| Features | Starter complètes (500 soumissions, 5 formulaires, anti-spam, webhooks) |
| Carte bancaire | Non demandée pendant le trial |
| Conversion après trial | Restriction aux 50 soumissions / 1 formulaire sans perte de données |
| Reminder | Email J7, J12, J14 |

---

## Gestion des Taxes — Stripe Tax

### Pourquoi Stripe Tax

- **Automatisation totale** : Stripe calcule la TVA applicable selon le pays du client
- **RGPD + taxes UE** : Pour les clients français et européens, Stripe applique la TVA du pays du client (règles MOSS/TVA UE sur services numériques)
- **Pas de déclaration manuelle** : Stripe génère les rapports de TVA pour chaque trimestre
- **Coût** : 0,50 € par transaction (en plus des fees standard)

### Configuration

```python
# Activer Stripe Tax dans le dashboard Stripe
# Tax settings → Enable Stripe Tax

# Dans le checkout :
session = stripe.checkout.Session.create(
    customer=customer.stripe_id,
    mode="subscription",
    line_items=[{"price": price_id, "quantity": 1, "tax_rates": ["txr_xxx"]}],
    automatic_tax={"enabled": True},  # ← Clé : activer la taxe auto
    # ... reste de la config
)
```

### Règles de taxation par pays

| Localisation client | TVA applicable | Notes |
|--------------------|---------------|-------|
| France | 20% | Taux standard biens numériques |
| UE (hors France) | TVA du pays client | Taux variables (19% Allemagne, 21% Espagne, 22% Pays-Bas...) |
| Hors UE | 0% | Reverse charge — le client déclare lui-même |
| Entreprises UE (TVA intracomm.) | 0% | Si le client fournit un numéro de TVA valide |

Stripe Tax gère tout ça automatiquement. Il suffit d'activer `automatic_tax`.

### Seuils de déclaration

- **France** : Déclaration mensuelle ou trimestrielle selon le volume
- **UE (MOSS)** : Déclaration trimestrielle si CA < 10 000 €/an dans le pays
- Avec Stripe Tax : export CSV des montants collectés par pays → prêt pour le formulaire MOSS

### Recommandation

| Action | Priorité | Délai |
|--------|----------|-------|
| Activer Stripe Tax dans le dashboard | Haute | Avant le 1er paiement |
| Configurer les taux par pays | Haute | Pendant le setup |
| Vérifier le paramétrage TVA France 20% | Haute | Pendant le setup |
| Déclaration MOSS trimestrielle | Moyenne | 1 mois après 1er paiement |

---

## Opérations de Paiement Quotidiennes

### Ce que Stripe gère (automatique)

- Débit mensuel des cartes
- Relances en cas d'échec (Stripe Smart Retries)
- Mise à jour des cartes expirées (Stripe Account Updater)
- Factures PDF générées automatiquement
- Email de reçu (personnalisé avec marque)
- Annulation d'abonnement
- Remboursement (depuis le dashboard Stripe)

### Ce qu'il reste à faire (manuellement)

| Action | Fréquence | Temps |
|--------|-----------|-------|
| Vérifier les impayés (past_due) | 1x/semaine | 2 min |
| Répondre aux emails de support billing | Au besoin | 5 min |
| Export CSV pour déclaration TVA | 1x/trimestre | 10 min |
| Revue MRR + churn + taux conversion post-blocage | 1x/mois | 5 min |

---

## Résumé

| Composant | Stack | Complexité |
|-----------|-------|-----------|
| Paiement | Stripe Checkout Sessions | 1 jour |
| Gestion abonnement | Stripe Customer Portal | 0,5 jour |
| Feature gating | Backend Python (Plan + Subscription) | 0,5 jour |
| Synchronisation webhook | FastAPI endpoint | 0,5 jour |
| Tracking usage (Form.submission_count) | DB PostgreSQL (déjà en place) | 0 jour |
| Limitation backend (blocage soumissions) | FastAPI middleware | 1 jour |
| Taxes | Stripe Tax (activation) | 1 heure |
| **Total monétisation** | | **~3,5 jours** |
