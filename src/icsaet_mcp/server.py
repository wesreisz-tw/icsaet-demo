"""FastMCP server setup and configuration.

This module configures the MCP server for Cursor IDE integration,
registering the query tool and prompts for ICAET knowledge base access.
"""

import logging

from icsaet_mcp import __version__
from icsaet_mcp.prompts import PROMPTS
from icsaet_mcp.tools import mcp

logger = logging.getLogger(__name__)


@mcp.prompt(name="icaet_overview", description="Learn what ICAET is and how to use it")
def icaet_overview() -> str:
    """Provide overview of what ICAET is and how to use it."""
    return PROMPTS[0]["content"]


@mcp.prompt(name="example_questions", description="Sample questions to ask ICAET")
def example_questions() -> str:
    """Provide example questions for ICAET queries."""
    return PROMPTS[1]["content"]


@mcp.prompt(
    name="formatting_guidance", description="Tips for writing better ICAET questions"
)
def formatting_guidance() -> str:
    """Provide tips for better ICAET questions."""
    return PROMPTS[2]["content"]


logger.info("ICAET MCP Server v%s initialized", __version__)
logger.info("Registered 1 tool, 3 prompts")

__all__ = ["mcp"]
