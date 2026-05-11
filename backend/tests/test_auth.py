"""Tests for auth endpoints: magic link flow and JWT verification."""

import pytest
from fastapi.testclient import TestClient


class TestMagicLinkFlow:
    """Magic link authentication flow."""

    def test_request_magic_link_creates_user(self, client: TestClient):
        """POST /auth/magic-link with a new email should create the user."""
        response = client.post("/auth/magic-link", json={"email": "test@example.com"})
        assert response.status_code == 200
        data = response.json()
        assert "dev_token" in data

    def test_request_magic_link_existing_user(self, client: TestClient):
        """POST /auth/magic-link with existing email should still return a token."""
        # First call creates
        client.post("/auth/magic-link", json={"email": "existing@example.com"})
        # Second call should also succeed
        response = client.post("/auth/magic-link", json={"email": "existing@example.com"})
        assert response.status_code == 200
        assert "dev_token" in response.json()

    def test_magic_link_invalid_email(self, client: TestClient):
        """POST /auth/magic-link with invalid email should return 400."""
        response = client.post("/auth/magic-link", json={"email": "not-an-email"})
        assert response.status_code == 400
        assert "email" in response.text.lower() or "invalid" in response.text.lower()

    def test_verify_magic_link_returns_tokens(self, client: TestClient):
        """GET /auth/verify?token=... should return access + refresh tokens."""
        # First get a magic link token
        resp = client.post("/auth/magic-link", json={"email": "verify@example.com"})
        token = resp.json()["dev_token"]

        # Then verify it
        response = client.get(f"/auth/verify?token={token}")
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_verify_expired_token(self, client: TestClient):
        """GET /auth/verify with expired/invalid token should return 400."""
        response = client.get("/auth/verify?token=invalid.token.here")
        assert response.status_code == 400

    def test_verify_missing_token(self, client: TestClient):
        """GET /auth/verify without token should return 422."""
        response = client.get("/auth/verify")
        assert response.status_code == 422


class TestRefreshToken:
    """Refresh token flow."""

    def test_refresh_returns_new_tokens(self, client: TestClient):
        """POST /auth/refresh with valid refresh token should return new tokens."""
        # Get initial tokens
        resp = client.post("/auth/magic-link", json={"email": "refresh@example.com"})
        token = resp.json()["dev_token"]
        verify_resp = client.get(f"/auth/verify?token={token}")
        refresh_token = verify_resp.json()["refresh_token"]

        # Refresh
        response = client.post("/auth/refresh", json={"refresh_token": refresh_token})
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data

    def test_refresh_with_invalid_token(self, client: TestClient):
        """POST /auth/refresh with invalid token should return 401."""
        response = client.post("/auth/refresh", json={"refresh_token": "garbage.token.here"})
        assert response.status_code == 401


class TestProtectedEndpoint:
    """Endpoints requiring authentication."""

    def test_get_me_without_token(self, client: TestClient):
        """GET /users/me without token should return 401."""
        response = client.get("/users/me")
        assert response.status_code == 401

    def test_get_me_with_valid_token(self, client: TestClient):
        """GET /users/me with valid token should return user info."""
        # Get token
        resp = client.post("/auth/magic-link", json={"email": "me@example.com"})
        token = resp.json()["dev_token"]
        verify_resp = client.get(f"/auth/verify?token={token}")
        access_token = verify_resp.json()["access_token"]

        # Access protected endpoint
        response = client.get(
            "/users/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "me@example.com"
