"""Shared test fixtures for ICAET MCP tests."""

from unittest.mock import MagicMock

import pytest

from icsaet_mcp.config import get_settings


@pytest.fixture
def mock_settings():
    """Create mock settings for testing."""
    settings = MagicMock()
    settings.icaet_api_key = "test-api-key-12345"
    settings.user_email = "test@example.com"
    return settings


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Set environment variables for testing."""
    monkeypatch.setenv("ICAET_API_KEY", "test-api-key-12345")
    monkeypatch.setenv("USER_EMAIL", "test@example.com")


@pytest.fixture(autouse=True)
def clear_settings_cache():
    """Clear settings cache before each test."""
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()
