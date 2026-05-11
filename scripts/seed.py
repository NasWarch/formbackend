#!/usr/bin/env python3
"""Seed script — crée les plans tarifaires et un utilisateur admin.

Pricing basé sur la recommandation Growth (benchmarké sur Formspree, FormKeep):
  Free:    0€  / 50    soumissions
  Starter: 6€  / 500   soumissions
  Pro:     15€ / 3000  soumissions
  Scale:   35€ / 15000 soumissions
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.core.database import SessionLocal, engine, Base
from app.models.subscription import Plan


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    plans = [
        Plan(
            name="Free",
            slug="free",
            description="Pour démarrer — 50 soumissions/mois",
            price_cents=0,
            features='["50_submissions","1_form","basic_endpoint","email_notifications"]',
            sort_order=1,
        ),
        Plan(
            name="Starter",
            slug="starter",
            description="Usage personnel — 500 soumissions/mois",
            price_cents=600,
            features='["500_submissions","5_forms","webhooks","cors","spam_filtering","email_notifications"]',
            sort_order=2,
        ),
        Plan(
            name="Pro",
            slug="pro",
            description="Usage professionnel — 3000 soumissions/mois",
            price_cents=1500,
            features='["3000_submissions","unlimited_forms","webhooks","cors","csv_export","email_templates","custom_domain","spam_filtering","file_uploads","priority_support"]',
            sort_order=3,
        ),
        Plan(
            name="Scale",
            slug="scale",
            description="Solution sur mesure — 15000 soumissions/mois",
            price_cents=3500,
            features='["15000_submissions","unlimited_forms","webhooks","cors","csv_export","email_templates","custom_domain","spam_filtering","file_uploads","api_access","dedicated_support"]',
            sort_order=4,
        ),
    ]

    for plan in plans:
        existing = db.query(Plan).filter(Plan.slug == plan.slug).first()
        if not existing:
            db.add(plan)
            print(f"  + Plan créé : {plan.name} ({plan.slug}) — {plan.price_cents / 100:.2f}€")
        else:
            # Update pricing if plan exists
            existing.price_cents = plan.price_cents
            existing.description = plan.description
            existing.features = plan.features
            existing.sort_order = plan.sort_order
            print(f"  ~ Plan mis à jour : {plan.name} ({plan.slug}) — {plan.price_cents / 100:.2f}€")

    # If old "business" plan exists, remove it (replaced by Scale)
    old_business = db.query(Plan).filter(Plan.slug == "business").first()
    if old_business:
        db.delete(old_business)
        print("  - Plan supprimé : Business (remplacé par Scale)")

    db.commit()
    db.close()
    print("Seed terminé.")


if __name__ == "__main__":
    seed()
