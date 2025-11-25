"""Configuration management for ICSAET MCP server."""

from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for ICSAET MCP server.

    Loads configuration from environment variables:
        ICAET_API_KEY: API key for ICAET authentication
        USER_EMAIL: User email for API requests
    """

    model_config = SettingsConfigDict(case_sensitive=False, extra="ignore")

    icaet_api_key: str = Field(
        ..., min_length=10, description="ICAET API key for authentication"
    )
    user_email: str = Field(
        ..., min_length=5, description="User email for API requests"
    )

    @field_validator("icaet_api_key")
    @classmethod
    def validate_api_key_not_empty(cls, v: str) -> str:
        """Validate API key is not empty after stripping whitespace."""
        if not v.strip():
            raise ValueError("ICAET_API_KEY cannot be empty")
        return v

    @field_validator("user_email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        """Validate email contains @ and . characters."""
        if "@" not in v or "." not in v:
            raise ValueError(
                "USER_EMAIL must be a valid email format (contain @ and .)"
            )
        return v


@lru_cache
def get_settings() -> Settings:
    """Get cached Settings instance (singleton pattern).

    Returns the same Settings instance on every call to avoid
    reloading environment variables multiple times.

    Returns:
        Settings: Cached settings instance
    """
    return Settings()
