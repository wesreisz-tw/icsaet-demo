# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-11-25

### Added

- Initial release of ICAET MCP Server
- Query tool for asking natural language questions about ICAET conference content
- Three helpful prompts:
  - ICAET Overview: Learn what ICAET is and how to use it
  - Example Questions: Sample questions to get started
  - Formatting Guidance: Tips for writing better questions
- Configuration via environment variables (ICAET_API_KEY, USER_EMAIL)
- Comprehensive error handling with user-friendly messages
- Cursor MCP integration via stdio protocol
- Logging with API key masking for security
- Full test suite with 93% coverage

### Requirements

- Python 3.13+
- fastmcp >= 0.1.0
- httpx >= 0.24.0
- pydantic-settings >= 2.0.0

