"""Unit tests for configuration management."""

import pytest
from pydantic import ValidationError

from icsaet_mcp.config import Settings, get_settings


class TestSettings:
    """Tests for Settings class validation."""

    def test_settings_loads_with_valid_env_vars(self, monkeypatch):
        """Test Settings loads successfully with valid environment variables."""
        # Arrange
        monkeypatch.setenv("ICAET_API_KEY", "test-api-key-12345")
        monkeypatch.setenv("USER_EMAIL", "test@example.com")

        # Act
        settings = Settings()

        # Assert
        assert settings.icaet_api_key == "test-api-key-12345"
        assert settings.user_email == "test@example.com"

    def test_missing_api_key_raises_error(self, monkeypatch):
        """Test missing ICAET_API_KEY raises ValidationError."""
        # Arrange
        monkeypatch.delenv("ICAET_API_KEY", raising=False)
        monkeypatch.setenv("USER_EMAIL", "test@example.com")

        # Act & Assert
        with pytest.raises(ValidationError):
            Settings()

    def test_missing_email_raises_error(self, monkeypatch):
        """Test missing USER_EMAIL raises ValidationError."""
        # Arrange
        monkeypatch.setenv("ICAET_API_KEY", "test-api-key-12345")
        monkeypatch.delenv("USER_EMAIL", raising=False)

        # Act & Assert
        with pytest.raises(ValidationError):
            Settings()

    def test_empty_api_key_rejected(self, monkeypatch):
        """Test empty string API key is rejected."""
        # Arrange
        monkeypatch.setenv("ICAET_API_KEY", "")
        monkeypatch.setenv("USER_EMAIL", "test@example.com")

        # Act & Assert
        with pytest.raises(ValidationError, match="ICAET_API_KEY cannot be empty"):
            Settings()

    def test_whitespace_api_key_rejected(self, monkeypatch):
        """Test whitespace-only API key is rejected."""
        # Arrange
        monkeypatch.setenv("ICAET_API_KEY", "   ")
        monkeypatch.setenv("USER_EMAIL", "test@example.com")

        # Act & Assert
        with pytest.raises(ValidationError, match="ICAET_API_KEY cannot be empty"):
            Settings()

    def test_empty_email_rejected(self, monkeypatch):
        """Test empty string email is rejected."""
        # Arrange
        monkeypatch.setenv("ICAET_API_KEY", "test-api-key-12345")
        monkeypatch.setenv("USER_EMAIL", "")

        # Act & Assert
        with pytest.raises(ValidationError, match="USER_EMAIL cannot be empty"):
            Settings()

    def test_invalid_email_format_rejected(self, monkeypatch):
        """Test email without @ is rejected."""
        # Arrange
        monkeypatch.setenv("ICAET_API_KEY", "test-api-key-12345")
        monkeypatch.setenv("USER_EMAIL", "invalid-email")

        # Act & Assert
        with pytest.raises(ValidationError, match="must contain @"):
            Settings()


class TestGetSettings:
    """Tests for get_settings singleton pattern."""

    def test_get_settings_returns_same_instance(self, monkeypatch):
        """Test get_settings returns cached singleton instance."""
        # Arrange
        get_settings.cache_clear()
        monkeypatch.setenv("ICAET_API_KEY", "test-api-key-12345")
        monkeypatch.setenv("USER_EMAIL", "test@example.com")

        # Act
        settings1 = get_settings()
        settings2 = get_settings()

        # Assert
        assert settings1 is settings2

    def test_get_settings_returns_settings_instance(self, monkeypatch):
        """Test get_settings returns Settings instance."""
        # Arrange
        get_settings.cache_clear()
        monkeypatch.setenv("ICAET_API_KEY", "test-api-key-12345")
        monkeypatch.setenv("USER_EMAIL", "test@example.com")

        # Act
        settings = get_settings()

        # Assert
        assert isinstance(settings, Settings)
        assert settings.icaet_api_key == "test-api-key-12345"
        assert settings.user_email == "test@example.com"
