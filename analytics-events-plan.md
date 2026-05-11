# Analytics Events Plan — Template de Tracking

> Tenant : monetization-lab  
> Moteur : logs nginx + GoAccess (phase 1), Umami (phase 2)  
> Principe : tracker les actions qui mesurent le progrès vers les métriques clés, pas tout ce qui bouge.

---

## 1. Métriques Clés (North Star + Input Metrics)

| Métrique | Type | Définition |
|----------|------|------------|
| **MRR** | Output | Revenu mensuel récurrent (total des abonnements actifs) |
| **Nouveaux utilisateurs** | Input | Inscriptions complétées (email vérifié) |
| **Activation** | Input | % d'utilisateurs qui atteignent le moment "aha" (défini par produit) |
| **Rétention J7 / J30** | Input | % d'utilisateurs revenus après 7 / 30 jours |
| **Conversion free→paid** | Input | % de comptes gratuits devenant payants |
| **Churn mensuel** | Output | % d'abonnés qui annulent chaque mois |

---

## 2. Événements à Tracker

### Acquisition (avant login)

| Événement | Propriétés | Pourquoi |
|-----------|-----------|----------|
| `page_view` | url, referrer, utm_source, utm_medium, utm_campaign | Trafic |
| `landing_visit` | page, referrer type (organic, direct, referral, social) | Performance landing |
| `cta_click` | cta_text, page_section, button_position | Taux de clic par section |
| `pricing_view` | plan_viewed (starter/pro/enterprise) | Intention d'achat |
| `signup_start` | method (email / google / magic_link) | Funnel entrée |
| `signup_complete` | method, time_to_complete (s) | Funnel conversion |

### Activation (première session)

| Événement | Propriétés | Pourquoi |
|-----------|-----------|----------|
| `onboarding_step` | step_name, step_number, completed (bool), time_on_step | Funnel onboarding |
| `first_key_action` | action_name, time_since_signup | Activation ! |
| `value_seen` | feature_name, page | L'utilisateur a vu une feature clé |
| `help_needed` | page, help_topic, resolved (bool) | Frictions onboarding |

### Engagement (usage)

| Événement | Propriétés | Pourquoi |
|-----------|-----------|----------|
| `session_start` | source, device | Sessions quotidiennes |
| `feature_used` | feature_name, count, session_duration | Feature adoption |
| `api_call` | endpoint, response_time, status | Usage technique |
| `search_query` | query_text (anonymisé), results_count | Recherche interne |
| `export_action` | format (csv/pdf), item_count | Export / workflow |
| `invite_sent` | method (email / link), count | Viralité |
| `invite_accepted` | inviter_id, time_to_accept | Viralité |

### Monétisation

| Événement | Propriétés | Pourquoi |
|-----------|-----------|----------|
| `pricing_page_view` | previous_plan (si connu) | Intention |
| `checkout_start` | plan, price, coupon | Funnel checkout |
| `checkout_complete` | plan, price, coupon, payment_method | Revenu ! |
| `subscription_created` | plan, billing_cycle, trial_days | MRR |
| `subscription_canceled` | plan, reason (si fourni), days_active | Churn |
| `subscription_reactivated` | plan, days_gone | Win-back |
| `payment_failed` | attempt_number, amount | Churn risque |

### Rétention

| Événement | Propriétés | Pourquoi |
|-----------|-----------|----------|
| `return_visit` | days_since_last_visit | Rétention |
| `feature_reengagement` | feature_name, trigger (email / notification / manual) | Engagement |
| `notification_clicked` | type (email / push / in-app), campaign | Réengagement |
| `feedback_given` | type (nps / bug / feature_request), rating | Satisfaction |
| `support_ticket` | category, resolved_time, sentiment | Support load |

---

## 3. Propriétés Globales (sur tous les événements)

```json
{
  "distinct_id": "uuid",           // Identifiant utilisateur (pas email)
  "session_id": "uuid",            // Session courante
  "timestamp": "ISO8601",          // Serveur-side, pas client
  "url": "/pricing",
  "referrer": "https://google.com",
  "utm_source": "twitter",
  "utm_medium": "social",
  "utm_campaign": "launch-v1",
  "user_agent": "Mozilla/...",
  "screen_size": "1440x900",
  "country": "FR",                 // Geo-IP, pas user input
  "plan": "free",                  // Plan actuel (si connecté)
  "days_since_signup": 14
}
```

---

## 4. Implémentation Technique

### Phase 1 — Logs nginx uniquement (MVP)

```nginx
# Dans le bloc server
log_format monetization '$remote_addr - $remote_user [$time_local] '
    '"$request" $status $body_bytes_sent '
    '"$http_referer" "$http_user_agent" '
    '$request_time';

# GoAccess dashboard : analyse quotidienne
# Commande : goaccess /var/log/nginx/access.log -o /var/www/report.html --log-format=COMBINED
```

**Ce qu'on peut mesurer avec les logs nginx seuls :**
- Pages vues, visiteurs uniques, sessions (par IP)
- Sources de trafic (referrer, UTM dans l'URL)
- Taux de rebond, temps sur site (approximatif)
- Pages les plus visitées, chemins de navigation
- Codes HTTP, erreurs

**Ce qu'on ne peut PAS mesurer :**
- Événements utilisateur côté client (CTA clicks, signup complétion, feature usage)
- Métriques produit (activation, rétention, conversion)
- Parcours individuels (pas de user_id dans les logs)

### Phase 2 — Umami (après lancement)

```javascript
// Envoi manuel d'événements Umami (via API HTTP)
// Pas de SDK JS nécessaire — appel HTTP vers l'instance Umami

umami.track('signup_complete', {
  method: 'magic_link',
  time_to_complete: 45
});
```

**Propriétés Umami :** pas de propriétés custom en version gratuite → nommer les événements avec suffisamment d'info dans le nom (`pricing_starter_view`, `pricing_pro_view`)

### Phase 3 — Système dédié (post-MVP)

Quand le volume le justifie (≥ 1000 utilisateurs actifs ou ≥ €1k MRR) :
- **PostHog** : self-hosted, open source, events + funnels + retention
- Alternative : **Plausible** (plus simple, moins cher, moins de features)

---

## 5. Dashboard de Bord (GoAccess / Umami)

### Métriques quotidiennes à surveiller

```
┌────────────────────────────────────────────┐
│  Dashboard quotidien                       │
│                                            │
│  Visiteurs : 142  (+12% vs J-7)            │
│  Inscriptions : 8  (conversion 5.6%)       │
│  Pages/session : 3.2                       │
│  Temps moyen : 4m12s                       │
│  Top pages : /, /pricing, /features        │
│  Sources : direct 45%, organic 30%, X 15%  │
│  Erreurs 5xx : 0                           │
└────────────────────────────────────────────┘
```

---

## 6. Rules

- **Ne pas tracker les admins / nous-mêmes.** Filtrer par IP ou cookie.
- **Anonymiser les IPs** (dernier octet supprimé) pour conformité RGPD.
- **Pas d'event PII dans les propriétés** — jamais d'email, nom, adresse.
- **Consentement :** pas requis pour Umami (self-hosted, sans cookies). Requis si GA.
- **Revue trimestrielle :** supprimer les événements non utilisés depuis 6 mois.
