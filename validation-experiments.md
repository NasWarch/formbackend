# Validation Experiments — Framework Réutilisable

> Tenant : monetization-lab  
> Principe : chaque hypothèse doit être testée avant d'y consacrer 1 semaine de dev.  
> Si ça peut être testé en 1 jour, fais-le en 1 jour.

---

## 1. Hiérarchie des Expériences

```
Coût ↓ / Confiance ↑
        │
  ┌─────┴─────┐
  │  Paiement │  ← Pre-orders, LOIs, ventes réelles
  ├───────────┤
  │  Temps    │  ← Inscriptions waitlist, signups, téléchargements
  ├───────────┤
  │  Intention│  ← Sondages, interviews, landing page A/B
  └───────────┘
  │  Opinion  │  ← « Tu achèterais ça ? » (le moins fiable)
        │
Pertinence ↓ / Bruit ↑
```

**Principe :** tester au niveau le plus haut possible. Une vente réelle vaut 1000 opinions.

---

## 2. Pré-Lancement (avant d'écrire du code)

### Expérience 1 : Landing Page Smoke Test

**Hypothèse :** « Les gens sont intéressés par ce problème/solution. »

- [ ] Créer une landing page one-pager avec ton produit décrit (même s'il n'existe pas)
- [ ] Ajouter un CTA « S'inscrire pour un accès anticipé » (collecte d'email)
- [ ] Drive du trafic : posts Twitter/LinkedIn, partage dans 2 communautés
- [ ] **Succès =** ≥ 5% de conversion visiteurs → emails
- [ ] **Intervalle :** 1 semaine ou 500 visiteurs

### Expérience 2 : Smoke Test "Faux CTA"

**Hypothèse :** « Les gens cliqueraient sur "Acheter" si le produit existait. »

- [ ] Landing page avec un bouton « Voir les prix » ou « Commencer »
- [ ] Au clic : modal indiquant « Nous arrivons bientôt — laissez votre email »
- [ ] **Succès =** ≥ 3% de clics sur le CTA (sur les visiteurs)
- [ ] **Échec =** personne ne clique → ton message ne résonne pas

### Expérience 3 : Interviews Problème

**Hypothèse :** « Le problème est suffisamment douloureux pour payer. »

- [ ] Identifier 10 personnes correspondant au persona cible
- [ ] Les interviewer sur LEUR problème (pas sur ton produit)
- [ ] Questions clés :
  - « Qu'utilises-tu actuellement pour résoudre X ? »
  - « Qu'est-ce qui te frustre le plus avec la solution actuelle ? »
  - « Combien de temps perds-tu par semaine à cause de X ? »
  - « Combien paierais-tu pour un outil qui résoudrait X ? »
- [ ] **Succès =** ≥ 7/10 confirment un problème récurrent ET un montant cohérent avec ton pricing
- [ ] **Red flag :** si personne ne mentionne le problème spontanément

---

## 3. Lancement (version fonctionnelle, même brutale)

### Expérience 4 : Concierge MVP

**Principe :** tu fais manuellement ce que le produit fera automatisé.

- [ ] Offrir le service manuellement à 3-5 beta-testeurs
- [ ] Tu exécutes toi-même le process (envoi de rapports, analyses, etc.)
- [ ] Tu notes le temps passé, les douleurs, ce qui est répétable
- [ ] **Succès =** tes beta-testeurs continuent d'utiliser le service après 2 semaines
- [ ] **Trouvaille :** tu découvres ce qui est vraiment important avant d'automatiser

### Expérience 5 : Pre-Orders / Letter of Intent

**Hypothèse :** « Des inconnus sont prêts à payer. »

- [ ] Une fois le concierge MVP validé, proposer un tarif réduit à vie aux 10 premiers
- [ ] « Early adopter — tarif fondateur : 50% de réduction à vie »
- [ ] **Succès =** ≥ 3 pré-commandes sur 10 prospects
- [ ] **Super succès =** ≥ 5 pré-commandes → fonce
- [ ] **Échec =** zéro → ton pricing est trop haut ou la valeur perçue trop faible

---

## 4. Post-Lancement (produit live)

### Expérience 6 : Feature Adoption Test

**Hypothèse :** « La feature X est utile et sera utilisée. »

- [ ] Mesurer l'utilisation de X après 7 jours de disponibilité
- [ ] **Succès =** ≥ 30% des utilisateurs actifs hebdo utilisent X
- [ ] **Si < 10% :** X n'est pas assez visible, trop complexe, ou inutile → pivoter ou supprimer

### Expérience 7 : Pricing Elasticity (3-cell A/B)

**Hypothèse :** « Le pricing actuel est optimal. »

- [ ] 3 cohortes de nouveaux arrivants voient 3 prix différents :
  - Groupe A : prix actuel
  - Groupe B : prix +20%
  - Groupe C : prix -20%
- [ ] Mesurer sur 2 semaines : taux de conversion et MRR par visiteur
- [ ] **Gagnant =** le prix avec le meilleur LTV, pas juste le meilleur taux de conversion

### Expérience 8 : NPS Loop

**Hypothèse :** « On sait pourquoi les gens restent ou partent. »

- [ ] Email J30 : NPS (0-10) + question ouverte
  - Promoteurs (9-10) : « Qu'est-ce que tu aimes le plus ? »
  - Détracteurs (0-6) : « Qu'est-ce qui te manque ou t'a déçu ? »
- [ ] **Seuil :** cibler NPS ≥ 30 après 3 mois
- [ ] **Action :** chaque mois, adresser la plainte #1 des détracteurs

---

## 5. Tableau de Décision

| Résultat combinaison | Action |
|---------------------|--------|
| Smoke test ✅ + Interviews ✅ | Construire le MVP |
| Smoke test ✅ + Interviews ❌ | Revoir le message, personas, ou prix |
| Smoke test ❌ + Interviews ✅ | Le problème existe mais ton message ne passe pas. Retravailler le copy. |
| Smoke test ❌ + Interviews ❌ | Le problème n'est pas assez urgent. Changer de problème ou d'audience. |
| Pre-orders ✅ | Accélérer le développement, prioriser les features des early adopters |
| Pre-orders ❌ mais usage engagement ✅ | Revoir le pricing (trop haut) ou la proposition de valeur (pas assez claire) |
| Concierge ✅ mais produit automatisé ❌ | Le service humain était la vraie valeur → repenser l'approche produit |

---

## 6. Anti-Patterns

- **"On lance et on verra"** — sans hypothèse testable, tu ne sauras pas quoi mesurer.
- **"Tout le monde m'a dit que c'était une bonne idée"** — les amis / famille ne sont pas un échantillon valide.
- **"Les premiers utilisateurs sont venus gratuitement donc c'est validé"** — gratuit ≠ validation. L'engagement et le paiement sont les vrais signaux.
- **"On va A/B tester le pricing dès le premier jour"** — pas assez de trafic. Minimum 1000 visiteurs par variante.
- **Arrêter les expériences après le premier résultat positif** — confirme avec une deuxième expérience de niveau supérieur.

---

> **Rappel :** le but n'est pas de prouver que tu as raison. Le but est de découvrir la vérité le plus vite possible, même si elle dérange.
