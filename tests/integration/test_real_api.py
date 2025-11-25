"""Optional integration test against real ICAET API.

This test is skipped by default. To run it:
    ICAET_API_KEY=your-key USER_EMAIL=your@email.com pytest tests/integration/test_real_api.py -v

Expected response format:
{
    "answer": "...",
    "sources": [...]
}
"""

import os

import pytest

from icsaet_mcp.config import get_settings
from icsaet_mcp.tools import ICAETClient


@pytest.mark.integration
@pytest.mark.skipif(
    not os.getenv("ICAET_API_KEY") or not os.getenv("USER_EMAIL"),
    reason="ICAET_API_KEY and USER_EMAIL environment variables required",
)
class TestRealAPI:
    """Tests against real ICAET API (requires credentials)."""

    def test_real_api_query(self):
        """Test real API call returns valid response."""
        # Arrange
        get_settings.cache_clear()
        settings = get_settings()
        client = ICAETClient(settings)

        # Act
        result = client.query("What is ICAET?")

        # Assert
        assert isinstance(result, dict)
        assert "pinecone_matches" in result or "answer" in result
