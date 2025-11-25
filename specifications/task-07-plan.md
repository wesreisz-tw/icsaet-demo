# Task 07 Implementation Plan: Entry Point Implementation

**Story**: SCRUM-5 - Cursor MCP Server for ICAET Query Access  
**Task**: 07 - Entry Point Implementation

---

## 1. Issue

Implement the `__main__.py` entry point that starts the MCP server, configures logging, handles command-line execution, and manages graceful shutdown.

---

## 2. Solution

Implement `main()` function that configures logging to stderr (stdout reserved for MCP protocol), validates configuration early via `get_settings()`, imports and runs the MCP server, and handles KeyboardInterrupt for graceful shutdown. Return appropriate exit codes.

---

## 3. Implementation Steps

1. Implement `src/icsaet_mcp/__main__.py`:
   - Import `logging`, `sys`
   - Import `pydantic.ValidationError`
   - Import `__version__` from `icsaet_mcp`
   - Import `get_settings` from `icsaet_mcp.config`

2. Implement logging configuration function:
   ```python
   def setup_logging() -> None:
       logging.basicConfig(
           level=logging.INFO,
           format="%(asctime)s %(levelname)s %(name)s %(message)s",
           datefmt="%Y-%m-%d %H:%M:%S",
           stream=sys.stderr,  # stdout used by MCP protocol
       )
   ```

3. Implement `main() -> int` function:
   - Call `setup_logging()`
   - Create logger: `logger = logging.getLogger(__name__)`
   - Log INFO: f"Starting ICAET MCP Server v{__version__}"
   - Try block for configuration validation:
     - Call `get_settings()` to validate early
     - Log INFO: "Configuration validated successfully"
   - Except `ValidationError`:
     - Print to stderr: helpful message about setting ICAET_API_KEY and USER_EMAIL
     - Print: "See README.md for detailed setup instructions."
     - Return 1
   - Import `mcp` from `icsaet_mcp.server` (import here to avoid circular imports)
   - Try block for server run:
     - Call `mcp.run()` (blocks until server exits)
     - Return 0
   - Except `KeyboardInterrupt`:
     - Log INFO: "Received shutdown signal, exiting..."
     - Return 0
   - Except `Exception` as e:
     - Log ERROR with exc_info=True
     - Return 1

4. Add `if __name__ == "__main__"` block:
   ```python
   if __name__ == "__main__":
       sys.exit(main())
   ```

5. Create `tests/unit/test_main.py`:
   - Test: `test_setup_logging_configures_stderr` - call setup_logging(), verify handler on stderr
   - Test: `test_main_config_error_returns_1` - mock get_settings to raise ValidationError, verify exit 1
   - Test: `test_main_keyboard_interrupt_returns_0` - mock mcp.run to raise KeyboardInterrupt, verify exit 0
   - Test: `test_main_logs_version` - mock mcp.run, verify version logged
   - Test: `test_main_validates_config_first` - mock get_settings and mcp.run, verify get_settings called before mcp.run

6. Run `pytest tests/unit/test_main.py -v`

7. Run `ruff check src/icsaet_mcp/__main__.py` and `mypy src/icsaet_mcp/__main__.py`

---

## 4. Verification

- [ ] `main()` returns `int` exit code (0 success, 1 error)
- [ ] Logging configured to stderr (not stdout)
- [ ] Configuration validated before server starts
- [ ] Missing config prints helpful error message to stderr
- [ ] KeyboardInterrupt handled gracefully (no stack trace)
- [ ] `python -m icsaet_mcp` works (fails gracefully without env vars)
- [ ] All unit tests pass
- [ ] `ruff check` and `mypy` pass
