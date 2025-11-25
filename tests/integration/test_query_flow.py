"""Integration tests for full query flow."""

from unittest.mock import MagicMock, patch

import httpx
import pytest

from icsaet_mcp.tools import query_icaet


@pytest.mark.integration
def test_full_query_flow_with_valid_config(monkeypatch):
    """Arrange: Valid environment variables and mocked API response
    Act: Call query tool through full stack
    Assert: Returns answer from API"""
    monkeypatch.setenv("ICAET_API_KEY", "test-api-key-12345")
    monkeypatch.setenv("USER_EMAIL", "test@example.com")

    with patch("httpx.Client") as mock_client:
        mock_response = MagicMock()
        mock_response.json.return_value = {"answer": "Integration test answer"}
        mock_client.return_value.post.return_value = mock_response

        from icsaet_mcp.config import get_settings

        get_settings.cache_clear()

        result = query_icaet("What is ICAET?")

        assert result == "Integration test answer"
        mock_client.return_value.post.assert_called_once()


@pytest.mark.integration
def test_full_query_flow_with_missing_config():
    """Arrange: Missing environment variables
    Act: Call query tool
    Assert: Raises RuntimeError with configuration guidance"""
    from icsaet_mcp.config import get_settings

    get_settings.cache_clear()

    with patch.dict("os.environ", {}, clear=True):
        with pytest.raises(RuntimeError) as exc_info:
            query_icaet("test question")

        assert "Missing configuration" in str(exc_info.value)
        assert "ICAET_API_KEY" in str(exc_info.value)


@pytest.mark.integration
def test_full_query_flow_with_api_error(monkeypatch):
    """Arrange: Valid config but API returns error
    Act: Call query tool
    Assert: Raises RuntimeError with helpful message"""
    monkeypatch.setenv("ICAET_API_KEY", "test-key-12345")
    monkeypatch.setenv("USER_EMAIL", "test@example.com")

    with patch("httpx.Client") as mock_client:
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_client.return_value.post.side_effect = httpx.HTTPStatusError(
            "Server error", request=MagicMock(), response=mock_response
        )

        from icsaet_mcp.config import get_settings

        get_settings.cache_clear()

        with pytest.raises(RuntimeError) as exc_info:
            query_icaet("test question")

        assert "API error" in str(exc_info.value)


@pytest.mark.integration
def test_server_startup_validation(monkeypatch):
    """Arrange: Valid configuration environment
    Act: Import server module
    Assert: Server initializes without errors"""
    monkeypatch.setenv("ICAET_API_KEY", "test-key")
    monkeypatch.setenv("USER_EMAIL", "test@example.com")

    from icsaet_mcp.server import mcp

    assert mcp is not None
    assert mcp.name == "icsaet"


@pytest.mark.integration
def test_prompt_content_integration():
    """Arrange: Server with registered prompts
    Act: Call each prompt function
    Assert: All prompts return substantial content"""
    from icsaet_mcp.server import (
        get_example_questions,
        get_formatting_guidance,
        get_icaet_overview,
    )

    overview = get_icaet_overview()
    examples = get_example_questions()
    guidance = get_formatting_guidance()

    assert len(overview) > 200
    assert len(examples) > 200
    assert len(guidance) > 200

    assert "ICAET" in overview
    assert "question" in examples.lower()
    assert "tip" in guidance.lower() or "do" in guidance.lower()

