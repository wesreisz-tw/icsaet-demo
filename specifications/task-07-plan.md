# Task 07 Implementation Plan: Entry Point Implementation

**Story**: SCRUM-5  
**Task ID**: Task 07  
**Task Dependencies**: Task 06 (MCP server setup complete), Task 02 (Configuration complete)  
**Created**: 2025-11-25

---

## 1. Issue

Need to implement the `__main__.py` entry point that starts the MCP server, configures logging to stderr, validates configuration at startup, handles graceful shutdown on KeyboardInterrupt, and manages proper exit codes.

---

## 2. Solution

Create a main() function that configures logging, validates settings early, imports and runs the MCP server, and handles all error cases (missing config, KeyboardInterrupt, general exceptions) with appropriate error messages and exit codes.

**Technical Rationale**:
- Log to stderr (stdout reserved for MCP protocol stdio communication)
- Validate configuration before starting server (fail fast)
- Use structured logging format (timestamp, level, logger name, message)
- Handle KeyboardInterrupt for graceful Ctrl+C shutdown
- Exit code 0 for clean shutdown, 1 for errors
- Keep main() simple and focused on orchestration

---

## 3. Implementation Steps

### Step 1: Import Dependencies
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/src/icsaet_mcp/__main__.py`
- Replace entire file content with:
  ```python
  """Entry point for icsaet-mcp server."""

  import logging
  import sys

  from pydantic import ValidationError

  from icsaet_mcp import __version__
  from icsaet_mcp.config import get_settings
  from icsaet_mcp.server import mcp

  logger = logging.getLogger(__name__)
  ```

### Step 2: Add Logging Configuration Function
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/src/icsaet_mcp/__main__.py`
- After imports, add:
  ```python


  def configure_logging() -> None:
      """Configure logging to stderr with INFO level."""
      logging.basicConfig(
          level=logging.INFO,
          format="%(asctime)s %(levelname)s %(name)s %(message)s",
          datefmt="%Y-%m-%d %H:%M:%S",
          stream=sys.stderr,
      )
  ```

### Step 3: Implement Main Function
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/src/icsaet_mcp/__main__.py`
- After configure_logging function, add:
  ```python


  def main() -> None:
      """Start the ICAET MCP server."""
      configure_logging()

      logger.info(f"Starting ICAET MCP Server v{__version__}")

      try:
          settings = get_settings()
          logger.info("Configuration validated successfully")
          logger.info(f"API URL: {settings.api_url}")

      except ValidationError as e:
          logger.error("Configuration validation failed")
          missing_fields = []
          for error in e.errors():
              field = error["loc"][0] if error["loc"] else "unknown"
              missing_fields.append(field)

          print(
              f"\nError: Missing required configuration\n",
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
  ```

### Step 4: Add Entry Point Block
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/src/icsaet_mcp/__main__.py`
- At end of file, add:
  ```python


  if __name__ == "__main__":
      main()
  ```

### Step 5: Create Test File
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/tests/unit/test_main.py`
- Create new file with content:
  ```python
  """Unit tests for entry point."""

  import logging
  import sys
  from unittest.mock import MagicMock, patch

  import pytest
  from pydantic import ValidationError

  from icsaet_mcp.__main__ import configure_logging, main


  def test_configure_logging():
      """Arrange: Clean logging state
      Act: Call configure_logging
      Assert: Logging configured to stderr with INFO level"""
      configure_logging()

      root_logger = logging.getLogger()
      assert root_logger.level == logging.INFO

      handlers = root_logger.handlers
      assert any(
          isinstance(h, logging.StreamHandler) and h.stream == sys.stderr
          for h in handlers
      )


  def test_main_with_valid_configuration():
      """Arrange: Valid configuration and mocked server
      Act: Call main
      Assert: Server starts successfully"""
      with patch("icsaet_mcp.__main__.get_settings") as mock_settings, patch(
          "icsaet_mcp.__main__.mcp"
      ) as mock_mcp:
          mock_settings.return_value = MagicMock(
              api_url="https://api.example.com/query"
          )
          mock_mcp.run.return_value = None

          main()

          mock_settings.assert_called_once()
          mock_mcp.run.assert_called_once()


  def test_main_with_missing_configuration(capsys):
      """Arrange: Missing environment variables
      Act: Call main
      Assert: Exits with code 1 and prints helpful error message"""
      with patch("icsaet_mcp.__main__.get_settings") as mock_settings:
          mock_settings.side_effect = ValidationError.from_exception_data(
              "Settings",
              [
                  {
                      "type": "missing",
                      "loc": ("ICAET_API_KEY",),
                      "input": {},
                      "msg": "Field required",
                  }
              ],
          )

          with pytest.raises(SystemExit) as exc_info:
              main()

          assert exc_info.value.code == 1

          captured = capsys.readouterr()
          assert "Missing required configuration" in captured.err
          assert "ICAET_API_KEY" in captured.err
          assert "Cursor" in captured.err


  def test_main_with_keyboard_interrupt():
      """Arrange: Server running, user presses Ctrl+C
      Act: Raise KeyboardInterrupt during server run
      Assert: Exits gracefully with code 0"""
      with patch("icsaet_mcp.__main__.get_settings") as mock_settings, patch(
          "icsaet_mcp.__main__.mcp"
      ) as mock_mcp:
          mock_settings.return_value = MagicMock(
              api_url="https://api.example.com/query"
          )
          mock_mcp.run.side_effect = KeyboardInterrupt()

          with pytest.raises(SystemExit) as exc_info:
              main()

          assert exc_info.value.code == 0


  def test_main_with_server_error(capsys):
      """Arrange: Server raises unexpected exception
      Act: Call main
      Assert: Exits with code 1 and prints error message"""
      with patch("icsaet_mcp.__main__.get_settings") as mock_settings, patch(
          "icsaet_mcp.__main__.mcp"
      ) as mock_mcp:
          mock_settings.return_value = MagicMock(
              api_url="https://api.example.com/query"
          )
          mock_mcp.run.side_effect = RuntimeError("Test error")

          with pytest.raises(SystemExit) as exc_info:
              main()

          assert exc_info.value.code == 1

          captured = capsys.readouterr()
          assert "Server failed to start" in captured.err
          assert "Test error" in captured.err


  def test_main_logs_version():
      """Arrange: Valid configuration
      Act: Call main
      Assert: Logs include version number"""
      with patch("icsaet_mcp.__main__.get_settings") as mock_settings, patch(
          "icsaet_mcp.__main__.mcp"
      ) as mock_mcp, patch("icsaet_mcp.__main__.logger") as mock_logger:
          mock_settings.return_value = MagicMock(
              api_url="https://api.example.com/query"
          )
          mock_mcp.run.return_value = None

          main()

          info_calls = [str(call) for call in mock_logger.info.call_args_list]
          assert any("v0.1.0" in call or "version" in call.lower() for call in info_calls)


  def test_main_validates_config_before_starting():
      """Arrange: Configuration that will fail validation
      Act: Call main
      Assert: get_settings called before mcp.run"""
      with patch("icsaet_mcp.__main__.get_settings") as mock_settings, patch(
          "icsaet_mcp.__main__.mcp"
      ) as mock_mcp:
          mock_settings.side_effect = ValidationError.from_exception_data(
              "Settings", [{"type": "missing", "loc": ("ICAET_API_KEY",), "input": {}}]
          )

          with pytest.raises(SystemExit):
              main()

          mock_settings.assert_called_once()
          mock_mcp.run.assert_not_called()
  ```

### Step 6: Run Tests
**Command**: `pytest tests/unit/test_main.py -v`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: All 8 tests pass

### Step 7: Run Linter
**Command**: `ruff check src/icsaet_mcp/__main__.py tests/unit/test_main.py`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: Zero errors

### Step 8: Run Formatter
**Command**: `black --check src/icsaet_mcp/__main__.py tests/unit/test_main.py`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: No changes needed

### Step 9: Run Type Checker
**Command**: `mypy src/icsaet_mcp/__main__.py`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: Zero type errors

### Step 10: Verify Entry Point Execution
**Command**: `python -m icsaet_mcp --help 2>&1 | head -5`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: Shows error about missing configuration (expected when env vars not set)

---

## 4. Verification

### Main Function Implementation
- Function signature: `def main() -> None:`
- Configures logging first (to stderr)
- Validates settings before starting server
- Imports and calls mcp.run()
- Returns proper exit codes (0 for success, 1 for errors)

### Logging Configuration
- Logging configured to stderr (not stdout)
- Default level is INFO
- Format includes timestamp, level, logger name, message
- Timestamp format: YYYY-MM-DD HH:MM:SS
- Clean, readable format

### Configuration Validation
- Calls get_settings() early in startup
- Catches ValidationError for missing env vars
- Extracts missing field names from error
- Prints helpful error message to stderr
- Guides user to configure in Cursor
- Exits with code 1 on validation failure

### Error Handling
- Catches ValidationError and exits with code 1
- Catches KeyboardInterrupt and exits with code 0
- Catches general Exception and exits with code 1
- Logs shutdown message on KeyboardInterrupt
- All error messages go to stderr
- No stack traces shown to user (logged only)

### Entry Point Block
- `if __name__ == "__main__":` block present
- Calls main() function
- Supports `python -m icsaet_mcp` execution

### Code Quality
- All 8 tests pass
- ruff reports zero errors
- black reports no formatting changes needed
- mypy reports zero type errors
- Full type hints on all functions

---

## IMPLEMENTATION CHECKLIST

:white_check_mark: 1. Add imports (logging, sys, pydantic, version, config, server)
:white_check_mark: 2. Create logger instance
:white_check_mark: 3. Implement configure_logging function
:white_check_mark: 4. Set logging to stderr with INFO level
:white_check_mark: 5. Set logging format with timestamp, level, name, message
:white_check_mark: 6. Implement main function
:white_check_mark: 7. Call configure_logging at start of main
:white_check_mark: 8. Log startup message with version
:white_check_mark: 9. Validate settings with get_settings
:white_check_mark: 10. Log successful configuration validation
:white_check_mark: 11. Add ValidationError handling with helpful error message
:white_check_mark: 12. Print configuration guidance to stderr
:white_check_mark: 13. Exit with code 1 on configuration error
:white_check_mark: 14. Call mcp.run to start server
:white_check_mark: 15. Add KeyboardInterrupt handling
:white_check_mark: 16. Log shutdown message on interrupt
:white_check_mark: 17. Exit with code 0 on clean shutdown
:white_check_mark: 18. Add general Exception handling
:white_check_mark: 19. Exit with code 1 on server error
:white_check_mark: 20. Add if __name__ == "__main__" block
:white_check_mark: 21. Create test_main.py with 8 test cases
:white_check_mark: 22. Run pytest and verify all tests pass
:white_check_mark: 23. Run ruff and verify zero errors
:white_check_mark: 24. Run black and verify no changes needed
:white_check_mark: 25. Run mypy and verify zero type errors

