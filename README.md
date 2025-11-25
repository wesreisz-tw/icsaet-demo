# ICAET MCP Server

MCP server for querying the ICAET conference knowledge base from Cursor IDE.

## Features

- **Query Tool**: Ask natural language questions about conference talks, speakers, and topics
- **Helpful Prompts**: Three built-in prompts to guide your queries
  - ICAET Overview: Learn what ICAET is and how to use it
  - Example Questions: Sample questions to get started
  - Formatting Guidance: Tips for better questions
- **Secure Credentials**: API keys loaded from environment variables, never hardcoded
- **Error Handling**: Clear, actionable error messages

## Requirements

- Python 3.13 or higher
- ICAET API key
- Cursor IDE

## Installation

Install from GitHub:

```bash
pip install git+https://github.com/yourusername/icsaet-mcp.git
```

Or install in development mode:

```bash
git clone https://github.com/yourusername/icsaet-mcp.git
cd icsaet-mcp
pip install -e .
```

## Configuration

Add the ICAET MCP server to your Cursor MCP settings (`~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "icsaet": {
      "command": "python",
      "args": ["-m", "icsaet_mcp"],
      "env": {
        "ICAET_API_KEY": "your-api-key-here",
        "USER_EMAIL": "your-email@example.com"
      }
    }
  }
}
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ICAET_API_KEY` | Yes | Your ICAET API key |
| `USER_EMAIL` | Yes | Your email address for API authentication |

## Usage

After configuring Cursor, you can query the ICAET knowledge base directly from the Cursor IDE.

### Example Queries

- "What did Leslie Miley talk about?"
- "What sessions covered microservices architecture?"
- "Who spoke about platform engineering?"
- "What were the main themes of the conference?"
- "What advice was given about team leadership?"

### Available Prompts

Access these prompts in Cursor for guidance:

1. **ICAET Overview** - Learn what ICAET is and what knowledge it contains
2. **Example Questions** - See sample questions across different query types
3. **Formatting Guidance** - Tips for writing questions that get better answers

## Troubleshooting

### "Missing environment variable" Error

Ensure both `ICAET_API_KEY` and `USER_EMAIL` are set in your Cursor MCP configuration:

1. Open Cursor settings
2. Navigate to MCP configuration (`~/.cursor/mcp.json`)
3. Verify the `env` section includes both variables

### "API key invalid" Error

- Verify your API key is correct
- Check that the key hasn't expired
- Ensure there are no extra spaces in the key

### "Network timeout" Error

- Check your internet connection
- The ICAET API may be temporarily unavailable
- Try again in a few moments

### Server Not Starting

- Verify Python 3.13+ is installed: `python --version`
- Reinstall the package: `pip install --force-reinstall icsaet-mcp`
- Check Cursor logs for detailed error messages

### Checking Logs

Server logs are written to stderr. In Cursor, check the MCP server output panel for detailed information.

## Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=src/icsaet_mcp
```

Run linters:

```bash
ruff check .
black --check .
mypy src/icsaet_mcp
```

## License

MIT
