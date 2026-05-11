"""Users routes — profile, subscription status."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.subscription import Subscription

router = APIRouter()


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    """Profil de l'utilisateur connecté."""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "display_name": current_user.display_name,
        "is_admin": current_user.is_admin,
        "created_at": current_user.created_at.isoformat() if current_user.created_at else None,
    }


@router.get("/me/subscription")
def get_my_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Abonnement de l'utilisateur connecté."""
    sub = db.query(Subscription).filter(Subscription.user_id == current_user.id).first()
    if not sub:
        return {"subscription": None, "plan": None}

    return {
        "subscription": {
            "id": sub.id,
            "status": sub.status.value,
            "current_period_end": sub.current_period_end.isoformat() if sub.current_period_end else None,
            "trial_end": sub.trial_end.isoformat() if sub.trial_end else None,
            "cancel_at_period_end": sub.cancel_at_period_end,
        },
        "plan": {
            "name": sub.plan.name if sub.plan else None,
            "slug": sub.plan.slug if sub.plan else None,
        },
    }
