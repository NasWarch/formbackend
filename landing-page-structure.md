# Landing Page Structure — Template Réutilisable

> Tenant : monetization-lab
> Usage : Adapter les sections ci-dessous pour chaque produit/campagne.
> Principe : une section = un objectif. Pas de contenu décoratif.

---

## 1. Structure Standard (7 sections)

### HERO — 3 secondes max
- [ ] Titre : formule problème + solution en ≤ 10 mots
- [ ] Sous-titre : bénéfice concret, chiffré si possible
- [ ] CTA unique : verbe d'action + promesse (« Commencer ma première analyse »)
- [ ] Image / démo visuelle : screenshot, animation, ou mockup du produit en action
- [ ] Social proof starter : « Déjà utilisé par X beta-testeurs » ou logo de confiance

### PROBLEM — la douleur
- [ ] Décrire le problème en termes que le client utilise lui-même (verbatims)
- [ ] Pas de jargon technique, pas de nom de produit
- [ ] Une phrase qui fait hocher la tête (« Vous en avez marre de… »)
- [ ] *Optionnel* : calcul du coût du problème (temps perdu × €/h)

### SOLUTION — comment ça marche
- [ ] 3 étapes max (visuelles, numérotées)
- [ ] Chaque étape = une ligne + une icône/screenshot
- [ ] Pas de détails techniques — « comment » pas « avec quoi »
- [ ] Lien vers docs ou demo si besoin

### FEATURES / BÉNÉFICES
- [ ] 3 à 6 features, chaque feature = bénéfice client (pas caractéristique technique)
- [ ] Format : icône + titre court + phrase d'explication
- [ ] Hiérarchie visuelle : la feature la plus distinctive en premier

### SOCIAL PROOF
- [ ] Témoignages clients réels (nom, fonction, entreprise, photo)
- [ ] Chiffres d'impact : « +40% de productivité », « 3x plus rapide »
- [ ] Logos clients / partenaires (si existants)
- [ ] Cas d'usage / success stories (1-2 max)

### PRICING
- [ ] 3 plans max (Starter, Pro, Enterprise ou Gratuit, Pro, Custom)
- [ ] Plan recommandé mis en avant visuellement
- [ ] Comparaison claire des features
- [ ] CTA par plan
- [ ] FAQ pricing (question fréquente = objection levée)
- [ ] Garantie / période d'essai affichée

### CTA FINAL
- [ ] Rappel du bénéfice principal
- [ ] Bouton CTA identique à celui du hero
- [ ] Dernière objection levée (sécurité, données, support)
- [ ] Signal de confiance final (garantie, badges security, nombre d'utilisateurs)

---

## 2. Variation par objectif

| Objectif | Hero | CTA | Section supplémentaire |
|----------|------|-----|----------------------|
| **Lead gen** | Offre irrésistible (ebook, checklist) | « Télécharger gratuitement » | Formulaire (nom, email) |
| **Free trial** | « Essayez gratuitement 14 jours » | « Commencer l'essai » | Onboarding steps |
| **Waitlist** | FOMO + exclusivité | « Rejoindre la liste d'attente » | Compteur d'inscrits |
| **Direct sale** | Prix + promesse ROI | « Acheter maintenant » | Garantie remboursée |
| **Newsletter** | « Recevez X chaque semaine » | « S'abonner gratuitement » | Exemple d'édito |

---

## 3. Éléments obligatoires (toutes les pages)

- [ ] Favicon
- [ ] Meta title + description (SEO)
- [ ] Open Graph (Facebook, LinkedIn, Twitter)
- [ ] Lien vers CGV / Privacy Policy
- [ ] Cookie consent banner (même sans GA — couverture légale)
- [ ] Footer : contact, legal, réseaux sociaux
- [ ] Analytics pixel installé (voir analytics-events-plan.md)
- [ ] Page speed ≤ 3s (Lighthouse mobile)
- [ ] Mobile responsive testé sur 3 appareils minimum
- [ ] 404 page custom

---

## 4. Tests A/B à prévoir (phase 2)

| Élément | Variables à tester |
|---------|-------------------|
| Titre du hero | Bénéfice vs. douleur vs. curiosité |
| CTA | Couleur, texte, position |
| Images | Produit vs. lifestyle vs. abstract |
| Pricing | Ordre des plans, prix, features listées |
| Social proof | Nombre vs. détail d'un seul témoignage |

---

> **Principe :** chaque section doit pouvoir être testée isolément.
> Si tu ne peux pas A/B tester un élément, c'est qu'il est probablement décoratif.
