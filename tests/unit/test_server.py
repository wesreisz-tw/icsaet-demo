"""Unit tests for MCP server setup."""

from icsaet_mcp.server import mcp


class TestServerSetup:
    """Tests for MCP server configuration."""

    def test_server_instance_exists(self):
        """Test server instance is created."""
        # Assert
        assert mcp is not None

    def test_server_name(self):
        """Test server has correct name."""
        # Assert
        assert mcp.name == "icsaet"

    def test_query_tool_registered(self):
        """Test query tool is registered with server."""
        # Assert
        tools = mcp._tool_manager._tools
        assert "query" in tools

    def test_prompts_registered(self):
        """Test all three prompts are registered."""
        # Assert
        prompts = mcp._prompt_manager._prompts
        assert "icaet_overview" in prompts
        assert "example_questions" in prompts
        assert "formatting_guidance" in prompts

    def test_prompt_count(self):
        """Test exactly three prompts are registered."""
        # Assert
        prompts = mcp._prompt_manager._prompts
        assert len(prompts) == 3
