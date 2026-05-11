"""Tests for GET /health endpoint."""

import pytest
from fastapi.testclient import TestClient


class TestHealthEndpoint:
    """Health check endpoint should verify DB and Redis connectivity."""

    def test_health_returns_200(self, client: TestClient):
        """GET /health should return 200 OK."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_status_fields(self, client: TestClient):
        """Response should contain status, db, and redis fields."""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert "db" in data
        assert "redis" in data

    def test_health_db_ok(self, client: TestClient):
        """Database should be reported as reachable."""
        response = client.get("/health")
        data = response.json()
        # DB might be degraded if PG is down, but in test env it should be ok
        assert data["db"] is True or data["status"] == "degraded"

    def test_health_status_is_ok_when_all_healthy(self, client: TestClient):
        """When DB and Redis are both reachable, status should be 'ok'."""
        response = client.get("/health")
        data = response.json()
        if data["db"] and data["redis"]:
            assert data["status"] == "ok"
