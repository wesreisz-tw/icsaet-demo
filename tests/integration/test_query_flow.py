"""Integration tests for full query flow."""

import httpx
import respx

from icsaet_mcp.tools import BASE_URL, query_icaet


def call_query_tool(question: str) -> str:
    """Helper to call the underlying tool function."""
    return query_icaet.fn(question)


class TestQueryFlow:
    """Integration tests for end-to-end query flow."""

    @respx.mock
    def test_full_query_flow_success(self, mock_env_vars):
        """Test successful query through full stack."""
        # Arrange
        expected_response = {"answer": "Leslie talked about engineering leadership"}
        respx.post(f"{BASE_URL}/query").mock(
            return_value=httpx.Response(200, json=expected_response)
        )

        # Act
        result = call_query_tool("What did Leslie talk about?")

        # Assert
        assert "Leslie" in result or "leadership" in result

    def test_query_flow_missing_config(self, monkeypatch):
        """Test query with missing configuration returns error."""
        # Arrange
        monkeypatch.delenv("ICAET_API_KEY", raising=False)
        monkeypatch.delenv("USER_EMAIL", raising=False)

        # Act
        result = call_query_tool("What is ICAET?")

        # Assert
        assert "Configuration error" in result

    @respx.mock
    def test_query_flow_api_timeout(self, mock_env_vars):
        """Test timeout handling in query flow."""
        # Arrange
        respx.post(f"{BASE_URL}/query").mock(
            side_effect=httpx.TimeoutException("timeout")
        )

        # Act
        result = call_query_tool("What is ICAET?")

        # Assert
        assert "timed out" in result

    @respx.mock
    def test_query_flow_api_error(self, mock_env_vars):
        """Test API error handling in query flow."""
        # Arrange
        respx.post(f"{BASE_URL}/query").mock(
            return_value=httpx.Response(500, text="Internal Server Error")
        )

        # Act
        result = call_query_tool("What is ICAET?")

        # Assert
        assert "HTTP 500" in result

    @respx.mock
    def test_error_propagation(self, mock_env_vars):
        """Test errors propagate correctly through layers."""
        # Arrange
        respx.post(f"{BASE_URL}/query").mock(
            return_value=httpx.Response(401, text="Unauthorized")
        )

        # Act
        result = call_query_tool("What is ICAET?")

        # Assert
        assert "HTTP 401" in result
        assert "Unauthorized" in result


class TestEdgeCases:
    """Edge case tests for query flow."""

    @respx.mock
    def test_special_characters_in_question(self, mock_env_vars):
        """Test questions with special characters are handled."""
        # Arrange
        expected_response = {"answer": "Test answer"}
        respx.post(f"{BASE_URL}/query").mock(
            return_value=httpx.Response(200, json=expected_response)
        )

        # Act
        result = call_query_tool(
            "What about C++ & Python? <script>alert('test')</script>"
        )

        # Assert
        assert "Test answer" in result

    @respx.mock
    def test_long_question(self, mock_env_vars):
        """Test handling of long questions."""
        # Arrange
        long_question = "What " * 1000  # Very long question
        expected_response = {"answer": "Test answer"}
        respx.post(f"{BASE_URL}/query").mock(
            return_value=httpx.Response(200, json=expected_response)
        )

        # Act
        result = call_query_tool(long_question)

        # Assert
        assert "Test answer" in result
