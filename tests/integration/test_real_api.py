"""Optional integration test against real ICAET API.

This test is skipped by default and requires:
- ICAET_API_KEY environment variable
- USER_EMAIL environment variable
- Network access to ICAET API

Run with: pytest -m real_api tests/integration/test_real_api.py
"""

import os

import pytest

from icsaet_mcp.tools import query_icaet


@pytest.mark.real_api
@pytest.mark.skipif(
    not os.getenv("ICAET_API_KEY") or not os.getenv("USER_EMAIL"),
    reason="Requires ICAET_API_KEY and USER_EMAIL environment variables",
)
def test_query_against_real_api():
    """Arrange: Real ICAET credentials in environment
    Act: Call query tool with real question
    Assert: Returns response from real API"""
    result = query_icaet("What is ICAET?")

    assert isinstance(result, str)
    assert len(result) > 0

    print(f"\nReal API Response:\n{result}\n")

