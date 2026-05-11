#!/usr/bin/env python3
"""
Scoring framework for opportunity selection (monetization-lab).
Reusable module: import and call score() with dimension values (0-10).
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple

WEIGHTS_PATH = Path(__file__).parent / "scoring_weights.json"

# ---------------------------------------------------------------------------
# Dimension definitions
# ---------------------------------------------------------------------------

DIMENSIONS = {
    "urgency": {
        "label": "Urgence",
        "description": "Time-sensitivity of the opportunity. Is there a closing window?",
        "low": "No rush — can start anytime (0-3)",
        "high": "Window is closing fast — must act now (8-10)",
    },
    "willingness_to_pay": {
        "label": "Willingness to pay",
        "description": "How much are target customers actually willing to pay?",
        "low": "Free/cheap expectations only (0-3)",
        "high": "High willingness, proven willingness in adjacent markets (8-10)",
    },
    "competition": {
        "label": "Competition",
        "description": "How saturated is the market? (inverted — higher score = less competition)",
        "low": "Crowded, well-funded, entrenched players (0-3)",
        "high": "Green field or fragmented / poorly served (8-10)",
    },
    "distribution_difficulty": {
        "label": "Distribution difficulty",
        "description": "How hard is it to reach paying customers? (inverted — higher = easier)",
        "low": "Requires sales team, big ad budget, or partnerships (0-3)",
        "high": "Existing audience, viral loop, or cheap channels (8-10)",
    },
    "feasibility": {
        "label": "Faisabilité",
        "description": "Can we build/ship this with available skills & tools?",
        "low": "Needs skills/tech we don't have — high risk (0-3)",
        "high": "Well within our capabilities (8-10)",
    },
    "time_to_first_dollar": {
        "label": "Time-to-first-dollar",
        "description": "How long until first revenue? (inverted — higher = faster)",
        "low": "6+ months to first dollar (0-3)",
        "high": "Monetizable within weeks (8-10)",
    },
    "gross_margin": {
        "label": "Gross margin",
        "description": "Unit economics — revenue minus direct costs.",
        "low": "Under 40% margin (0-3)",
        "high": "80%+ margin (software, content, data products) (8-10)",
    },
    "legal_risk": {
        "label": "Legal risk",
        "description": "Regulatory / legal exposure. (inverted — higher = safer)",
        "low": "Heavily regulated, high liability, uncertain legal ground (0-3)",
        "high": "No special regulation, low liability (8-10)",
    },
    "data_availability": {
        "label": "Data availability",
        "description": "Can we get the data needed to deliver value?",
        "low": "Data doesn't exist, is paywalled, or hard to scrape legally (0-3)",
        "high": "Public APIs, open data, or we already have it (8-10)",
    },
}

DEFAULT_WEIGHTS: Dict[str, float] = {
    "urgency": 0.10,
    "willingness_to_pay": 0.15,
    "competition": 0.10,
    "distribution_difficulty": 0.10,
    "feasibility": 0.15,
    "time_to_first_dollar": 0.10,
    "gross_margin": 0.10,
    "legal_risk": 0.10,
    "data_availability": 0.10,
}

DECISION_THRESHOLDS = {
    "green": 7.0,    # Go — strong opportunity
    "amber": 5.0,    # Investigate further — viable but has risks
    # Below 5.0 = red — weak opportunity, deprioritise
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _clamp(val: float, lo: float = 0.0, hi: float = 10.0) -> float:
    return max(lo, min(hi, val))


def _validate_and_clamp(scores: Dict[str, float]) -> Dict[str, float]:
    validated = {}
    for key in DIMENSIONS:
        if key not in scores:
            raise ValueError(f"Missing dimension: {key!r}")
        validated[key] = _clamp(scores[key])
    return validated


def load_weights(path: Optional[Path] = None) -> Dict[str, float]:
    """Load weights from JSON file, falling back to defaults."""
    p = path or WEIGHTS_PATH
    if p.exists():
        with open(p) as f:
            return json.load(f)

    # Write defaults if file doesn't exist
    save_weights(DEFAULT_WEIGHTS, p)
    return dict(DEFAULT_WEIGHTS)


def save_weights(weights: Dict[str, float], path: Optional[Path] = None) -> None:
    """Persist custom weights to JSON file."""
    p = path or WEIGHTS_PATH
    # Validate all keys
    for k in weights:
        if k not in DIMENSIONS:
            raise ValueError(f"Unknown dimension: {k!r}")
    with open(p, "w") as f:
        json.dump(weights, f, indent=2)
        f.write("\n")


def _check_weights_sum(weights: Dict[str, float]) -> float:
    s = sum(weights.values())
    if abs(s - 1.0) > 0.02:
        raise ValueError(f"Weights sum to {s:.3f}, expected ~1.0")
    return s

# ---------------------------------------------------------------------------
# Core scoring
# ---------------------------------------------------------------------------

def score(
    scores: Dict[str, float],
    weights: Optional[Dict[str, float]] = None,
) -> Tuple[float, str, Dict[str, float], Dict[str, float]]:
    """
    Evaluate an opportunity.

    Parameters
    ----------
    scores : dict
        Values 0-10 for each dimension in DIMENSIONS.
    weights : dict or None
        Custom weights (must sum to ~1.0). Falls back to saved / defaults.

    Returns
    -------
    (total_score, decision_label, dimension_scores, weighted_scores)
    """
    validated = _validate_and_clamp(scores)
    w = load_weights() if weights is None else weights
    _check_weights_sum(w)

    raw_breakdown = {}
    weighted_breakdown = {}
    total = 0.0
    for dim, val in validated.items():
        wt = w[dim]
        weighted = val * wt
        raw_breakdown[dim] = val
        weighted_breakdown[dim] = round(weighted, 2)
        total += weighted

    total = round(total, 2)

    if total >= DECISION_THRESHOLDS["green"]:
        decision = "PASSER — Go / strong opportunity"
    elif total >= DECISION_THRESHOLDS["amber"]:
        decision = "INVESTIGUER — Viable but needs deeper look"
    else:
        decision = "ÉVITER — Weak opportunity, deprioritise"

    return total, decision, raw_breakdown, weighted_breakdown


def score_from_stdin() -> None:
    """CLI entrypoint: reads JSON scores from stdin, prints result."""
    import sys
    data = json.load(sys.stdin)
    scores = data.get("scores")
    if not scores:
        print('Usage: echo \'{"scores": {"urgency": 8, ...}}\' | python3 scoring_framework.py')
        sys.exit(1)
    weights = data.get("weights")
    total, decision, raw, weighted = score(scores, weights)
    print(f"Score total : {total:.2f}/10")
    print(f"Décision   : {decision}")
    print()
    print("Détail :")
    for dim in DIMENSIONS:
        label = DIMENSIONS[dim]["label"]
        r = raw[dim]
        w = weighted[dim]
        print(f"  {label:25s}  {r:5.1f}  x {w/r:.2f}  =  {w:.2f}" if r > 0 else
              f"  {label:25s}  {r:5.1f}  x 0.00  =  0.00")


def describe_dimensions() -> Dict[str, dict]:
    """Return structured dimension metadata (for documentation, export)."""
    return DIMENSIONS


if __name__ == "__main__":
    score_from_stdin()
