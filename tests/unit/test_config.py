"""Tests for configuration management."""

import pytest
from pydantic import ValidationError

from icsaet_mcp.config import Settings, get_settings


@pytest.fixture
def valid_env_vars(monkeypatch):
    """Set valid environment variables for testing."""
    monkeypatch.setenv("ICAET_API_KEY", "test_api_key_12345")
    monkeypatch.setenv("USER_EMAIL", "test@example.com")


@pytest.fixture(autouse=True)
def clear_settings_cache():
    """Clear settings cache after each test."""
    yield
    get_settings.cache_clear()


def test_settings_loads_with_valid_env_vars(valid_env_vars):
    """Arrange: Valid environment variables set
    Act: Create Settings instance
    Assert: Both fields populated correctly"""
    settings = Settings()
    assert settings.icaet_api_key == "test_api_key_12345"
    assert settings.user_email == "test@example.com"


def test_get_settings_returns_same_instance(valid_env_vars):
    """Arrange: Valid environment variables set
    Act: Call get_settings() twice
    Assert: Both returns are same object"""
    settings1 = get_settings()
    settings2 = get_settings()
    assert settings1 is settings2


def test_settings_accepts_valid_email_format(monkeypatch):
    """Arrange: Valid email with @ and .
    Act: Create Settings instance
    Assert: No exception raised"""
    monkeypatch.setenv("ICAET_API_KEY", "test_api_key_12345")
    monkeypatch.setenv("USER_EMAIL", "valid@email.com")
    settings = Settings()
    assert settings.user_email == "valid@email.com"


def test_missing_api_key_raises_validation_error(monkeypatch):
    """Arrange: Only USER_EMAIL set
    Act: Attempt to create Settings instance
    Assert: ValidationError raised"""
    monkeypatch.setenv("USER_EMAIL", "test@example.com")
    monkeypatch.delenv("ICAET_API_KEY", raising=False)
    with pytest.raises(ValidationError):
        Settings()


def test_missing_user_email_raises_validation_error(monkeypatch):
    """Arrange: Only ICAET_API_KEY set
    Act: Attempt to create Settings instance
    Assert: ValidationError raised"""
    monkeypatch.setenv("ICAET_API_KEY", "test_api_key_12345")
    monkeypatch.delenv("USER_EMAIL", raising=False)
    with pytest.raises(ValidationError):
        Settings()


def test_empty_api_key_rejected(monkeypatch):
    """Arrange: Empty ICAET_API_KEY
    Act: Attempt to create Settings instance
    Assert: ValidationError raised"""
    monkeypatch.setenv("ICAET_API_KEY", "")
    monkeypatch.setenv("USER_EMAIL", "test@example.com")
    with pytest.raises(ValidationError):
        Settings()


def test_empty_user_email_rejected(monkeypatch):
    """Arrange: Empty USER_EMAIL
    Act: Attempt to create Settings instance
    Assert: ValidationError raised"""
    monkeypatch.setenv("ICAET_API_KEY", "test_api_key_12345")
    monkeypatch.setenv("USER_EMAIL", "")
    with pytest.raises(ValidationError):
        Settings()


def test_invalid_email_format_rejected(monkeypatch):
    """Arrange: USER_EMAIL without @
    Act: Attempt to create Settings instance
    Assert: ValidationError raised with email format message"""
    monkeypatch.setenv("ICAET_API_KEY", "test_api_key_12345")
    monkeypatch.setenv("USER_EMAIL", "invalid_email")
    with pytest.raises(ValidationError, match="valid email format"):
        Settings()

