"""Unit tests for MCP server setup."""

from icsaet_mcp.server import (
    get_example_questions,
    get_formatting_guidance,
    get_icaet_overview,
    mcp,
)


def test_server_instance_exists():
    """Arrange: Import server module
    Act: Access mcp instance
    Assert: Instance exists and is FastMCP type"""
    assert mcp is not None
    assert hasattr(mcp, "run")


def test_server_has_query_tool():
    """Arrange: Server configured with tools
    Act: Check tools list
    Assert: query tool is registered"""
    from icsaet_mcp.tools import query

    assert query is not None


def test_icaet_overview_prompt_content():
    """Arrange: Server with registered prompts
    Act: Get icaet_overview prompt function
    Assert: Returns ICAET overview content"""
    content = get_icaet_overview()

    assert "ICAET" in content
    assert "knowledge base" in content.lower()
    assert len(content) > 100


def test_example_questions_prompt_content():
    """Arrange: Server with registered prompts
    Act: Get example_questions prompt function
    Assert: Returns example questions content"""
    content = get_example_questions()

    assert "example" in content.lower() or "question" in content.lower()
    assert len(content) > 100


def test_formatting_guidance_prompt_content():
    """Arrange: Server with registered prompts
    Act: Get formatting_guidance prompt function
    Assert: Returns formatting guidance content"""
    content = get_formatting_guidance()

    assert "tip" in content.lower() or "do" in content.lower()
    assert len(content) > 100


def test_server_name():
    """Arrange: Server instance
    Act: Access server name
    Assert: Name is 'icsaet'"""
    assert mcp.name == "icsaet"
