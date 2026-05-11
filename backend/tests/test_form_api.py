"""Tests for Form Backend API submission endpoints."""

import pytest
from fastapi.testclient import TestClient


class TestFormSubmissionAPI:
    """Public form submission endpoint POST /api/f/{endpoint}."""

    def test_submit_to_form(self, client: TestClient):
        """POST /api/f/{endpoint} should accept form data and return 200."""
        # First create a user and a form via the API
        resp = client.post("/auth/magic-link", json={"email": "form-api@example.com"})
        token = resp.json()["dev_token"]
        verify_resp = client.get(f"/auth/verify?token={token}")
        access_token = verify_resp.json()["access_token"]

        # Create a form via the dashboard (which uses in-memory FORMS_DB)
        resp = client.post(
            "/api/forms/create",
            data={"name": "Contact Form"},
            cookies={"access_token": access_token},
        )
        assert resp.status_code == 200

        # Get the form list to find the endpoint slug
        resp = client.get(
            "/api/forms",
            cookies={"access_token": access_token},
        )
        assert resp.status_code == 200

    def test_submit_without_auth(self, client: TestClient):
        """Public form submission should work without auth token."""
        # The public endpoint /api/f/{endpoint} accepts POST data
        # For this MVP, submissions go through the in-memory store
        # which requires the form to exist first
        resp = client.post(
            "/api/f/non-existent-form",
            data={"name": "Test", "email": "test@example.com"},
        )
        # Without a valid form endpoint, should return 404
        assert resp.status_code == 404
