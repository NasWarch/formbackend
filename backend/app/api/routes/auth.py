"""Auth routes — magic link generation, token verification, refresh.

HTMX-compatible: le POST /auth/magic-link retourne du HTML pour le formulaire de login.
En dev, le token est affiché comme lien cliquable (pas d'email SMTP).
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from jose import JWTError
from pydantic import EmailStr

from app.core.database import get_db
from app.core.config import settings
from app.core.limiter import limiter
from app.core.security import (
    create_access_token,
    create_refresh_token,
    create_magic_link_token,
    decode_token,
)
from app.models.user import User
from app.schemas.auth import MagicLinkRequest, TokenResponse, RefreshRequest

router = APIRouter()


@router.post("/magic-link")
@limiter.limit(settings.RATE_LIMIT)
async def request_magic_link(request: Request, db: Session = Depends(get_db)):
    """Étape 1 : demande de magic link. Crée l'utilisateur si inexistant.
    Retourne HTML pour HTMX (swap dans #magic-result) ou JSON pour l'API.
    """
    # Support form-encoded (HTMX) et JSON (API)
    content_type = request.headers.get("content-type", "")
    if "application/json" in content_type:
        body = await request.json()
        email = body.get("email", "")
    else:
        form_data = await request.form()
        email = form_data.get("email", "")

    if not email or "@" not in email:
        if request.headers.get("HX-Request"):
            return HTMLResponse(
                '<p class="text-red-400 text-sm mt-3">Adresse email invalide.</p>'
            )
        raise HTTPException(status_code=400, detail="Invalid email")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(email=email, display_name=email.split("@")[0])
        db.add(user)
        db.commit()
        db.refresh(user)

    token = create_magic_link_token(email)
    base_url = str(request.base_url).rstrip("/")
    magic_link = f"{base_url}/auth/verify-page?token={token}"

    # HTMX response — rendu dans le formulaire de login
    if request.headers.get("HX-Request"):
        return HTMLResponse(f"""
        <div class="mt-4 p-4 rounded-xl bg-gray-900/50 border border-indigo-700/30">
            <div class="flex items-start gap-3">
                <svg class="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
                <div>
                    <p class="text-green-400 text-sm font-medium">Lien magique prêt !</p>
                    <p class="text-gray-400 text-xs mt-1">Mode développement — cliquez sur le lien ci-dessous :</p>
                    <a href="{magic_link}"
                       class="block mt-3 px-4 py-2 rounded-lg bg-indigo-600 text-white text-sm font-medium text-center hover:bg-indigo-500 transition-colors">
                        Se connecter en tant que {email}
                    </a>
                    <p class="text-gray-500 text-xs mt-2">Ce lien expire dans 15 minutes.</p>
                </div>
            </div>
        </div>
        """)

    # JSON response pour l'API
    return {
        "message": "Magic link sent (dev mode)",
        "dev_token": token,
        "magic_link": magic_link,
    }


@router.post("/magic-link-json")
def request_magic_link_json(payload: MagicLinkRequest, db: Session = Depends(get_db)):
    """Alternative JSON endpoint for API clients."""
    email = payload.email
    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(email=email, display_name=email.split("@")[0])
        db.add(user)
        db.commit()
        db.refresh(user)

    token = create_magic_link_token(email)
    return {
        "message": "Magic link sent (dev mode)",
        "dev_token": token,
    }


@router.get("/verify", response_model=TokenResponse)
def verify_magic_link(token: str, db: Session = Depends(get_db)):
    """Étape 2 : vérification du magic link → JWT pair."""
    try:
        payload = decode_token(token)
        if payload.get("type") != "magic_link":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token type",
            )
        email: str = payload.get("sub")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired magic link",
        )

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return TokenResponse(
        access_token=create_access_token(subject=user.id),
        refresh_token=create_refresh_token(subject=user.id),
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh_tokens(payload: RefreshRequest):
    """Échange un refresh token valide contre un nouveau JWT pair."""
    try:
        payload_decoded = decode_token(payload.refresh_token)
        if payload_decoded.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token type",
            )
        user_id = payload_decoded.get("sub")
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    return TokenResponse(
        access_token=create_access_token(subject=user_id),
        refresh_token=create_refresh_token(subject=user_id),
    )
