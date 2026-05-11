"""
Test configuration and fixtures for Monetization Lab backend.

IMPORTANT: Set environment variables BEFORE any app imports to ensure
config.py reads the test DB URL.
"""
import os
from unittest.mock import MagicMock, patch

TEST_DB_URL = "postgresql://monetization:monetization@localhost:5432/monetization_test"

os.environ.setdefault("DATABASE_URL", TEST_DB_URL)
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("SECRET_KEY", "test-secret-key-not-for-production")
os.environ.setdefault("DEBUG", "true")
os.environ.setdefault("ENVIRONMENT", "test")

import pytest
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.core.database import Base, get_db
from app.main import app


@pytest.fixture(autouse=True)
def mock_redis():
    """Mock Redis for all tests — patch get_redis() to return a fake client.

    This avoids needing a real Redis server running during tests.
    The mock client responds to ping() and basic Redis commands.
    """
    fake_redis = MagicMock()
    fake_redis.ping.return_value = True
    fake_redis.set.return_value = True
    fake_redis.get.return_value = None
    fake_redis.delete.return_value = 1
    fake_redis.exists.return_value = 0
    with patch("app.core.redis.get_redis", return_value=fake_redis):
        yield


@pytest.fixture(scope="session")
def db_engine():
    """Create test database engine."""
    engine = create_engine(TEST_DB_URL, pool_pre_ping=True)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(db_engine):
    """Create a fresh database session for each test with transaction rollback."""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(autocommit=False, autoflush=False, bind=connection)()
    yield session
    session.close()
    # Only rollback if the transaction is still active
    if transaction.is_active:
        transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session) -> Generator:
    """Test client with overridden DB dependency and mocked Redis."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    # Use a separate engine that doesn't trigger lifespan create_all
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
