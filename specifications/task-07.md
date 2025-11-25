# Task 07: Entry Point Implementation

**Story**: SCRUM-5 - Cursor MCP Server for ICAET Query Access  
**Task Sequence**: 7 of 9  
**Dependencies**: Task 06 (MCP server setup complete)

---

## Objective

Implement the `__main__.py` entry point that starts the MCP server, configures logging, handles command-line execution, and manages graceful shutdown.

---

## Scope

- Implement `main()` function in `__main__.py`
- Configure logging for the application
- Import and run the MCP server
- Handle KeyboardInterrupt for graceful shutdown
- Add basic error handling for startup failures
- Support `python -m icsaet_mcp` execution
- Ensure proper exit codes

---

## Acceptance Criteria

1. **Main Function**
   - [ ] Function signature: `def main() -> None:`
   - [ ] Imports MCP server from `server.py`
   - [ ] Configures logging before running server
   - [ ] Calls server's run method
   - [ ] Returns proper exit codes

2. **Logging Configuration**
   - [ ] Logging configured to stderr
   - [ ] Default level: INFO
   - [ ] Format includes timestamp, level, logger name, message
   - [ ] DEBUG level available via environment variable (optional)
   - [ ] Clean, readable log format

3. **Server Startup**
   - [ ] Imports: `from icsaet_mcp.server import mcp`
   - [ ] Validates configuration before starting (call get_settings())
   - [ ] Logs startup message with version
   - [ ] Runs server: `mcp.run()`
   - [ ] Blocks until server exits

4. **Error Handling**
   - [ ] Catches `ValidationError` for missing configuration
   - [ ] Prints helpful error message to stderr
   - [ ] Exits with code 1 for configuration errors
   - [ ] Catches `KeyboardInterrupt` for graceful shutdown
   - [ ] Logs shutdown message
   - [ ] Exits with code 0 on clean shutdown
   - [ ] Catches general exceptions and logs them

5. **Configuration Validation**
   - [ ] Calls `get_settings()` early to validate env vars
   - [ ] Fails fast if configuration invalid
   - [ ] Error message guides user to set ICAET_API_KEY and USER_EMAIL
   - [ ] Error message references Cursor MCP configuration

6. **Command-Line Support**
   - [ ] `if __name__ == "__main__":` block present
   - [ ] Calls `main()` when executed
   - [ ] Works with `python -m icsaet_mcp`
   - [ ] Works via entry point in pyproject.toml

7. **Graceful Shutdown**
   - [ ] Handles Ctrl+C (KeyboardInterrupt)
   - [ ] Logs shutdown message
   - [ ] Cleans up resources
   - [ ] Exits cleanly without stack trace

8. **Testing**
   - [ ] Unit test: Logging configured correctly
   - [ ] Unit test: Configuration validation runs
   - [ ] Unit test: Missing config causes proper exit
   - [ ] Unit test: KeyboardInterrupt handled gracefully
   - [ ] Integration test: Can start server (mocked)

9. **Code Quality**
   - [ ] Full type hints
   - [ ] Module docstring
   - [ ] Follows Python style guide
   - [ ] Passes ruff, black, mypy checks
   - [ ] Clean, readable code

---

## Required Inputs

**From Task 06**:
- Working MCP server instance: `mcp`
- Server run method
- Server lifecycle patterns

**From Task 02**:
- `get_settings()` function for configuration validation
- ValidationError for missing config

**From Task 01**:
- Package version from `__init__.py`
- Entry point configuration in pyproject.toml

---

## Expected Outputs

### Implemented __main__.py
```python
# Key components (not full implementation):
- Logging configuration
- main() function
- Configuration validation
- Server startup
- Error handling
- Graceful shutdown
- if __name__ == "__main__" block
```

### Executable Entry Point
- Can run: `python -m icsaet_mcp`
- Can run: `icsaet-mcp` (via installed entry point)
- Starts MCP server for Cursor
- Handles errors gracefully

### Test file
- `tests/unit/test_main.py` with entry point tests
- Tests for error scenarios
- Tests for graceful shutdown

---

## Handoff Criteria

**Ready for Task 08 when**:
1. All acceptance criteria met
2. All tests passing
3. Can execute `python -m icsaet_mcp` successfully
4. Server starts and connects to Cursor (manual test)
5. Configuration errors show helpful messages
6. Ctrl+C shuts down gracefully
7. Logging works correctly
8. Linters report zero errors
9. Entry point is fully functional

**Artifacts for Next Task**:
- Working entry point
- Pattern for testing the full server
- Logging configuration
- Error messages for troubleshooting guide

---

## Task-Specific Constraints

- Logging to stderr (stdout used by MCP protocol for stdio)
- No command-line arguments needed (config via env vars)
- Keep main() simple and focused
- Error messages must guide users to fix configuration
- Exit codes: 0 for success, 1 for errors
- Support running as module: `python -m icsaet_mcp`
- Work with Cursor's MCP server lifecycle

---

## Logging Format Example

```
2025-11-25 10:30:15 INFO icsaet_mcp.__main__ Starting ICAET MCP Server v0.1.0
2025-11-25 10:30:15 INFO icsaet_mcp.config Configuration validated successfully
2025-11-25 10:30:15 INFO icsaet_mcp.server Server initialized with 1 tool, 3 prompts
2025-11-25 10:30:15 INFO icsaet_mcp.server MCP server running...
```

---

## Error Message Examples

**Missing Configuration**:
```
Error: Missing required environment variable: ICAET_API_KEY

Please configure the ICAET MCP server in Cursor:
1. Open Cursor settings
2. Navigate to MCP configuration
3. Add ICAET_API_KEY and USER_EMAIL environment variables

See README.md for detailed setup instructions.
```

**Graceful Shutdown**:
```
2025-11-25 10:35:20 INFO icsaet_mcp.__main__ Received shutdown signal
2025-11-25 10:35:20 INFO icsaet_mcp.server Server shutdown complete
```

