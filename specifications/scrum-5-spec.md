# SCRUM-5: Cursor MCP Server for ICAET Query Access

**Issue Type:** Task  
**Status:** To Do  
**Priority:** Medium  
**Created:** 2025-11-22  
**Reporter:** Wesley Reisz  

---

## As a

Developer using Cursor IDE who wants to query the ICAET knowledge base.

## I want to Configure a local MCP server in Cursor that allows me to ask questions against the ICAET API using simple environment variable configuration.

## So that

I can ask multi-turn questions against the ICAET Query API directly from Cursor without managing complex authentication flows, while keeping the existing ICAET API completely untouched.

---

# High-Level Description of the System

A local MCP server runs on the developer's machine and integrates with Cursor IDE. The developer configures their ICAET API key and email as environment variables in Cursor's MCP configuration. The MCP server exposes a query tool and helpful prompts that enable natural language interaction with the ICAET knowledge base.

The MCP server:

1. Receives queries from Cursor
2. Calls the existing ICAET API with the configured API key and email
3. Returns results to Cursor
4. Provides helpful prompts and examples to guide users

---

# Architecture Components

## Local Resources

* **Python MCP Server** (using fastmcp framework) - Runs locally on developer's machine
* **Environment Variables** - Stores ICAET_API_KEY and USER_EMAIL

## External Services

* **Cursor IDE** - MCP client interface
* **Existing ICAET API** - [https://icaet-dev.wesleyreisz.com/query](https://icaet-dev.wesleyreisz.com/query) (UNTOUCHED)

## No AWS Infrastructure Required

* MCP server runs entirely locally
* No Lambda, API Gateway, or other cloud resources needed

---

# Request Flow

```
1. Developer configures MCP server in Cursor
   ↓
2. Developer opens Cursor IDE
   ↓
3. Cursor starts local MCP server process
   ↓
4. Developer asks: "What did Leslie Miley talk about?"
   ↓
5. Cursor sends query to MCP server
   ↓
6. MCP server:
   - Receives question from Cursor
   - Reads ICAET_API_KEY and USER_EMAIL from environment
   - Calls ICAET API: POST https://icaet-dev.wesleyreisz.com/query
     Headers: x-api-key: {ICAET_API_KEY}
     Body: {"email": "{USER_EMAIL}", "question": "What did Leslie Miley talk about?"}
   - Returns ICAET response
   ↓
7. Cursor displays results to developer
```

---

# Acceptance Criteria

## 1. MCP Server Implementation

* Python-based MCP server using fastmcp framework
* Single `query` tool that accepts a question parameter
* Tool calls ICAET API with configured credentials
* Handles errors gracefully (API errors, network issues, missing credentials)
* Logs appropriately (no sensitive data in logs)

## 2. MCP Server Prompts

* Prompt that explains what ICAET is and how to use it

    * \[STUB: To be filled in with ICAET description\]
    
* Prompt that provides example questions

    * \[STUB: To be filled in with example queries\]
    
* Prompt that helps users format their questions better

    * \[STUB: To be filled in with formatting guidance\]
    

## 3. Cursor Configuration

* MCP server configured in Cursor's settings
* Environment variables set for ICAET_API_KEY and USER_EMAIL
* Server starts automatically when Cursor launches
* Server stops gracefully when Cursor closes

## 4. Tool Interface

* Tool name: `query`
* Input parameter: `question` (string, required)
* Returns: ICAET API response (JSON)
* Error handling for missing/invalid parameters

## 5. Security

* No credentials hardcoded in code
* API key and email read from environment variables only
* No sensitive data logged
* All communication with ICAET API over HTTPS

## 6. User Experience

* Developer configures once, uses indefinitely
* Natural language queries work seamlessly
* Multi-turn conversations supported
* Clear error messages for configuration issues
* Helpful prompts guide usage

## 7. Non-Impact to Existing Infrastructure

* Existing ICAET API unchanged and still functional independently
* No AWS resources created or modified
* No dependencies on existing infrastructure
* Can be installed/removed without affecting other systems

---

# Definition of Done

## Functional DoD

* MCP server successfully connects to Cursor
* Queries return ICAET results
* Missing credentials show clear error messages
* Multi-turn conversations work seamlessly
* Prompts display correctly in Cursor

## Security DoD

* No credentials in code
* HTTPS communication with ICAET API
* No sensitive data logged
* Environment variables properly isolated

## Operational DoD

* Simple installation process (pip install + config)
* Clear documentation for setup
* MCP server starts/stops cleanly
* End-to-end test passes
* Troubleshooting guide available

---

# Implementation Details

## Technology Stack

* **Language:** Python 3.12+
* **Framework:** fastmcp
* **IDE Integration:** Cursor MCP client
* **Authentication:** Environment variables
* **Deployment:** Local process

## Cursor MCP Configuration Example

```
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

## MCP Server Structure

```
icsaet-mcp/
├── pyproject.toml          # Python package configuration
├── README.md               # Setup and usage instructions
├── src/
│   └── icsaet_mcp/
│       ├── __init__.py
│       ├── __main__.py     # MCP server entry point
│       ├── server.py       # fastmcp server implementation
│       ├── tools.py        # Query tool implementation
│       └── prompts.py      # Prompt templates
└── tests/
    └── test_server.py      # Basic tests
```

## Existing ICAET API Contract

```
curl -X POST "https://icaet-dev.wesleyreisz.com/query" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $ICAET_API_KEY" \
  -d '{
    "email": "user@example.com",
    "question": "What stories did Leslie Miley tell in his talk?"
  }'
```

## Installation Steps

1. Install Python package from GitHub: `pip install git+https://github.com/yourusername/icsaet-mcp.git`

    * Alternative: Install from PyPI: `pip install icsaet-mcp` (if published)
    
2. Configure Cursor MCP settings with API key and email
3. Restart Cursor
4. MCP server starts automatically

See the "Packaging and Distribution" section below for detailed installation options.

## Required Environment Variables

* `ICAET_API_KEY` - API key for ICAET service (required)
* `USER_EMAIL` - Email address to pass to ICAET API (required)

---

# Packaging and Distribution

## Package Configuration (pyproject.toml)

```
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "icsaet-mcp"
version = "0.1.0"
description = "MCP server for querying the ICAET knowledge base from Cursor IDE"
readme = "README.md"
requires-python = ">=3.12"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
keywords = ["mcp", "cursor", "icaet", "knowledge-base"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
]

dependencies = [
    "fastmcp>=0.1.0",
    "httpx>=0.24.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
]

[project.urls]
Homepage = "https://github.com/yourusername/icsaet-mcp"
Repository = "https://github.com/yourusername/icsaet-mcp"
Issues = "https://github.com/yourusername/icsaet-mcp/issues"

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
icsaet_mcp = ["py.typed"]
```

## Installation Methods

### Method 1: Install from GitHub (Recommended for Users)

```
pip install git+https://github.com/yourusername/icsaet-mcp.git
```

### Method 2: Install Specific Version/Branch/Tag

```
# Install specific tag/version
pip install git+https://github.com/yourusername/icsaet-mcp.git@v0.1.0

# Install specific branch
pip install git+https://github.com/yourusername/icsaet-mcp.git@main

# Install specific commit
pip install git+https://github.com/yourusername/icsaet-mcp.git@abc123def
```

### Method 3: Development Installation (For Contributors)

```
# Clone repository
git clone https://github.com/yourusername/icsaet-mcp.git
cd icsaet-mcp

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

### Method 4: Install from PyPI (Future Option)

```
pip install icsaet-mcp
```

## GitHub Repository Setup

### Required Files

1. **LICENSE** - MIT or Apache 2.0 recommended
2. **README.md** - Installation and usage instructions
3. **pyproject.toml** - Package configuration (shown above)
4. **.gitignore** - Python-specific ignores
5. [**MANIFEST.in**](http://MANIFEST.in) - Include non-Python files if needed

### README.md Structure

```
# ICAET MCP Server

MCP server for querying the ICAET knowledge base from Cursor IDE.

## Installation

pip install git+https://github.com/yourusername/icsaet-mcp.git

## Configuration

Add to your Cursor MCP settings (~/.cursor/config.json):

[Configuration JSON example from above]

## Usage

[Usage examples]

## Development

[Development setup instructions]

## License

MIT
```

### GitHub Release Process

1. **Tag Version**

    ```
    git tag -a v0.1.0 -m "Release version 0.1.0"
    git push origin v0.1.0
    
    ```
2. **Create GitHub Release**

    * Go to repository → Releases → Create new release
    * Select the version tag
    * Add release notes
    * Attach built wheel/sdist (optional)
    
3. **Build Distribution (Optional)**

    ```
    pip install build
    python -m build
    
    ```

    This creates `dist/icsaet_mcp-0.1.0.tar.gz` and `dist/icsaet_mcp-0.1.0-py3-none-any.whl`



## Publishing to PyPI (Optional)

### Test PyPI (Recommended First)

```
# Install twine
pip install twine

# Upload to Test PyPI
python -m twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ icsaet-mcp
```

### Production PyPI

```
# Upload to PyPI
python -m twine upload dist/*

# Users can now install via
pip install icsaet-mcp
```

## Version Management

* Follow Semantic Versioning (<custom data-type="smartlink" data-id="id-0">http://semver.org</custom> )
* Update version in `pyproject.toml` before release
* Keep CHANGELOG.md updated
* Tag releases in Git

---

# Key Simplifications

* **No OAuth** - Simple environment variable configuration
* **No AWS Infrastructure** - Runs entirely locally
* **No Token Management** - Static API key
* **No Web Server** - MCP protocol over stdio
* **No Database** - Stateless tool calls

---

# Prompt Templates (To Be Completed)

## ICAET Overview Prompt

\[STUB: Add description of what ICAET is, what it contains, and how to use it\]

## Example Questions Prompt

\[STUB: Add example questions that demonstrate ICAET capabilities\]

Example format:

* "What did Leslie Miley talk about?"
* \[Add more examples\]

## Question Formatting Guidance Prompt

\[STUB: Add guidance on how to format questions for best results\]

Example guidance:

* Be specific in your questions
* \[Add more formatting tips\]

