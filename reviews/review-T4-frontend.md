# Review — Frontend (T4) : Templates Jinja2

Date de revue : 2026-05-07
Reviewer : TARZ (agent review)
Document source : /root/monetization-lab/backend/app/templates/

---

## Résumé

| Dimension | Score | Commentaire court |
|-----------|-------|-------------------|
| A — Design & UX | 🟢 | Dark theme cohérent, responsive mobile-first, typographie soignée (Inter + JetBrains Mono). |
| B — HTMX & Interactivité | 🟢 | Progressive enhancement, pas de JS lourd. Magic link, dashboard, pricing tout HTMX. |
| C — Contenu & Marquage | 🟡 | 6 templates : base, index, login, dashboard, pricing, docs. Bien mais sans page statut. |
| D — Performance & Assets | 🟢 | HTMX local, CSS inline (~560 lignes), favicon SVG. Google Fonts externe (seul point). |
| E — Adéquation produit | 🔴 | **Même problème que le backend : templates parlent de monitoring serveur mais servent des formulaires.** |

---

## Détail par critère

### A — Design & UX

| # | Critère | Résultat | Justification | Confiance |
|---|---------|----------|---------------|-----------|
| A1 | Dark theme cohérent | 🟢 | Palette sombre homogène (bg #0a0c10, cards #1e1e2e, accents indigo). Design system visible dans style.css. | HIGH |
| A2 | Responsive mobile-first | 🟢 | Navigation mobile avec hamburger menu. Grid layouts avec breakpoints. | HIGH |
| A3 | Typographie | 🟢 | Inter (corps) + JetBrains Mono (code). Google Fonts avec preconnect. | HIGH |
| A4 | Accessibilité | 🟡 | Labels sur inputs, contrastes corrects. Mais pas d'attributs aria explicites. | MED |
| A5 | État loading HTMX | 🟢 | htmx-indicator sur formulaire de login, spinner CSS. | HIGH |

### B — HTMX & Interactivité

| # | Critère | Résultat | Justification | Confiance |
|---|---------|----------|---------------|-----------|
| B1 | Magic link flow HTMX | 🟢 | POST /auth/magic-link → swap dans #magic-result. Pas de rechargement de page. | HIGH |
| B2 | Dashboard dynamique | 🟢 | Liste des forms via HTMX get, création via POST, suppression avec confirmation. | HIGH |
| B3 | Embed modal | 🟢 | Affichage modal avec copie dans le presse-papier. | HIGH |
| B4 | Usage stats live | 🟢 | /api/usage endpoint HTMX pour barres de progression. | HIGH |
| B5 | Pas de JavaScript vanilla (sauf clipboard) | 🟢 | Toute l'interactivité repose sur HTMX. Clipboard API uniquement pour "Copier". | HIGH |

### C — Contenu & Marquage

| # | Critère | Résultat | Justification | Confiance |
|---|---------|----------|---------------|-----------|
| C1 | Nombre de templates | 🟢 | 6 templates fonctionnels : base, index, login, dashboard, pricing, docs. | HIGH |
| C2 | Branding cohérent | 🟢 | Logo "M", nom "Monito", tagline monitoring. Footer avec CGV/Confidentialité (placeholders). | HIGH |
| C3 | Page documentation complète | 🟢 | docs.html avec API reference + Docker deploy guide. Bon contenu technique. | HIGH |
| C4 | Pas de page statut public | 🟡 | Prévue en Business plan mais pas de template statut (même statique). | MED |
| C5 | Pas de page 404 personnalisée | 🟡 | Template 404 manquant. FastAPI retournera une page par défaut. | MED |

### D — Performance & Assets

| # | Critère | Résultat | Justification | Confiance |
|---|---------|----------|---------------|-----------|
| D1 | Static assets bundles | 🟢 | HTMX téléchargé localement (71 KB), CSS unique (~560 lignes), favicon SVG. | HIGH |
| D2 | Google Fonts externe | 🟡 | Dépendance externe pour le rendu. Fonctionnel mais requête HTTP supplémentaire et vie privée (RGPD — IP transmise à Google). Alternative : self-hoster Inter. | MED |
| D3 | Aucun tracking tiers | 🟢 | Aucun GA, Meta, Hotjar, etc. Conforme RGPD. | HIGH |
| D4 | Taille statique totale | 🟢 | ~71 KB pour HTMX + CSS + favicon. Excellent. | HIGH |

### E — Points de blocage obligatoires

| # | Point | Résultat | Détail |
|---|-------|----------|--------|
| E1 | Aucun tracker tiers sans consentement | ✅ PASS | Aucun tracker. Même les polices Google pourraient être considérées comme un transfert de données, mais acceptable en phase MVP. |
| E2 | Aucune donnée client exposée | ✅ PASS | Les templates sont des coquilles vides, aucune donnée cliente hardcodée. |
| E3 | Design cohérent avec le produit | ❌ FAIL (scope) | Les templates sont parfaitement conçus pour un monitoring serveur... mais le backend sert des formulaires. |

### F — Notes additionnelles

**Cohérence template/back-end :** Les templates sont alignés avec le branding "Monito" et le positionnement monitoring. Le problème n'est donc pas dans les templates — ils sont bons pour le monitoring. Le problème est que le backend ne correspond pas. Si le scope est corrigé (backend → vrai monitoring), les templates n'auront besoin que d'ajustements mineurs.

**Améliorations possibles (phase 2) :**
- Self-hoster Inter et JetBrains Mono (RGPD + offline)
- Ajouter template 404.html personnalisé
- Ajouter page statut publique statique (pour Business plan)
- Ajouter mode clair (toggle) si demande
- Ajouter meta tags Open Graph pour le partage

---

## Recommandations

1. **Corréler le scope** : Décider si le produit final est Monitoring ou Form Backend. Les templates sont bons pour le monitoring mais incohérents avec le backend actuel.

2. **Self-hoster les polices** : Pour RGPD et résilience, télécharger Inter + JetBrains Mono en local au lieu de Google Fonts.

3. **Ajouter template 404** : Page personnalisée pour les erreurs 404 (UX basique mais important).

4. **Aucun changement urgent** côté templates — le design est propre et fonctionnel.

---

*Grille remplie selon /root/monetization-lab/review-checklist.md version 2.0*
