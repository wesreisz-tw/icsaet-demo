"""Entry point for icsaet-mcp server."""

import logging
import sys

from pydantic import ValidationError

from icsaet_mcp import __version__
from icsaet_mcp.config import get_settings
from icsaet_mcp.server import mcp

logger = logging.getLogger(__name__)


def configure_logging() -> None:
    """Configure logging to stderr with INFO level."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stderr,
    )


def main() -> None:
    """Start the ICAET MCP server."""
    configure_logging()

    logger.info(f"Starting ICAET MCP Server v{__version__}")

    try:
        get_settings()
        logger.info("Configuration validated successfully")

    except ValidationError as e:
        logger.error("Configuration validation failed")
        missing_fields = []
        for error in e.errors():
            field = error["loc"][0] if error["loc"] else "unknown"
            missing_fields.append(field)

        print(
            "\nError: Missing required configuration\n",
            file=sys.stderr,
        )
        print("Missing environment variables:", file=sys.stderr)
        for field in missing_fields:
            print(f"  - {field}", file=sys.stderr)

        print(
            "\nPlease configure the ICAET MCP server in Cursor:",
            file=sys.stderr,
        )
        print("1. Open Cursor settings", file=sys.stderr)
        print("2. Navigate to MCP configuration", file=sys.stderr)
        print(
            "3. Add ICAET_API_KEY and USER_EMAIL environment variables\n",
            file=sys.stderr,
        )
        print("See README.md for detailed setup instructions.\n", file=sys.stderr)
        sys.exit(1)

    try:
        logger.info("Starting MCP server...")
        mcp.run()

    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
        logger.info("Server shutdown complete")
        sys.exit(0)

    except Exception as e:
        logger.error(f"Server error: {e}")
        print(f"\nError: Server failed to start: {e}\n", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
