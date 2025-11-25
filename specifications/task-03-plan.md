# Task 03 Implementation Plan: ICAET API Client

**Story**: SCRUM-5  
**Task**: 3 of 9  
**Dependencies**: Task 02 (configuration management - COMPLETE)

---

## 1. Issue

Implement a synchronous HTTP client (`ICAETClient`) that calls the ICAET API with proper authentication and error handling. The client must handle all expected error scenarios and provide user-friendly error messages for the MCP interface.

---

## 2. Solution

Create an `ICAETClient` class in `src/icsaet_mcp/tools.py` that:
- Uses `httpx.Client` (synchronous) with 30-second timeout
- Authenticates using `x-api-key` header from Settings
- Makes POST requests to `/query` endpoint at `https://icaet-dev.wesleyreisz.com`
- Handles network, timeout, and HTTP errors with descriptive RuntimeError messages
- Returns parsed JSON response as dictionary

Testing strategy: Use `unittest.mock` to mock httpx requests, following the AAA pattern established in `test_config.py`.

---

## 3. Implementation Steps

### 3.1 Update pyproject.toml Dependencies
1. Add `httpx` to dependencies list (main dependency)
2. Add `respx` to dev dependencies for testing HTTP mocking
3. Verify existing dependencies include `pytest` and `pydantic-settings`

### 3.2 Implement ICAETClient in tools.py
1. Add imports at top of `src/icsaet_mcp/tools.py`:
   - `import logging`
   - `from typing import Any, cast`
   - `import httpx`
   - `from icsaet_mcp.config import Settings`

2. Create logger: `logger = logging.getLogger(__name__)`

3. Define `ICAETClient` class with:
   - Class constant: `BASE_URL = "https://icaet-dev.wesleyreisz.com"`
   - Docstring explaining purpose and usage

4. Implement `__init__(self, settings: Settings) -> None`:
   - Store settings instance as `self.settings`
   - Create `self._client = httpx.Client(timeout=30.0, base_url=self.BASE_URL)`

5. Implement `query(self, question: str) -> dict[str, Any]`:
   - **Build request**:
     - `headers = {"x-api-key": self.settings.icaet_api_key}`
     - `payload = {"email": self.settings.user_email, "question": question}`
   
   - **Execute with error handling** (try/except blocks):
     - Try: `response = self._client.post("/query", json=payload, headers=headers)`
     - Try: `response.raise_for_status()`
     - Try: `return cast(dict[str, Any], response.json())`
     - Except `httpx.TimeoutException as e`: 
       - `logger.error(f"Request timeout: {e}")`
       - Raise `RuntimeError("Request timed out. The ICAET API is taking too long to respond.")`
     - Except `httpx.HTTPStatusError as e`:
       - `logger.error(f"HTTP error {e.response.status_code}: {e}")`
       - If 401: Raise `RuntimeError("Authentication failed. Please check your ICAET_API_KEY.")`
       - If 400: Raise `RuntimeError("Invalid request. Please check your question format and email.")`
       - Else: Raise `RuntimeError(f"API error: {e.response.status_code}. Please try again later.")`
     - Except `httpx.RequestError as e`:
       - `logger.error(f"Network error: {e}")`
       - Raise `RuntimeError("Network error. Please check your internet connection.")`
   
   - Docstring: `"""Query the ICAET knowledge base."""`

### 3.3 Create Test Cases in test_tools.py
Tests are included in `tests/unit/test_tools.py` alongside query tool tests.

1. Write test: `test_icaet_client_query_success`
   - Arrange: Mock httpx.Client with successful response
   - Act: Call `client.query("test question")`
   - Assert: Returns expected dictionary

2. Write test: `test_query_with_api_timeout`
   - Arrange: Mock httpx.Client to raise TimeoutException
   - Act: Call `query_icaet("test")`
   - Assert: `RuntimeError` raised with "timed out" in message

3. Write test: `test_query_with_401_error`
   - Arrange: Mock httpx.Client to raise HTTPStatusError with 401
   - Act: Call `query_icaet("test")`
   - Assert: `RuntimeError` raised with "Authentication failed" in message

### 3.4 Verification Steps
1. Run tests: `pytest tests/unit/test_tools.py -v`
2. Verify all tests pass
3. Run linters: `ruff check src/icsaet_mcp/tools.py`
4. Run type checker: `mypy src/icsaet_mcp/tools.py`
5. Verify no linter errors

---

## 4. Verification

**All acceptance criteria from task-03.md must be met**:

### Functional Requirements
- [x] `ICAETClient` initializes with Settings instance
- [x] Uses httpx.Client with 30-second timeout
- [x] Base URL: `https://icaet-dev.wesleyreisz.com`
- [x] POST requests to `/query` endpoint work correctly
- [x] Headers include `x-api-key`
- [x] Request body format: `{"email": "...", "question": "..."}`
- [x] Returns parsed JSON as `dict[str, Any]`

### Error Handling
- [x] `httpx.TimeoutException` caught → raises `RuntimeError` with clear message
- [x] `httpx.HTTPStatusError` caught → raises `RuntimeError` with specific messages for 401, 400, other
- [x] `httpx.RequestError` caught → raises `RuntimeError` with network hint
- [x] All error messages are user-friendly

### Logging & Security
- [x] Logger uses `logging.getLogger(__name__)`
- [x] ERROR logs for failures
- [x] No hardcoded credentials anywhere
- [x] HTTPS enforced (no HTTP fallback)

### Testing
- [x] Unit tests pass
- [x] Tests use `unittest.mock` for mocking httpx
- [x] Tests follow AAA pattern with comments
- [x] Tests verify success scenario
- [x] Tests verify error scenarios

### Code Quality
- [x] Full type hints on all methods and attributes
- [x] Docstrings on class and public methods
- [x] No code comments (code is self-documenting)
- [x] Passes `ruff check`
- [x] Passes `black --check`
- [x] Passes `mypy` type checking
- [x] Line count reasonable (file under 300 lines)

---

## Implementation Checklist

:white_check_mark: 1. Add `httpx` to dependencies in `pyproject.toml`
:white_check_mark: 2. Add `respx` to dev dependencies in `pyproject.toml`
:white_check_mark: 3. Implement `ICAETClient.__init__()` in `tools.py`
:white_check_mark: 4. Implement `ICAETClient.query()` request logic in `tools.py`
:white_check_mark: 5. Implement `ICAETClient.query()` error handling in `tools.py`
:white_check_mark: 6. Write test cases in `test_tools.py`
:white_check_mark: 7. Run all tests and verify they pass
:white_check_mark: 8. Run linters (ruff, black, mypy) and fix any issues
:white_check_mark: 9. Verify all acceptance criteria from task-03.md

---

**Ready for Task 04 when**: All checklist items complete, all tests passing, linters report zero errors, and API client can query ICAET API with proper error handling.

