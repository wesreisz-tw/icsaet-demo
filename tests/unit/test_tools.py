"""Unit tests for MCP tools."""

from unittest.mock import MagicMock, patch

import httpx
import pytest
from pydantic import ValidationError

from icsaet_mcp.tools import ICAETClient, query_icaet


def test_query_with_valid_question():
    """Arrange: Valid question and mocked successful API response
    Act: Call query tool
    Assert: Returns answer from API response"""
    with (
        patch("icsaet_mcp.tools.get_settings") as mock_settings,
        patch("httpx.Client") as mock_client,
    ):
        mock_settings.return_value = MagicMock(
            icaet_api_key="test-key",
            user_email="test@example.com",
        )
        mock_response = MagicMock()
        mock_response.json.return_value = {"answer": "Test answer"}
        mock_client.return_value.post.return_value = mock_response

        result = query_icaet("What did Leslie talk about?")

        assert result == "Test answer"


def test_query_with_empty_question():
    """Arrange: Empty question string
    Act: Call query tool
    Assert: Raises ValueError with helpful message"""
    with pytest.raises(ValueError) as exc_info:
        query_icaet("")

    assert "cannot be empty" in str(exc_info.value)


def test_query_with_whitespace_question():
    """Arrange: Whitespace-only question
    Act: Call query tool
    Assert: Raises ValueError"""
    with pytest.raises(ValueError) as exc_info:
        query_icaet("   ")

    assert "cannot be empty" in str(exc_info.value)


def test_query_with_missing_configuration():
    """Arrange: Missing environment variables (ValidationError from settings)
    Act: Call query tool
    Assert: Raises RuntimeError with configuration guidance"""
    with patch("icsaet_mcp.tools.get_settings") as mock_settings:
        mock_settings.side_effect = ValidationError.from_exception_data(
            "Settings", [{"type": "missing", "loc": ("ICAET_API_KEY",), "input": {}}]
        )

        with pytest.raises(RuntimeError) as exc_info:
            query_icaet("test question")

        assert "Missing configuration" in str(exc_info.value)
        assert "ICAET_API_KEY" in str(exc_info.value)


def test_query_with_api_timeout():
    """Arrange: API call times out
    Act: Call query tool
    Assert: Raises RuntimeError with timeout message"""
    with (
        patch("icsaet_mcp.tools.get_settings") as mock_settings,
        patch("httpx.Client") as mock_client,
    ):
        mock_settings.return_value = MagicMock(
            icaet_api_key="test-key",
            user_email="test@example.com",
        )
        mock_client.return_value.post.side_effect = httpx.TimeoutException("Timeout")

        with pytest.raises(RuntimeError) as exc_info:
            query_icaet("test question")

        assert "timed out" in str(exc_info.value).lower()


def test_query_with_401_error():
    """Arrange: API returns 401 Unauthorized
    Act: Call query tool
    Assert: Raises RuntimeError with authentication message"""
    with (
        patch("icsaet_mcp.tools.get_settings") as mock_settings,
        patch("httpx.Client") as mock_client,
    ):
        mock_settings.return_value = MagicMock(
            icaet_api_key="invalid-key",
            user_email="test@example.com",
        )
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_client.return_value.post.side_effect = httpx.HTTPStatusError(
            "Unauthorized", request=MagicMock(), response=mock_response
        )

        with pytest.raises(RuntimeError) as exc_info:
            query_icaet("test question")

        assert "Authentication failed" in str(exc_info.value)


def test_icaet_client_query_success():
    """Arrange: ICAETClient with valid settings and mocked successful response
    Act: Call client.query()
    Assert: Returns parsed JSON response"""
    settings = MagicMock(
        icaet_api_key="test-key",
        user_email="test@example.com",
    )

    with patch("httpx.Client") as mock_client:
        mock_response = MagicMock()
        mock_response.json.return_value = {"answer": "Test answer"}
        mock_client.return_value.post.return_value = mock_response

        client = ICAETClient(settings)
        result = client.query("test question")

        assert result == {"answer": "Test answer"}


def test_icaet_client_strips_whitespace():
    """Arrange: Question with leading/trailing whitespace
    Act: Call query tool
    Assert: Whitespace is stripped before API call"""
    with (
        patch("icsaet_mcp.tools.get_settings") as mock_settings,
        patch("httpx.Client") as mock_client,
    ):
        mock_settings.return_value = MagicMock(
            icaet_api_key="test-key",
            user_email="test@example.com",
        )
        mock_response = MagicMock()
        mock_response.json.return_value = {"answer": "Test"}
        mock_client.return_value.post.return_value = mock_response

        query_icaet("  test question  ")

        call_args = mock_client.return_value.post.call_args.kwargs
        assert call_args["json"]["question"] == "test question"
