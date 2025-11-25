"""MCP tool definitions for ICAET queries."""

import logging
from typing import Any, cast

import httpx
from fastmcp import FastMCP
from pydantic import ValidationError

from icsaet_mcp.config import Settings, get_settings

logger = logging.getLogger(__name__)
mcp = FastMCP("icsaet")


class ICAETClient:
    """Client for interacting with ICAET API."""

    BASE_URL = "https://icaet-dev.wesleyreisz.com"

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._client = httpx.Client(timeout=30.0, base_url=self.BASE_URL)

    def query(self, question: str) -> dict[str, Any]:
        """Query the ICAET knowledge base."""
        headers = {"x-api-key": self.settings.icaet_api_key}
        payload = {"email": self.settings.user_email, "question": question}

        try:
            response = self._client.post("/query", json=payload, headers=headers)
            response.raise_for_status()
            return cast(dict[str, Any], response.json())
        except httpx.TimeoutException as e:
            logger.error(f"Request timeout: {e}")
            raise RuntimeError(
                "Request timed out. The ICAET API is taking too long to respond."
            ) from e
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code}: {e}")
            if e.response.status_code == 401:
                raise RuntimeError(
                    "Authentication failed. Please check your ICAET_API_KEY."
                ) from e
            elif e.response.status_code == 400:
                raise RuntimeError(
                    "Invalid request. Please check your question format and email."
                ) from e
            else:
                raise RuntimeError(
                    f"API error: {e.response.status_code}. Please try again later."
                ) from e
        except httpx.RequestError as e:
            logger.error(f"Network error: {e}")
            raise RuntimeError(
                "Network error. Please check your internet connection."
            ) from e


def query_icaet(question: str) -> str:
    """Query the ICAET knowledge base.

    Args:
        question: A natural language question about ICAET conference content,
                 speakers, topics, or sessions.

    Returns:
        Answer from the ICAET knowledge base.

    Raises:
        ValueError: If question is empty or invalid.
        RuntimeError: If API call fails or configuration is invalid.
    """
    if not question or not question.strip():
        raise ValueError("Question cannot be empty. Please provide a valid question.")

    try:
        settings = get_settings()
    except ValidationError as e:
        logger.error(f"Configuration error: {e}")
        raise RuntimeError(
            "Missing configuration. Please set ICAET_API_KEY and USER_EMAIL "
            "environment variables in your Cursor MCP settings."
        ) from e

    try:
        client = ICAETClient(settings)
        result = client.query(question.strip())

        if isinstance(result, dict) and "answer" in result:
            return cast(str, result["answer"])
        elif isinstance(result, dict):
            return str(result)
        else:
            return str(result)

    except RuntimeError:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise RuntimeError(
            f"An unexpected error occurred: {str(e)}. Please try again."
        ) from e


@mcp.tool()
def query(question: str) -> str:
    """Query the ICAET knowledge base.

    Args:
        question: A natural language question about ICAET conference content,
                 speakers, topics, or sessions.

    Returns:
        Answer from the ICAET knowledge base.
    """
    return query_icaet(question)


__all__ = ["mcp", "query", "query_icaet", "ICAETClient"]
