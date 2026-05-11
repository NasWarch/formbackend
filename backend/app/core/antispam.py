"""Anti-spam MVP — Cloudflare Turnstile + rate limiting + behavioral scoring.

Architecture en 3 couches, testables indépendamment:
1. Turnstile — vérification côté serveur du token Cloudflare
2. Rate limiting — fingerprint IP + User-Agent, stocké dans Redis
3. Behavioral scoring — patterns, champs cachés, timing, contenu

Chaque couche peut être activée/désactivée indépendamment via les settings.
"""

import json
import re
import time
import hashlib
import ipaddress
from typing import Optional
from urllib.parse import urlparse

import httpx

from app.core.config import settings
from app.core.redis import get_redis


# ─── 1. Cloudflare Turnstile ─────────────────────────────────────────────────


TURNSTILE_VERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"


async def verify_turnstile_token(token: str, remote_ip: Optional[str] = None) -> bool:
    """Verify a Cloudflare Turnstile token server-side.

    In dev mode, the test key always passes.
    """
    if not token:
        return False

    # Test keys are always allowed in non-production environments
    if settings.ENVIRONMENT != "production":
        # Turnstile test keys: always passes
        if token == "1x0000000000000000000000000000000AA":
            return True
        # Always fails (for testing failure mode)
        if token == "2x0000000000000000000000000000000AA":
            return False

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.post(
                TURNSTILE_VERIFY_URL,
                data={
                    "secret": settings.TURNSTILE_SECRET_KEY,
                    "response": token,
                    "remoteip": remote_ip or "",
                },
            )
            result = resp.json()
            return result.get("success", False)
    except Exception:
        # Fail open if Turnstile is unreachable — don't break form submissions
        return True


# ─── 2. Rate Limiting (fingerprint-based) ────────────────────────────────────


def make_fingerprint(ip: str, user_agent: str) -> str:
    """Create a fingerprint hash from IP + normalized User-Agent."""
    raw = f"{ip}|{_normalize_ua(user_agent)}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def _normalize_ua(ua: str) -> str:
    """Normalize User-Agent to group similar browsers/scripts."""
    ua_lower = ua.lower()

    # Common bot patterns
    if "curl/" in ua_lower:
        return "curl"
    if "wget/" in ua_lower or "wget/" in ua_lower:
        return "wget"
    if "python-requests" in ua_lower:
        return "python-requests"
    if "go-http-client" in ua_lower:
        return "go-http-client"
    if "axios" in ua_lower:
        return "axios"
    if "postman" in ua_lower:
        return "postman"
    if "okhttp" in ua_lower:
        return "okhttp"
    if "ahrefssiteaudit" in ua_lower or "ahrefsbot" in ua_lower:
        return "ahrefs"
    if "googlebot" in ua_lower:
        return "googlebot"
    if "bingbot" in ua_lower:
        return "bingbot"

    # Browser — extract browser family
    if "firefox/" in ua_lower:
        return "firefox"
    if "chrome/" in ua_lower and "chromium" not in ua_lower:
        return "chrome"
    if "safari/" in ua_lower and "chrome" not in ua_lower:
        return "safari"

    # Non-browser or unknown
    if len(ua) < 30:
        return ua_lower[:30]
    return hashlib.md5(ua.encode()).hexdigest()[:12]


def is_private_ip(ip: str) -> bool:
    """Check if an IP is private (RFC 1918, localhost, etc.)."""
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback or addr.is_link_local
    except ValueError:
        return True  # Treat invalid IPs as private for safety


def check_rate_limit(
    ip: str,
    user_agent: str,
    redis_window: int = 60,
    ip_limit: int = 20,
    fingerprint_limit: int = 10,
) -> dict:
    """Check rate limits for a submission attempt.

    Two tiers:
    1. Per-IP (simple, catches broad abuse)
    2. Per-fingerprint (IP + UA hash, catches targeted scraping)

    Returns {"allowed": bool, "reason": str | None, "counts": {...}}
    """
    redis_client = get_redis()
    if redis_client is None:
        return {"allowed": True, "reason": None, "counts": {}}

    now = int(time.time())
    window_key = now // redis_window

    # Tier 1: Per-IP
    ip_key = f"rl:ip:{ip}:{window_key}"
    ip_count = redis_client.get(ip_key)
    ip_count = int(ip_count) if ip_count else 0

    # Tier 2: Per-fingerprint
    fp = make_fingerprint(ip, user_agent)
    fp_key = f"rl:fp:{fp}:{window_key}"
    fp_count = redis_client.get(fp_key)
    fp_count = int(fp_count) if fp_count else 0

    counts = {
        "ip_count": ip_count,
        "fp_count": fp_count,
        "window_seconds": redis_window,
    }

    if ip_count >= ip_limit:
        return {
            "allowed": False,
            "reason": f"IP rate limit exceeded ({ip_count}/{ip_limit})",
            "counts": counts,
        }

    if fp_count >= fingerprint_limit:
        return {
            "allowed": False,
            "reason": f"Fingerprint rate limit exceeded ({fp_count}/{fingerprint_limit})",
            "counts": counts,
        }

    # Increment counters
    redis_client.incr(ip_key)
    redis_client.expire(ip_key, redis_window * 2)

    redis_client.incr(fp_key)
    redis_client.expire(fp_key, redis_window * 2)

    counts["ip_count"] = ip_count + 1
    counts["fp_count"] = fp_count + 1
    return {"allowed": True, "reason": None, "counts": counts}


# ─── 3. Behavioral Scoring ──────────────────────────────────────────────────


SPAM_PATTERNS = {
    # Links in fields that shouldn't have them
    "link_in_name": re.compile(
        r"(https?://|www\.|bit\.ly|tinyurl|t\.co|shorturl|is\.gd)",
        re.IGNORECASE,
    ),
    # Suspicious TLD-only references (likely URLs without protocol)
    # Used only in name-field context (not general text scan — too noisy)
    "suspicious_tld_ref": re.compile(
        r"\b[\w\-]+\.(com|io|net|org)\b(?!@)",
        re.IGNORECASE,
    ),
    # Gibberish — repeated characters
    "gibberish_repeat": re.compile(r"(.)\1{4,}"),
    # All caps long text
    "all_caps": re.compile(r"^[A-Z][A-Z\s]{10,}$"),
    # Phone number spam pattern
    "phone_spam": re.compile(
        r"(\+?\d[\d\s\-\(\)]{7,}\d)|(\b(phone|call|contact)\s*(me|us|now)\b)",
        re.IGNORECASE,
    ),
    # SEO keyword stuffing
    "keyword_stuffing": re.compile(
        r"\b(buy|cheap|discount|free|click|subscribe|visit|offer|limited|act now)\b",
        re.IGNORECASE,
    ),
}

SPAM_TRIGGER_WORDS = [
    "seo services",
    "guest post",
    "link building",
    "digital marketing",
    "backlink",
    "content writing",
    "web design services",
    "social media marketing",
    "bulk email",
    "email list",
    "traffic generator",
    "rank your website",
    "website ranking",
    "affiliate marketing",
    "make money fast",
]


class SpamScore:
    """Container for a spam score evaluation result."""

    def __init__(self):
        self.score: int = 0
        self.signals: list[str] = []

    def add(self, points: int, signal: str) -> None:
        self.score += points
        self.signals.append(signal)

    @property
    def is_spam(self) -> bool:
        return self.score >= settings.SPAM_SCORE_THRESHOLD


def score_form_data(form_data: dict) -> SpamScore:
    """Evaluate form submission data for spam signals.

    Returns a SpamScore with:
    - score: cumulative integer score (higher = more likely spam)
    - signals: list of triggered signal descriptions
    - is_spam: True if score >= threshold
    """
    result = SpamScore()

    if not form_data:
        return result

    fields_text = " ".join(str(v).strip() for v in form_data.values() if v)
    all_field_values = list(form_data.values())

    # 1. Empty submission
    if not any(v and str(v).strip() for v in all_field_values):
        result.add(3, "empty_submission")
        return result

    # 2. Same value repeated in every field
    unique_values = set(str(v).strip().lower() for v in all_field_values if v)
    if len(unique_values) == 1 and len(all_field_values) > 1:
        result.add(4, "same_value_all_fields")

    # 3. Pattern-based checks
    for pattern_name, pattern in SPAM_PATTERNS.items():
        if pattern_name == "suspicious_tld_ref":
            continue  # Used only in name-field context, not general scan
        matches = pattern.findall(fields_text)
        if matches:
            if pattern_name == "link_in_name":
                # More links = higher score
                result.add(min(len(matches), 4), f"link_detected:{len(matches)}")
            elif pattern_name == "gibberish_repeat":
                result.add(2, "gibberish_repeated_chars")
            elif pattern_name == "all_caps":
                result.add(2, "all_caps_text")
            elif pattern_name == "phone_spam":
                result.add(4, "phone_spam_pattern")
            elif pattern_name == "keyword_stuffing":
                result.add(min(len(matches), 4), f"keyword_stuffing:{len(matches)}")

    # 4. Trigger words
    text_lower = fields_text.lower()
    for word in SPAM_TRIGGER_WORDS:
        if word in text_lower:
            result.add(2, f"trigger_word:{word}")
            break  # Only count once per batch of trigger words

    # 5. Too many fields (form field enumeration bots)
    if len(all_field_values) > 20:
        result.add(2, "too_many_fields")

    # 6. URL in non-message fields (e.g. name field with a URL)
    name_like_fields = [v for k, v in form_data.items()
                        if k.lower() in ("name", "first_name", "last_name", "subject", "company", "title")]
    for val in name_like_fields:
        if val and (SPAM_PATTERNS["link_in_name"].search(str(val))
                    or SPAM_PATTERNS["suspicious_tld_ref"].search(str(val))):
            result.add(4, "url_in_name_field")

    # 7. Repeated URLs across fields
    urls_found = set()
    for val in all_field_values:
        if val and isinstance(val, str):
            urls = re.findall(r"https?://[^\s]+", val)
            urls_found.update(urls)
    if len(urls_found) >= 3:
        result.add(3, "multiple_unique_urls")

    return result


def score_user_agent(ua: str) -> SpamScore:
    """Score User-Agent for known bot/crawler patterns."""
    result = SpamScore()
    if not ua:
        result.add(2, "missing_user_agent")
        return result

    ua_lower = ua.lower()

    # Known spam tools / headless browsers
    suspicious_uas = [
        "python-requests", "curl/", "wget", "go-http-client",
        "scrapy", "masscan", "zgrab", "python urllib",
    ]
    for pattern in suspicious_uas:
        if pattern in ua_lower:
            result.add(3, f"suspicious_ua:{pattern}")
            return result  # One match is enough for UA scoring

    # Empty or suspiciously short UA
    if len(ua) < 20:
        result.add(1, "short_user_agent")

    return result


def score_timing(submit_duration_ms: int) -> SpamScore:
    """Score submission timing.

    Bots submit forms instantly (< 1 second). Humans take time.
    """
    result = SpamScore()

    if submit_duration_ms < 500:
        result.add(3, "submitted_too_fast")
    elif submit_duration_ms < 1500:
        result.add(1, "submitted_fast")

    return result


# ─── 4. Combined Evaluation ─────────────────────────────────────────────────


async def evaluate_submission(
    form_data: dict,
    ip: str,
    user_agent: str,
    request_body: Optional[dict] = None,
    turnstile_token: Optional[str] = None,
    submit_duration_ms: int = 0,
    spam_scoring_enabled: bool = True,
    turnstile_enabled: bool = True,
) -> dict:
    """Run the full anti-spam pipeline on a submission.

    Returns a verdict dict:
    {
        "allowed": bool,
        "reason": str | None,
        "score": int,
        "signals": list[str],
        "turnstile_passed": bool | None,
        "rate_limit": {...} | None,
    }
    """
    result = {
        "allowed": True,
        "reason": None,
        "score": 0,
        "signals": [],
        "turnstile_passed": None,
        "rate_limited": False,
    }

    # Layer 1: Honeypot (always active, no cost)
    honeypot_value = None
    if request_body:
        honeypot_value = request_body.pop("_gotcha", None)
    elif form_data:
        honeypot_value = form_data.pop("_gotcha", None)

    if honeypot_value:
        result["allowed"] = False
        result["reason"] = "Honeypot triggered"
        result["signals"].append("honeypot_triggered")
        return result

    # Layer 2: Turnstile (configurable per-form)
    if turnstile_enabled:
        turnstile_ok = await verify_turnstile_token(turnstile_token or "", ip)
        result["turnstile_passed"] = turnstile_ok
        if not turnstile_ok:
            result["allowed"] = False
            result["reason"] = "Turnstile verification failed"
            result["signals"].append("turnstile_failed")
            return result

    # Layer 3: Rate limiting (always active for public endpoint)
    rl_result = check_rate_limit(
        ip=ip,
        user_agent=user_agent,
        redis_window=settings.SPAM_RATE_LIMIT_WINDOW,
        ip_limit=settings.SPAM_RATE_LIMIT_MAX,
        fingerprint_limit=settings.SPAM_RATE_LIMIT_MAX,
    )
    if not rl_result["allowed"]:
        result["allowed"] = False
        result["reason"] = rl_result["reason"]
        result["rate_limited"] = True
        result["signals"].append("rate_limited")
        return result

    # Layer 4: Behavioral scoring (can be disabled per-form or globally)
    if spam_scoring_enabled:
        ua_score = score_user_agent(user_agent)
        timing_score = score_timing(submit_duration_ms)
        data_score = score_form_data(form_data)

        total_score = ua_score.score + timing_score.score + data_score.score

        result["score"] = total_score
        result["signals"] = ua_score.signals + timing_score.signals + data_score.signals

        if total_score >= settings.SPAM_SCORE_THRESHOLD:
            result["allowed"] = False
            result["reason"] = f"Spam score exceeded threshold ({total_score}/{settings.SPAM_SCORE_THRESHOLD})"

    return result
