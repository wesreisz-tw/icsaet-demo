"""MCP tool implementations for ICAET queries."""

import json
import logging
from typing import Any, cast

import httpx
from fastmcp import FastMCP
from pydantic import ValidationError

from icsaet_mcp.config import Settings, get_settings

logger = logging.getLogger(__name__)

BASE_URL = "https://icaet-dev.wesleyreisz.com"
TIMEOUT_SECONDS = 20.0

mcp = FastMCP("icsaet")


@mcp.tool(name="query", description="Query the ICAET knowledge base")
def query_icaet(question: str) -> str:
    """Query the ICAET knowledge base with a natural language question.

    Args:
        question: The question to ask the ICAET knowledge base.

    Returns:
        JSON-formatted response from the ICAET API.
    """
    if not question or not question.strip():
        return "Error: Please provide a question. The question cannot be empty."

    try:
        settings = get_settings()
        client = ICAETClient(settings)
        result = client.query(question)
        return json.dumps(result, indent=2)
    except ValidationError:
        return (
            "Configuration error: Please ensure ICAET_API_KEY and USER_EMAIL "
            "are set in your Cursor MCP configuration."
        )
    except RuntimeError as e:
        return str(e)
    except Exception:
        logger.exception("Unexpected error in query_icaet")
        return "An unexpected error occurred. Please try again."


class ICAETClient:
    """HTTP client for the ICAET API.

    Handles authentication, request/response processing, and error handling
    for queries to the ICAET knowledge base.
    """

    def __init__(self, settings: Settings) -> None:
        """Initialize the client with configuration settings.

        Args:
            settings: Application settings containing API credentials.
        """
        self.settings = settings

    def _mask_api_key(self, key: str) -> str:
        """Mask API key for safe logging.

        Args:
            key: The API key to mask.

        Returns:
            Masked key showing only last 4 characters.
        """
        if len(key) >= 4:
            return "***" + key[-4:]
        return "***"

    def query(self, question: str) -> dict[str, Any]:
        """Query the ICAET API with a question.

        Args:
            question: The question to ask the ICAET knowledge base.

        Returns:
            Parsed JSON response from the API.

        Raises:
            RuntimeError: If the API request fails for any reason.
        """
        masked_key = self._mask_api_key(self.settings.icaet_api_key)
        logger.info("Querying ICAET API (key: %s)", masked_key)
        logger.debug("Question length: %d chars", len(question))

        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.settings.icaet_api_key,
        }
        body = {
            "email": self.settings.user_email,
            "question": question,
        }

        try:
            with httpx.Client(timeout=TIMEOUT_SECONDS) as http_client:
                response = http_client.post(
                    f"{BASE_URL}/query", headers=headers, json=body
                )
                response.raise_for_status()
                return cast(dict[str, Any], response.json())
        except httpx.TimeoutException:
            logger.error("ICAET API request timed out")
            raise RuntimeError(
                "ICAET API request timed out. Please try again."
            ) from None
        except httpx.HTTPStatusError as e:
            logger.error("ICAET API returned HTTP %d", e.response.status_code)
            raise RuntimeError(
                f"ICAET API error (HTTP {e.response.status_code}): "
                f"{e.response.text or 'Unknown error'}"
            ) from None
        except httpx.RequestError as e:
            logger.error("Network error connecting to ICAET API: %s", str(e))
            raise RuntimeError(
                "Network error connecting to ICAET API. Check your connection."
            ) from None
