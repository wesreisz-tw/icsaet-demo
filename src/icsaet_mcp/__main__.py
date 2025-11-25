"""Entry point for the ICAET MCP server.

This module handles server startup, logging configuration,
and graceful shutdown when running as `python -m icsaet_mcp`.
"""

import logging
import sys

from pydantic import ValidationError

from icsaet_mcp import __version__
from icsaet_mcp.config import get_settings


def setup_logging() -> None:
    """Configure logging for the application.

    Logs are sent to stderr since stdout is used by MCP protocol.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stderr,
    )


def main() -> int:
    """Run the ICAET MCP server.

    Returns:
        Exit code: 0 for success, 1 for errors.
    """
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting ICAET MCP Server v%s", __version__)

    try:
        get_settings()
        logger.info("Configuration validated successfully")
    except ValidationError:
        print(
            "Error: Missing required environment variables.\n\n"
            "Please configure the ICAET MCP server in Cursor:\n"
            "1. Open Cursor settings\n"
            "2. Navigate to MCP configuration\n"
            "3. Add ICAET_API_KEY and USER_EMAIL environment variables\n\n"
            "See README.md for detailed setup instructions.",
            file=sys.stderr,
        )
        return 1

    try:
        from icsaet_mcp.server import mcp

        mcp.run()
        return 0
    except KeyboardInterrupt:
        logger.info("Received shutdown signal, exiting...")
        return 0
    except Exception:
        logger.exception("Unexpected error occurred")
        return 1


if __name__ == "__main__":
    sys.exit(main())
