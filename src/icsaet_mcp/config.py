"""Configuration management using Pydantic Settings."""

from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Requires ICAET_API_KEY and USER_EMAIL environment variables to be set.
    These are provided by Cursor IDE through MCP configuration.
    """

    model_config = SettingsConfigDict(case_sensitive=False)

    icaet_api_key: str
    user_email: str

    @field_validator("icaet_api_key")
    @classmethod
    def validate_api_key(cls, v: str) -> str:
        """Validate API key is not empty or whitespace."""
        if not v or not v.strip():
            raise ValueError(
                "ICAET_API_KEY cannot be empty. "
                "Set it in your Cursor MCP configuration."
            )
        return v

    @field_validator("user_email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Validate email is not empty and contains @."""
        if not v or not v.strip():
            raise ValueError(
                "USER_EMAIL cannot be empty. "
                "Set it in your Cursor MCP configuration."
            )
        if "@" not in v:
            raise ValueError(
                "USER_EMAIL must be a valid email address (must contain @)."
            )
        return v


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance.

    Returns:
        Settings instance loaded from environment variables.

    Raises:
        ValidationError: If required environment variables are missing or invalid.
    """
    return Settings()
