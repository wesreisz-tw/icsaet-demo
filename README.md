# icsaet-mcp

MCP server for querying ICAET conference data.

## Overview

This Model Context Protocol (MCP) server provides tools for querying the ICSAET QCon London 2025 conference data API.

## Requirements

- Python 3.13 or higher

## Installation

```bash
pip install -e .
```

## Configuration

This MCP server requires two environment variables to be configured in Cursor:

- `ICAET_API_KEY` - Your API key for ICAET authentication (minimum 10 characters)
- `USER_EMAIL` - Your email address for API requests (must be valid email format)

### Cursor Setup

1. Open Cursor Settings (Cmd+, on Mac or Ctrl+, on Windows/Linux)
2. Navigate to the MCP section
3. Add your MCP server configuration:

```json
{
  "mcpServers": {
    "icsaet": {
      "command": "python",
      "args": ["-m", "icsaet_mcp"],
      "env": {
        "ICAET_API_KEY": "your-actual-api-key-here",
        "USER_EMAIL": "your-email@example.com"
      }
    }
  }
}
```

Replace `your-actual-api-key-here` and `your-email@example.com` with your actual credentials.

## Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Run linter:

```bash
ruff check .
```

Format code:

```bash
black .
```

Type checking:

```bash
mypy src/icsaet_mcp
```

## License

MIT
