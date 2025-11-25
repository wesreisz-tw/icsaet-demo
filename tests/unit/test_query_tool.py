"""Unit tests for MCP query tool."""

import json
from unittest.mock import MagicMock, patch

from pydantic import ValidationError

from icsaet_mcp.tools import query_icaet


def call_query_tool(question: str) -> str:
    """Helper to call the underlying tool function."""
    return query_icaet.fn(question)


class TestQueryTool:
    """Tests for query_icaet tool function."""

    @patch("icsaet_mcp.tools.get_settings")
    @patch("icsaet_mcp.tools.ICAETClient")
    def test_query_success(self, mock_client_class, mock_get_settings):
        """Test successful query returns JSON-formatted response."""
        # Arrange
        mock_settings = MagicMock()
        mock_get_settings.return_value = mock_settings
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        expected_result = {"answer": "Test answer", "sources": []}
        mock_client.query.return_value = expected_result

        # Act
        result = call_query_tool("What is ICAET?")

        # Assert
        assert json.loads(result) == expected_result
        mock_client.query.assert_called_once_with("What is ICAET?")

    def test_query_empty_question(self):
        """Test empty question returns error message."""
        # Act
        result = call_query_tool("")

        # Assert
        assert "Error" in result
        assert "empty" in result.lower()

    def test_query_whitespace_question(self):
        """Test whitespace-only question returns error message."""
        # Act
        result = call_query_tool("   ")

        # Assert
        assert "Error" in result
        assert "empty" in result.lower()

    @patch("icsaet_mcp.tools.get_settings")
    def test_query_config_error(self, mock_get_settings):
        """Test configuration error returns helpful setup message."""
        # Arrange
        mock_get_settings.side_effect = ValidationError.from_exception_data(
            "Settings", []
        )

        # Act
        result = call_query_tool("What is ICAET?")

        # Assert
        assert "Configuration error" in result
        assert "ICAET_API_KEY" in result
        assert "USER_EMAIL" in result

    @patch("icsaet_mcp.tools.get_settings")
    @patch("icsaet_mcp.tools.ICAETClient")
    def test_query_api_error(self, mock_client_class, mock_get_settings):
        """Test API error message is propagated."""
        # Arrange
        mock_settings = MagicMock()
        mock_get_settings.return_value = mock_settings
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_client.query.side_effect = RuntimeError("ICAET API request timed out.")

        # Act
        result = call_query_tool("What is ICAET?")

        # Assert
        assert "timed out" in result

    def test_tool_metadata(self):
        """Test tool has correct name and description."""
        # Assert
        from icsaet_mcp.tools import mcp

        tools = mcp._tool_manager._tools
        assert "query" in tools
        tool = tools["query"]
        assert "ICAET" in tool.description or "knowledge base" in tool.description
