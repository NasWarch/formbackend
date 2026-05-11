# Scoring Framework — examples d'utilisation

## Import dans un script

```python
import scoring_framework as sf

scores = {
    "urgency": 7,
    "willingness_to_pay": 8,
    "competition": 6,
    "distribution_difficulty": 5,
    "feasibility": 9,
    "time_to_first_dollar": 3,
    "gross_margin": 9,
    "legal_risk": 7,
    "data_availability": 8,
}

total, decision, raw, weighted = sf.score(scores)
print(f"Score : {total}/10 — Décision : {decision}")
```

## Depuis le terminal (stdin)

```bash
echo '{"scores": {"urgency": 7, "willingness_to_pay": 8, "competition": 6, "distribution_difficulty": 5, "feasibility": 9, "time_to_first_dollar": 3, "gross_margin": 9, "legal_risk": 7, "data_availability": 8}}' | python3 scoring_framework.py
```

## Poids personnalisés

```python
import scoring_framework as sf

my_weights = {
    "urgency": 0.05,
    "willingness_to_pay": 0.25,
    "competition": 0.05,
    "distribution_difficulty": 0.05,
    "feasibility": 0.10,
    "time_to_first_dollar": 0.15,
    "gross_margin": 0.20,
    "legal_risk": 0.05,
    "data_availability": 0.10,
}

sf.save_weights(my_weights)  # persiste pour usage futur
total, decision, _, _ = sf.score(scores)  # utilise désormais les nouveaux poids
```

## Décisions selon le seuil

| Score | Décision |
|-------|----------|
| >= 7.0 | PASSER — Go / strong opportunity |
| >= 5.0 | INVESTIGUER — Viable but needs deeper look |
| < 5.0 | ÉVITER — Weak opportunity, deprioritise |

## Scénarios concrets

### SaaS B2B niche (API pour marketplaces)
```python
scores = {
    "urgency": 9,    # fenêtre courte avant qu'un concurrent arrive
    "willingness_to_pay": 8,  # entreprise, budget dev
    "competition": 9,  # quasi aucun acteur
    "distribution_difficulty": 4,  # vente B2B directe
    "feasibility": 8,  # compétences en interne
    "time_to_first_dollar": 6,  # 2-3 mois
    "gross_margin": 9,  # SaaS pur
    "legal_risk": 8,  # standard
    "data_availability": 7,  # APIs publiques
}
# Résultat : ~7.5 — PASSER
```

### Newsletter payante niche
```python
scores = {
    "urgency": 5,
    "willingness_to_pay": 6,
    "competition": 5,
    "distribution_difficulty": 7,  # SEO + Twitter
    "feasibility": 9,
    "time_to_first_dollar": 4,  # temps pour construire l'audience
    "gross_margin": 9,
    "legal_risk": 8,
    "data_availability": 5,
}
# Résultat : ~6.5 — INVESTIGUER
```

### Agent IA automatisé
```python
scores = {
    "urgency": 8,
    "willingness_to_pay": 7,
    "competition": 3,  # beaucoup de monde
    "distribution_difficulty": 5,
    "feasibility": 7,
    "time_to_first_dollar": 2,  # long à monétiser
    "gross_margin": 8,
    "legal_risk": 4,  # zone grise
    "data_availability": 8,
}
# Résultat : ~5.8 — INVESTIGUER (avec réserves sur le legal)
```
