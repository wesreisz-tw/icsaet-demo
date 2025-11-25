"""Unit tests for ICAET API client."""

from unittest.mock import MagicMock

import httpx
import pytest
import respx

from icsaet_mcp.tools import BASE_URL, ICAETClient


@pytest.fixture
def mock_settings():
    """Create mock settings for testing."""
    settings = MagicMock()
    settings.icaet_api_key = "test-api-key-12345"
    settings.user_email = "test@example.com"
    return settings


@pytest.fixture
def client(mock_settings):
    """Create ICAETClient instance for testing."""
    return ICAETClient(mock_settings)


class TestICAETClient:
    """Tests for ICAETClient class."""

    @respx.mock
    def test_query_success(self, client):
        """Test successful query returns expected data."""
        # Arrange
        expected_response = {"answer": "Test answer", "sources": []}
        respx.post(f"{BASE_URL}/query").mock(
            return_value=httpx.Response(200, json=expected_response)
        )

        # Act
        result = client.query("What is ICAET?")

        # Assert
        assert result == expected_response

    @respx.mock
    def test_query_timeout_handled(self, client):
        """Test timeout exception is handled with user-friendly error."""
        # Arrange
        respx.post(f"{BASE_URL}/query").mock(
            side_effect=httpx.TimeoutException("timeout")
        )

        # Act & Assert
        with pytest.raises(RuntimeError, match="timed out"):
            client.query("Test question")

    @respx.mock
    def test_query_http_401_handled(self, client):
        """Test HTTP 401 error is handled with status code in message."""
        # Arrange
        respx.post(f"{BASE_URL}/query").mock(
            return_value=httpx.Response(401, text="Unauthorized")
        )

        # Act & Assert
        with pytest.raises(RuntimeError, match="HTTP 401"):
            client.query("Test question")

    @respx.mock
    def test_query_http_500_handled(self, client):
        """Test HTTP 500 error is handled correctly."""
        # Arrange
        respx.post(f"{BASE_URL}/query").mock(
            return_value=httpx.Response(500, text="Internal Server Error")
        )

        # Act & Assert
        with pytest.raises(RuntimeError, match="HTTP 500"):
            client.query("Test question")

    @respx.mock
    def test_query_network_error_handled(self, client):
        """Test network error is handled with user-friendly message."""
        # Arrange
        respx.post(f"{BASE_URL}/query").mock(
            side_effect=httpx.RequestError("Connection refused")
        )

        # Act & Assert
        with pytest.raises(RuntimeError, match="Network error"):
            client.query("Test question")

    @respx.mock
    def test_api_key_in_header(self, client, mock_settings):
        """Test API key is correctly set in request headers."""
        # Arrange
        route = respx.post(f"{BASE_URL}/query").mock(
            return_value=httpx.Response(200, json={"answer": "test"})
        )

        # Act
        client.query("Test question")

        # Assert
        assert route.called
        request = route.calls[0].request
        assert request.headers["x-api-key"] == mock_settings.icaet_api_key

    @respx.mock
    def test_request_body_format(self, client, mock_settings):
        """Test request body contains email and question fields."""
        # Arrange
        route = respx.post(f"{BASE_URL}/query").mock(
            return_value=httpx.Response(200, json={"answer": "test"})
        )
        question = "What is ICAET?"

        # Act
        client.query(question)

        # Assert
        assert route.called
        request = route.calls[0].request
        import json

        body = json.loads(request.content)
        assert body["email"] == mock_settings.user_email
        assert body["question"] == question


class TestMaskApiKey:
    """Tests for API key masking."""

    def test_mask_api_key_long_key(self, client):
        """Test masking shows last 4 characters for long keys."""
        # Act
        result = client._mask_api_key("test-api-key-12345")

        # Assert
        assert result == "***2345"

    def test_mask_api_key_short_key(self, client):
        """Test masking returns *** for short keys."""
        # Act
        result = client._mask_api_key("abc")

        # Assert
        assert result == "***"

    def test_mask_api_key_exactly_4_chars(self, client):
        """Test masking handles exactly 4 character keys."""
        # Act
        result = client._mask_api_key("abcd")

        # Assert
        assert result == "***abcd"
