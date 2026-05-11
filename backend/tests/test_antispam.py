"""Tests for the anti-spam MVP module.

Tests are organized in 4 layers matching the pipeline:
1. Behavioral scoring (unit)
2. User-Agent scoring (unit)
3. Turnstile verification (unit with mock)
4. Full pipeline integration (end-to-end with mocked Redis)
"""
import os
from unittest.mock import patch, MagicMock, AsyncMock

import pytest

from app.core.antispam import (
    score_form_data,
    score_user_agent,
    score_timing,
    SpamScore,
    make_fingerprint,
    verify_turnstile_token,
    check_rate_limit,
    evaluate_submission,
)


# ─── Layer 1: Behavioral Scoring ──────────────────────────────────────────────


class TestScoreFormData:
    """Unit tests for score_form_data — evaluates form field content for spam."""

    def test_clean_submission_scores_zero(self):
        """A normal form submission should score 0."""
        data = {"name": "Jean Dupont", "email": "jean@example.com", "message": "Bonjour, une question sur vos tarifs."}
        result = score_form_data(data)
        assert result.score == 0
        assert not result.is_spam
        assert result.signals == []

    def test_url_in_name_field_flagged(self):
        """A URL in the 'name' field should trigger url_in_name_field."""
        data = {"name": "Buy cheap at spam-store.com", "email": "test@test.com", "message": "hello"}
        result = score_form_data(data)
        assert result.score >= 5
        assert result.is_spam
        assert any("url_in_name_field" in s for s in result.signals)

    def test_obvious_http_url_flagged(self):
        """Obvious http/https links in any field should be flagged."""
        data = {"name": "SEO Services", "email": "spam@test.com", "message": "Click now! https://spam.example.com"}
        result = score_form_data(data)
        assert result.is_spam
        assert any("link_detected" in s for s in result.signals)

    def test_same_value_all_fields(self):
        """Same value repeated across all fields is suspicious."""
        data = {"name": "test", "email": "test", "message": "test", "subject": "test"}
        result = score_form_data(data)
        assert result.score == 4
        assert any("same_value_all_fields" in s for s in result.signals)

    def test_gibberish_repeated_chars(self):
        """Repeated characters (aaaaa) should be detected."""
        data = {"name": "aaaaaabbbbb", "email": "x@x.com", "message": "hello"}
        result = score_form_data(data)
        assert any("gibberish" in s for s in result.signals)

    def test_keyword_stuffing(self):
        """Known spam keywords should increase the score."""
        data = {"name": "John", "email": "x@x.com", "message": "Click now for free discount buy cheap!!! Limited offer guest post service", "subject": "amazing offer"}
        result = score_form_data(data)
        assert result.is_spam

    def test_phone_number_spam(self):
        """Phone numbers + call to action should be flagged."""
        data = {"name": "John", "email": "x@x.com", "message": "Call +33612345678 now for the best offer!"}
        result = score_form_data(data)
        assert result.is_spam
        assert any("phone_spam" in s for s in result.signals)

    def test_empty_submission(self):
        """Empty or whitespace-only submission gets a base score."""
        data = {"name": "", "email": "", "message": ""}
        result = score_form_data(data)
        assert result.score == 3
        assert any("empty" in s for s in result.signals)

    def test_trigger_words_detected(self):
        """SEO trigger words should be detected."""
        data = {"name": "SEO Expert", "email": "x@x.com", "message": "I offer guest post and link building services"}
        result = score_form_data(data)
        assert any("trigger_word" in s for s in result.signals)

    def test_multiple_urls_across_fields(self):
        """Three or more unique URLs across fields should score higher."""
        data = {
            "name": "Check http://a.com and http://b.com",
            "email": "x@x.com",
            "message": "Also see https://c.com",
        }
        result = score_form_data(data)
        assert result.is_spam

    def test_email_in_message_not_flagged(self):
        """Email addresses should NOT trigger URL detection."""
        data = {"name": "Support", "email": "user@domain.com", "message": "Please contact me at my@email.com"}
        result = score_form_data(data)
        assert not result.is_spam


# ─── Layer 2: User-Agent Scoring ──────────────────────────────────────────────


class TestScoreUserAgent:
    """Unit tests for User-Agent based spam scoring."""

    def test_browser_ua_zero_score(self):
        """Legitimate browser UAs should score 0."""
        result = score_user_agent("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        assert result.score == 0

    def test_curl_scores_high(self):
        """curl User-Agent should score high."""
        result = score_user_agent("curl/7.88.1")
        assert result.score >= 3
        assert any("suspicious_ua" in s for s in result.signals)

    def test_python_requests_scores_high(self):
        """python-requests User-Agent should score high."""
        result = score_user_agent("python-requests/2.31.0")
        assert result.score >= 3
        assert any("suspicious_ua" in s for s in result.signals)

    def test_empty_ua_scores(self):
        """Missing User-Agent should score."""
        result = score_user_agent("")
        assert result.score >= 2
        assert any("missing" in s for s in result.signals)

    def test_short_ua_scores_low(self):
        """Very short UAs should score minimal."""
        result = score_user_agent("CustomApp/1.0")
        assert result.score == 1
        assert any("short" in s for s in result.signals)


# ─── Layer 2.5: Timing Scoring ──────────────────────────────────────────────


class TestScoreTiming:
    def test_instant_submission_flagged(self):
        result = score_timing(100)  # 100ms
        assert result.score >= 3

    def test_fast_submission_flagged_light(self):
        result = score_timing(800)  # 800ms
        assert result.score == 1

    def test_normal_timing_zero(self):
        result = score_timing(5000)  # 5s
        assert result.score == 0


# ─── Layer 3: Rate Limiting ─────────────────────────────────────────────────


class TestMakeFingerprint:
    def test_same_ua_different_ips_different_fp(self):
        fp1 = make_fingerprint("1.2.3.4", "Mozilla/5.0 Firefox/120.0")
        fp2 = make_fingerprint("5.6.7.8", "Mozilla/5.0 Firefox/120.0")
        assert fp1 != fp2

    def test_same_ip_diff_normalized_ua_same_fp(self):
        fp1 = make_fingerprint("1.2.3.4", "Mozilla/5.0 Firefox/120.0")
        fp2 = make_fingerprint("1.2.3.4", "Mozilla/5.0 (X11) Firefox/120.0")
        assert fp1 == fp2

    def test_curl_normalized(self):
        fp = make_fingerprint("1.2.3.4", "curl/8.0.1")
        assert len(fp) == 16


class TestCheckRateLimit:
    def test_allowed_when_no_redis(self):
        """Without Redis, rate limiter should allow by default."""
        from app.core.antispam import get_redis
        with patch("app.core.antispam.get_redis", return_value=None):
            result = check_rate_limit("1.2.3.4", "Mozilla/5.0", 60, 5, 5)
        assert result["allowed"] is True

    def test_blocked_after_limit_ip(self):
        """After hitting IP limit, should block."""
        mock_redis = MagicMock()
        mock_redis.get.return_value = 20  # Already at limit
        with patch("app.core.antispam.get_redis", return_value=mock_redis):
            result = check_rate_limit("1.2.3.4", "Mozilla/5.0", 60, 10, 10)
        assert result["allowed"] is False
        assert "IP rate limit" in result["reason"]


# ─── Layer 4: Turnstile ─────────────────────────────────────────────────────


class TestVerifyTurnstileToken:
    @pytest.mark.asyncio
    async def test_test_key_passes_in_dev(self):
        """The Turnstile test key should always pass in non-production."""
        result = await verify_turnstile_token("1x0000000000000000000000000000000AA")
        assert result is True

    @pytest.mark.asyncio
    async def test_test_fail_key_fails(self):
        """The Turnstile always-fail key should always fail."""
        os.environ["ENVIRONMENT"] = "development"
        result = await verify_turnstile_token("2x0000000000000000000000000000000AA")
        assert result is False

    @pytest.mark.asyncio
    async def test_empty_token_fails(self):
        """Empty token should fail verification."""
        result = await verify_turnstile_token("")
        assert result is False


# ─── Full Pipeline ──────────────────────────────────────────────────────────


class TestEvaluateSubmission:
    @pytest.mark.asyncio
    async def test_honeypot_triggers_first(self):
        """Honeypot field should be checked before anything else."""
        result = await evaluate_submission(
            form_data={},
            ip="1.2.3.4",
            user_agent="Mozilla/5.0",
            request_body={"_gotcha": "anything"},
        )
        assert result["allowed"] is False
        assert "honeypot" in result["reason"].lower()

    @pytest.mark.asyncio
    async def test_turnstile_disabled_skips_layer(self):
        """When turnstile is disabled, it shouldn't block."""
        result = await evaluate_submission(
            form_data={"name": "Test"},
            ip="1.2.3.4",
            user_agent="Mozilla/5.0",
            turnstile_enabled=False,
        )
        assert result["turnstile_passed"] is None

    @pytest.mark.asyncio
    async def test_clean_submission_passes_all_layers(self):
        """A clean submission should pass all anti-spam layers."""
        with patch("app.core.antispam.get_redis", return_value=None):
            result = await evaluate_submission(
                form_data={"name": "Jean", "email": "jean@example.com", "message": "Hello"},
                ip="1.2.3.4",
                user_agent="Mozilla/5.0 Firefox/120.0",
                turnstile_token="1x0000000000000000000000000000000AA",
                turnstile_enabled=True,
                spam_scoring_enabled=True,
                submit_duration_ms=5000,
            )
        assert result["allowed"] is True
        assert result["turnstile_passed"] is True

    @pytest.mark.asyncio
    async def test_spam_scoring_blocks(self):
        """Obvious spam should be blocked by scoring."""
        with patch("app.core.antispam.get_redis", return_value=None):
            result = await evaluate_submission(
                form_data={"name": "Buy cheap SEO https://spam.com", "email": "x@x.com", "message": "click now!"},
                ip="1.2.3.4",
                user_agent="Mozilla/5.0 Firefox/120.0",
                turnstile_token="1x0000000000000000000000000000000AA",
                spam_scoring_enabled=True,
                turnstile_enabled=True,
            )
        assert result["allowed"] is False
        assert "spam score" in result["reason"].lower()
