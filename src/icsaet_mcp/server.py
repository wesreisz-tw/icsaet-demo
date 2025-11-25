"""FastMCP server setup and configuration."""

import logging

from icsaet_mcp.prompts import (
    EXAMPLE_QUESTIONS,
    FORMATTING_GUIDANCE,
    ICAET_OVERVIEW,
)
from icsaet_mcp.tools import mcp

logger = logging.getLogger(__name__)


def get_icaet_overview() -> str:
    """Explains what ICAET is and how to use the knowledge base from Cursor."""
    return ICAET_OVERVIEW


def get_example_questions() -> str:
    """Provides diverse example questions for querying ICAET."""
    return EXAMPLE_QUESTIONS


def get_formatting_guidance() -> str:
    """Tips for writing better questions to get more targeted answers."""
    return FORMATTING_GUIDANCE


@mcp.prompt()
def icaet_overview() -> str:
    """Explains what ICAET is and how to use the knowledge base from Cursor."""
    return get_icaet_overview()


@mcp.prompt()
def example_questions() -> str:
    """Provides diverse example questions for querying ICAET."""
    return get_example_questions()


@mcp.prompt()
def formatting_guidance() -> str:
    """Tips for writing better questions to get more targeted answers."""
    return get_formatting_guidance()


logger.info("ICAET MCP server configured with 1 tool and 3 prompts")


__all__ = ["mcp", "get_icaet_overview", "get_example_questions", "get_formatting_guidance"]
