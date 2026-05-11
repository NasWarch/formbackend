"""Monetization Lab — Backend FastAPI application.
MVP product: Form Backend API (form backend as a service).
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.core.limiter import limiter
from sqlalchemy.orm import Session
from sqlalchemy import text
from jose import JWTError

from app.core.config import settings
import json

from app.core.database import engine, Base, get_db
from app.core.redis import init_redis
from app.core.security import decode_token
from app.models.user import User
from app.models.subscription import Plan, Subscription
from app.api.routes import auth, users, billing, webhooks, health


# ─── Feature labels for pricing page ─────────────────────────────────────────

FEATURE_LABELS = {
    "50_submissions": "50 soumissions/mois",
    "500_submissions": "500 soumissions/mois",
    "3000_submissions": "3000 soumissions/mois",
    "15000_submissions": "15000 soumissions/mois",
    "1_form": "1 formulaire",
    "5_forms": "5 formulaires",
    "unlimited_forms": "Formulaires illimités",
    "basic_endpoint": "Endpoint API de base",
    "email_notifications": "Notifications email",
    "webhooks": "Webhooks",
    "cors": "CORS personnalisé",
    "spam_filtering": "Filtrage anti-spam",
    "csv_export": "Export CSV",
    "email_templates": "Templates email",
    "custom_domain": "Domaine personnalisé",
    "file_uploads": "Upload de fichiers",
    "priority_support": "Support prioritaire",
    "api_access": "Accès API complet",
    "dedicated_support": "Support dédié",
    "data_retention": "Rétention des données",
}

# Ordered list for display — plans with "all" get everything
ALL_FEATURE_KEYS = [
    "50_submissions", "1_form", "basic_endpoint",
    "500_submissions", "5_forms",
    "3000_submissions", "unlimited_forms",
    "email_notifications", "webhooks", "cors", "spam_filtering",
    "csv_export", "email_templates", "custom_domain", "file_uploads",
    "priority_support",
    "15000_submissions",
    "api_access", "dedicated_support",
]


def format_plan_features(feature_keys: list[str]) -> list[dict]:
    """Convert feature keys to template-compatible [{\"label\": ..., \"included\": bool}]."""
    included = set(fk for fk in feature_keys if fk != "all")
    is_all = "all" in feature_keys

    # Determine which keys this plan includes
    result = []
    keys_to_show = [k for k in ALL_FEATURE_KEYS if k in included or is_all]
    seen = set()
    for k in keys_to_show:
        if k in seen:
            continue
        seen.add(k)
        result.append({
            "label": FEATURE_LABELS.get(k, k),
            "included": True,
        })
    return result


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_redis()
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown


app = FastAPI(
    title="Form Backend API",
    version="0.1.0",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# API Routers
app.include_router(health.router, prefix="", tags=["health"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])

templates = Jinja2Templates(directory="app/templates")


# ─── Cookie-based auth helper ────────────────────────────────────────────────

def get_current_user_from_request(request: Request, db: Session = Depends(get_db)) -> User | None:
    """Try cookie first, then Authorization header. Returns None if unauthenticated."""
    token = request.cookies.get("access_token")
    if not token:
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]

    if not token:
        return None

    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            return None
        user_id = payload.get("sub")
        if user_id is None:
            return None
    except JWTError:
        return None

    user = db.query(User).filter(User.id == user_id).first()
    if user is None or not user.is_active:
        return None
    return user


def get_user_context(request: Request, db: Session = Depends(get_db)) -> dict:
    """Build a user context dict for templates — avoids passing None."""
    user = get_current_user_from_request(request, db)
    if user is None:
        return {"user": None}
    return {
        "user": {
            "id": user.id,
            "email": user.email,
            "display_name": user.display_name,
            "is_admin": user.is_admin,
        }
    }


# ─── Page routes ─────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
def landing_page(request: Request, ctx: dict = Depends(get_user_context)):
    return templates.TemplateResponse(request, "index.html", ctx)


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request, ctx: dict = Depends(get_user_context)):
    return templates.TemplateResponse(request, "login.html", ctx)


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(request: Request, ctx: dict = Depends(get_user_context), db: Session = Depends(get_db)):
    if ctx["user"] is None:
        return RedirectResponse(url="/login", status_code=302)

    user_id = ctx["user"]["id"]
    user = db.query(User).filter(User.id == user_id).first()
    sub = db.query(Subscription).filter(Subscription.user_id == user_id).first()

    plan_name = "Free"
    plan_slug = "free"
    if sub and sub.plan:
        plan_name = sub.plan.name
        plan_slug = sub.plan.slug

    ctx["plan"] = {"name": plan_name, "slug": plan_slug}
    return templates.TemplateResponse(request, "dashboard.html", ctx)


@app.get("/pricing", response_class=HTMLResponse)
def pricing_page(request: Request, ctx: dict = Depends(get_user_context), db: Session = Depends(get_db)):
    db_plans = db.query(Plan).filter(Plan.is_active == True).order_by(Plan.sort_order).all()

    plans = []
    for p in db_plans:
        features = json.loads(p.features) if isinstance(p.features, str) else p.features or []
        plans.append({
            "name": p.name,
            "desc": p.description or "",
            "price": p.price_cents / 100,
            "highlight": p.slug == "pro",
            "slug": p.slug,
            "features": format_plan_features(features),
        })

    ctx["plans"] = plans
    return templates.TemplateResponse(request, "pricing.html", ctx)


@app.get("/formspree-alternative", response_class=HTMLResponse)
def formspree_alternative_page(request: Request, ctx: dict = Depends(get_user_context)):
    return templates.TemplateResponse(request, "formspree_alternative.html", ctx)


@app.get("/documentation", response_class=HTMLResponse)
def docs_page(request: Request, ctx: dict = Depends(get_user_context)):
    return templates.TemplateResponse(request, "docs.html", ctx)


# ─── Auth page flow ──────────────────────────────────────────────────────────

@app.get("/auth/verify-page")
def verify_magic_link_page(token: str, request: Request, db: Session = Depends(get_db)):
    """Vérifie le magic link et stocke le JWT dans un cookie, puis redirige."""
    try:
        payload = decode_token(token)
        if payload.get("type") != "magic_link":
            raise HTTPException(status_code=400, detail="Invalid token type")
        email = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired magic link")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    from app.core.security import create_access_token, create_refresh_token
    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)

    response = RedirectResponse(url="/dashboard", status_code=302)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
        max_age=900,  # 15 min
        secure=False,  # True en production
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="lax",
        max_age=604800,  # 7 jours
        secure=False,
    )
    return response


# ─── Form Backend API endpoints (MVP) ──────────────────────────────────────

FORMS_DB: dict = {}  # In-memory for MVP: user_id -> [{id, name, endpoint, submissions}]

@app.get("/api/forms")
def list_forms(request: Request, db: Session = Depends(get_db)):
    """HTMX: liste les formulaires de l'utilisateur connecté."""
    user = get_current_user_from_request(request, db)
    if not user:
        return HTMLResponse("Non connecté", status_code=401)

    forms = FORMS_DB.get(user.id, [])
    if not forms:
        return HTMLResponse("""
        <div class="text-center py-12 text-gray-400">
            <svg class="w-16 h-16 mx-auto mb-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
            </svg>
            <p class="text-lg font-medium">Aucun formulaire encore</p>
            <p class="text-sm mt-1">Créez votre premier formulaire pour commencer.</p>
        </div>
        """)

    cards = ""
    for f in forms:
        cards += f"""
        <div class="bg-gray-800/50 rounded-xl p-5 border border-gray-700 hover:border-indigo-500/50 transition-all">
            <div class="flex items-start justify-between mb-3">
                <div>
                    <h3 class="text-white font-semibold text-lg">{f['name']}</h3>
                    <code class="text-xs text-gray-400 font-mono">{f['endpoint']}</code>
                </div>
                <span class="px-2.5 py-1 rounded-full text-xs font-medium bg-indigo-900/50 text-indigo-300 border border-indigo-700/50">
                    {f.get('submissions', 0)} soumissions
                </span>
            </div>
            <div class="flex gap-2 mt-4">
                <button class="text-xs px-3 py-1.5 rounded-lg bg-gray-700 text-gray-300 hover:bg-gray-600 transition-colors"
                        hx-get="/api/forms/{f['id']}/submissions"
                        hx-target="#submissions-panel"
                        hx-swap="innerHTML">
                    Voir les soumissions
                </button>
                <button class="text-xs px-3 py-1.5 rounded-lg bg-gray-700 text-gray-300 hover:bg-gray-600 transition-colors"
                        hx-get="/api/forms/{f['id']}/embed"
                        hx-target="#embed-modal"
                        hx-swap="innerHTML">
                    Intégrer
                </button>
                <button class="text-xs px-3 py-1.5 rounded-lg bg-red-900/50 text-red-300 hover:bg-red-800/50 transition-colors ml-auto"
                        hx-post="/api/forms/{f['id']}/delete"
                        hx-target="#forms-list"
                        hx-swap="innerHTML"
                        hx-confirm="Supprimer le formulaire «{f['name']}» ? Toutes les soumissions seront perdues.">
                    Supprimer
                </button>
            </div>
        </div>
        """
    return HTMLResponse(f"""
    <div class="grid gap-4" id="forms-grid">
        {cards}
    </div>
    """)


@app.get("/api/forms/{form_id}/submissions")
def get_form_submissions(form_id: str, request: Request, db: Session = Depends(get_db)):
    """HTMX: affiche les soumissions d'un formulaire."""
    user = get_current_user_from_request(request, db)
    if not user:
        return HTMLResponse("Non connecté", status_code=401)

    forms = FORMS_DB.get(user.id, [])
    form = next((f for f in forms if f["id"] == form_id), None)
    if not form:
        return HTMLResponse('<p class="text-red-400">Formulaire introuvable</p>')

    subs = form.get("submissions_data", [])
    if not subs:
        return HTMLResponse(f"""
        <div class="bg-gray-800/50 rounded-xl p-6 border border-gray-700">
            <h4 class="text-white font-semibold mb-4">Soumissions — {form['name']}</h4>
            <p class="text-gray-400 text-sm">Aucune soumission pour le moment.</p>
        </div>
        """)

    rows = ""
    for s in subs[-10:]:  # 10 dernières
        fields = "".join(f'<span class="inline-block bg-gray-700/50 rounded px-2 py-0.5 text-xs text-gray-300 mr-1 mb-1">{k}: {v}</span>' for k, v in s.get("data", {}).items())
        rows += f"""
        <tr class="border-t border-gray-700 hover:bg-gray-700/30">
            <td class="py-3 px-4 text-gray-300 text-sm">{s.get('created_at', '—')}</td>
            <td class="py-3 px-4 text-gray-300 text-sm">{fields}</td>
        </tr>
        """

    return HTMLResponse(f"""
    <div class="bg-gray-800/50 rounded-xl p-6 border border-gray-700">
        <h4 class="text-white font-semibold mb-4">Soumissions — {form['name']}</h4>
        <div class="overflow-x-auto">
            <table class="w-full text-left">
                <thead>
                    <tr class="text-gray-400 text-xs uppercase tracking-wider">
                        <th class="pb-2 px-4">Date</th>
                        <th class="pb-2 px-4">Données</th>
                    </tr>
                </thead>
                <tbody>{rows}</tbody>
            </table>
        </div>
        {f'<p class="text-xs text-gray-500 mt-3">Dernières {min(len(subs), 10)} soumissions sur {len(subs)}</p>' if len(subs) > 10 else ''}
    </div>
    """)


@app.get("/api/forms/{form_id}/embed")
def get_form_embed(form_id: str, request: Request, db: Session = Depends(get_db)):
    """HTMX: affiche le code d'intégration d'un formulaire."""
    user = get_current_user_from_request(request, db)
    if not user:
        return HTMLResponse("Non connecté", status_code=401)

    forms = FORMS_DB.get(user.id, [])
    form = next((f for f in forms if f["id"] == form_id), None)
    if not form:
        return HTMLResponse('<p class="text-red-400">Formulaire introuvable</p>')

    base_url = request.base_url

    turnstile_enabled = form.get("turnstile_enabled", True)
    turnstile_site_key = settings.TURNSTILE_SITE_KEY

    turnstile_html = ""
    if turnstile_enabled:
        turnstile_html = f"""\
  <div class="cf-turnstile" data-sitekey="{turnstile_site_key}"></div>
  <script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>"""

    embed_code = f'''<form action="{base_url}api/f/{form["endpoint"]}" method="POST">
  <input type="text" name="name" placeholder="Votre nom" required>
  <input type="email" name="email" placeholder="Votre email" required>
  <textarea name="message" placeholder="Votre message"></textarea>
  <!-- Anti-spam honeypot: ne pas modifier -->
  <input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off">
{turnstile_html}
  <button type="submit">Envoyer</button>
</form>'''

    return HTMLResponse(f"""\
    <div class="fixed inset-0 bg-black/60 flex items-center justify-center z-50" id="embed-modal">
        <div class="bg-gray-800 rounded-2xl p-6 max-w-lg w-full mx-4 border border-gray-700 shadow-2xl">
            <div class="flex items-center justify-between mb-4">
                <h4 class="text-white font-semibold">Intégrer — {form['name']}</h4>
                <button class="text-gray-400 hover:text-white text-xl" onclick="document.getElementById('embed-modal').remove()">&times;</button>
            </div>
            <p class="text-gray-400 text-sm mb-3">Copiez ce code HTML dans votre site statique :</p>
            <pre class="bg-gray-900 rounded-xl p-4 text-xs text-gray-300 overflow-x-auto font-mono border border-gray-700"><code>{embed_code}</code></pre>
            <div class="mt-3 flex items-center gap-2 text-xs text-gray-500">
                <span class="inline-flex items-center gap-1 px-2 py-1 rounded bg-indigo-900/30 text-indigo-300 border border-indigo-700/30">
                    ✅ Turnstile {"activé" if turnstile_enabled else "désactivé"}
                </span>
                <span class="inline-flex items-center gap-1 px-2 py-1 rounded bg-gray-700/30 text-gray-300">
                    🛡️ Honeypot actif
                </span>
            </div>
            <button class="mt-4 w-full py-2 rounded-xl bg-indigo-600 text-white text-sm font-medium hover:bg-indigo-500 transition-colors"
                    onclick="navigator.clipboard.writeText(`{embed_code}`); this.textContent='Copié !'; setTimeout(()=>this.textContent='Copier le code', 2000)">
                Copier le code
            </button>
        </div>
    </div>
    """)


@app.get("/api/usage")
def get_usage(request: Request, db: Session = Depends(get_db)):
    """HTMX: charge les stats d'usage (soumissions utilisées / limite)."""
    user = get_current_user_from_request(request, db)
    if not user:
        return HTMLResponse("")

    forms = FORMS_DB.get(user.id, [])
    total_subs = sum(f.get("submissions", 0) for f in forms)
    total_forms = len(forms)

    sub = db.query(Subscription).filter(Subscription.user_id == user.id).first()
    plan_slug = sub.plan.slug if sub and sub.plan else "free"
    limits = {"free": 50, "starter": 500, "pro": 3000, "scale": 15000, "business": 10000}
    limit = limits.get(plan_slug, 50)

    pct = min(int((total_subs / limit) * 100), 100)
    bar_color = "bg-green-500" if pct < 50 else "bg-yellow-500" if pct < 80 else "bg-red-500"

    return HTMLResponse(f"""
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="bg-gray-800/50 rounded-xl p-5 border border-gray-700">
            <p class="text-gray-400 text-sm">Soumissions</p>
            <p class="text-white text-2xl font-bold mt-1">{total_subs} <span class="text-gray-500 text-sm font-normal">/ {limit}</span></p>
            <div class="w-full bg-gray-700 rounded-full h-2 mt-2">
                <div class="{bar_color} h-2 rounded-full transition-all duration-500" style="width: {pct}%"></div>
            </div>
        </div>
        <div class="bg-gray-800/50 rounded-xl p-5 border border-gray-700">
            <p class="text-gray-400 text-sm">Formulaires</p>
            <p class="text-white text-2xl font-bold mt-1">{total_forms}</p>
        </div>
        <div class="bg-gray-800/50 rounded-xl p-5 border border-gray-700">
            <p class="text-gray-400 text-sm">Plan actuel</p>
            <p class="text-white text-xl font-bold mt-1 capitalize">{plan_slug}</p>
        </div>
    </div>
    """)


@app.post("/api/forms/create")
async def create_form(request: Request, db: Session = Depends(get_db)):
    """HTMX: crée un nouveau formulaire."""
    user = get_current_user_from_request(request, db)
    if not user:
        return HTMLResponse("Non connecté", status_code=401)

    import uuid
    form_data = await request.form()
    form_name = form_data.get("name", "").strip()
    if not form_name:
        return HTMLResponse('<p class="text-red-400 text-sm mt-2">Le nom est requis</p>')

    form_id = str(uuid.uuid4())[:8]
    endpoint = f"f-{form_id}"

    if user.id not in FORMS_DB:
        FORMS_DB[user.id] = []

    FORMS_DB[user.id].append({
        "id": form_id,
        "name": form_name,
        "endpoint": endpoint,
        "submissions": 0,
        "submissions_data": [],
        "spam_protection_enabled": True,
        "turnstile_enabled": True,
        "spam_scoring_enabled": True,
    })

    return HTMLResponse(
        '<p class="text-green-400 text-sm mt-2">Formulaire créé avec succès !</p>'
    )


@app.get("/api/forms/count")
def get_form_count(request: Request, db: Session = Depends(get_db)):
    """HTMX: met à jour le compteur après création."""
    user = get_current_user_from_request(request, db)
    if not user:
        return HTMLResponse("0")
    return HTMLResponse(str(len(FORMS_DB.get(user.id, []))))


@app.get("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response


# ─── Public form submission endpoint ─────────────────────────────────────────


@app.post("/api/f/{endpoint}")
@limiter.limit(settings.SPAM_IP_RATE_LIMIT)
async def submit_form(endpoint: str, request: Request):
    """Endpoint public de soumission de formulaire.
    Accepte form-urlencoded, valide via anti-spam pipeline, stocke et retourne une confirmation.
    """
    import uuid
    from fastapi.responses import JSONResponse
    import json
    from datetime import datetime, timezone
    import time as time_module

    request_start = time_module.time()

    # Trouver le formulaire par endpoint
    form = None
    owner_id = None
    for uid, forms in FORMS_DB.items():
        for f in forms:
            if f["endpoint"] == endpoint:
                form = f
                owner_id = uid
                break
        if form:
            break

    if not form:
        return JSONResponse(
            {"success": False, "error": "Formulaire introuvable"},
            status_code=404,
        )

    # Anti-spam: disabled at form level → skip entirely
    spam_enabled = form.get("spam_protection_enabled", True)
    turnstile_enabled = form.get("turnstile_enabled", True) if spam_enabled else False
    scoring_enabled = form.get("spam_scoring_enabled", True) if spam_enabled else False

    # Parse form data
    raw = await request.form()
    raw_dict = dict(raw)

    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "")
    submit_duration_ms = int((time_module.time() - request_start) * 1000)

    if spam_enabled:
        from app.core.antispam import evaluate_submission

        turnstile_token = raw_dict.pop("cf-turnstile-response", None)

        verdict = await evaluate_submission(
            form_data=raw_dict,
            ip=client_ip,
            user_agent=user_agent,
            request_body=raw_dict,
            turnstile_token=turnstile_token,
            submit_duration_ms=submit_duration_ms,
            spam_scoring_enabled=scoring_enabled,
            turnstile_enabled=turnstile_enabled,
        )

        if not verdict["allowed"]:
            # Log spam rejection to form metadata
            if "spam_log" not in form:
                form["spam_log"] = []
            form["spam_log"].append({
                "reason": verdict["reason"],
                "score": verdict["score"],
                "signals": verdict["signals"][:3],
                "ip": client_ip,
                "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            })
            # Keep only last 100 entries
            form["spam_log"] = form["spam_log"][-100:]

            return JSONResponse(
                {"success": False, "error": "Submission rejected by anti-spam filters"},
                status_code=429,
            )
    else:
        # Even without anti-spam, still strip _gotcha
        raw_dict.pop("_gotcha", None)

    # Stocker la soumission
    submission = {
        "id": str(uuid.uuid4())[:8],
        "data": {k: v for k, v in raw_dict.items() if not k.startswith("_")},
        "ip": client_ip,
        "ua": user_agent[:120] if user_agent else "",
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
    }
    form["submissions_data"].append(submission)
    form["submissions"] = len(form["submissions_data"])

    return JSONResponse({
        "success": True,
        "message": "Formulaire soumis avec succès",
        "id": submission["id"],
    })


@app.post("/api/forms/{form_id}/delete")
def delete_form(form_id: str, request: Request, db: Session = Depends(get_db)):
    """HTMX: supprime un formulaire."""
    user = get_current_user_from_request(request, db)
    if not user:
        return HTMLResponse("Non connecté", status_code=401)

    forms = FORMS_DB.get(user.id, [])
    form = next((f for f in forms if f["id"] == form_id), None)
    if not form:
        return HTMLResponse('<p class="text-red-400">Formulaire introuvable</p>')

    FORMS_DB[user.id] = [f for f in forms if f["id"] != form_id]
    return HTMLResponse(
        '<p class="text-green-400 text-sm">Formulaire supprimé.</p>'
        '<script>setTimeout(() => htmx.trigger("#forms-list", "formCreated"), 100)</script>'
    )
