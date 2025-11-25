# Task 03 Implementation Plan: ICAET API Client

**Story**: SCRUM-5  
**Task**: 3 of 9  
**Dependencies**: Task 02 (configuration management - COMPLETE)

---

## 1. Issue

Implement a synchronous HTTP client (`ICAETClient`) that calls the ICAET API with proper authentication, error handling, and logging with sensitive data masking. The client must handle all expected error scenarios and provide user-friendly error messages for the MCP interface.

---

## 2. Solution

Create an `ICAETClient` class in `src/icsaet_mcp/tools.py` that:
- Uses `httpx.Client` (synchronous) with 20-second timeout
- Authenticates using `x-api-key` header from Settings
- Makes POST requests to `/query` endpoint at `https://icaet-dev.wesleyreisz.com`
- Handles network, timeout, and HTTP errors with descriptive messages
- Logs operations with API key masking (show only last 4 characters)
- Returns parsed JSON response as dictionary

Testing strategy: Use `respx` library to mock httpx requests, following the AAA pattern established in `test_config.py`.

---

## 3. Implementation Steps

### 3.1 Update pyproject.toml Dependencies
1. Add `httpx` to dependencies list (main dependency)
2. Add `respx` to dev dependencies for testing HTTP mocking
3. Verify existing dependencies include `pytest` and `pydantic-settings`

### 3.2 Implement ICAETClient in tools.py
1. Add imports at top of `src/icsaet_mcp/tools.py`:
   - `import logging`
   - `from typing import Any`
   - `import httpx`
   - `from icsaet_mcp.config import Settings`

2. Create logger: `logger = logging.getLogger(__name__)`

3. Define `ICAETClient` class with:
   - Private constant: `BASE_URL = "https://icaet-dev.wesleyreisz.com"`
   - Private constant: `TIMEOUT_SECONDS = 20`
   - Docstring explaining purpose and usage

4. Implement `__init__(self, settings: Settings) -> None`:
   - Store settings instance as `self._settings`
   - Create `self._client = httpx.Client(timeout=TIMEOUT_SECONDS, base_url=BASE_URL)`
   - Type hint: `self._settings: Settings`
   - Type hint: `self._client: httpx.Client`

5. Implement `_mask_api_key(self, api_key: str) -> str` private helper:
   - If key length < 4, return `"***"`
   - Otherwise return `f"***{api_key[-4:]}"`
   - Add docstring: "Mask API key for logging, showing only last 4 characters"

6. Implement `query(self, question: str) -> dict[str, Any]`:
   - **Input validation**:
     - If `not question or not question.strip()`: raise `ValueError("Question cannot be empty")`
   
   - **Logging start**:
     - `logger.info(f"Querying ICAET API with masked key: {self._mask_api_key(self._settings.icaet_api_key)}")`
     - `logger.debug(f"Query question length: {len(question)} characters")`
   
   - **Build request**:
     - `headers = {"Content-Type": "application/json", "x-api-key": self._settings.icaet_api_key}`
     - `payload = {"email": self._settings.user_email, "question": question}`
   
   - **Execute with error handling** (try/except blocks in this order):
     - Try: `response = self._client.post("/query", json=payload, headers=headers)`
     - Try: `response.raise_for_status()`
     - Try: `return response.json()`
     - Except `httpx.TimeoutException`: 
       - `logger.error("ICAET API request timed out after 20 seconds")`
       - Raise `TimeoutError("ICAET API request timed out. Please try again or check your network connection.")`
     - Except `httpx.HTTPStatusError as e`:
       - `logger.error(f"ICAET API returned error status: {e.response.status_code}")`
       - Raise `RuntimeError(f"ICAET API error (HTTP {e.response.status_code}). Please check your API key and try again.")`
     - Except `httpx.RequestError as e`:
       - `logger.error(f"Network error calling ICAET API: {str(e)}")`
       - Raise `ConnectionError(f"Failed to connect to ICAET API: {str(e)}. Check your network connection.")`
   
   - Docstring:
     ```
     """Query the ICAET API with a question.
     
     Args:
         question: The question to send to ICAET API
         
     Returns:
         Dictionary containing the API response
         
     Raises:
         ValueError: If question is empty or invalid
         TimeoutError: If request times out after 20 seconds
         RuntimeError: If API returns HTTP error status
         ConnectionError: If network connection fails
     """
     ```

7. Implement `__enter__` and `__exit__` for context manager support:
   - `__enter__(self) -> "ICAETClient"`: return `self`
   - `__exit__(self, *args) -> None`: call `self._client.close()`

### 3.3 Create Test File
1. Create `tests/unit/test_icaet_client.py`

2. Add imports:
   - `import pytest`
   - `import respx`
   - `import httpx`
   - `from icsaet_mcp.config import Settings`
   - `from icsaet_mcp.tools import ICAETClient`

3. Create fixture `mock_settings`:
   ```python
   @pytest.fixture
   def mock_settings():
       """Create mock Settings instance for testing"""
       return Settings(
           icaet_api_key="test_key_12345678",
           user_email="test@example.com"
       )
   ```

4. Create fixture `icaet_client`:
   ```python
   @pytest.fixture
   def icaet_client(mock_settings):
       """Create ICAETClient instance with mock settings"""
       return ICAETClient(settings=mock_settings)
   ```

5. Write test: `test_successful_query_returns_data`
   - Arrange: Mock respx route for successful POST
   - Act: Call `client.query("test question")`
   - Assert: Returns expected dictionary

6. Write test: `test_empty_question_raises_value_error`
   - Arrange: Client instance
   - Act: Call `client.query("")`
   - Assert: `ValueError` raised with "empty" in message

7. Write test: `test_whitespace_question_raises_value_error`
   - Arrange: Client instance
   - Act: Call `client.query("   ")`
   - Assert: `ValueError` raised

8. Write test: `test_http_401_raises_runtime_error`
   - Arrange: Mock respx route returning 401
   - Act: Call `client.query("test")`
   - Assert: `RuntimeError` raised with "401" in message

9. Write test: `test_http_500_raises_runtime_error`
   - Arrange: Mock respx route returning 500
   - Act: Call `client.query("test")`
   - Assert: `RuntimeError` raised with "500" in message

10. Write test: `test_timeout_raises_timeout_error`
    - Arrange: Mock respx route that times out
    - Act: Call `client.query("test")`
    - Assert: `TimeoutError` raised with "timed out" in message

11. Write test: `test_network_error_raises_connection_error`
    - Arrange: Mock respx route with network error
    - Act: Call `client.query("test")`
    - Assert: `ConnectionError` raised

12. Write test: `test_request_headers_include_api_key`
    - Arrange: Mock respx route that captures headers
    - Act: Call `client.query("test")`
    - Assert: `x-api-key` header matches settings value

13. Write test: `test_request_body_format`
    - Arrange: Mock respx route that captures body
    - Act: Call `client.query("What is ICAET?")`
    - Assert: Body contains `{"email": "test@example.com", "question": "What is ICAET?"}`

14. Write test: `test_api_key_masking_in_logs` (using `caplog` fixture)
    - Arrange: Client with specific API key
    - Act: Call `client.query("test")` with caplog
    - Assert: Logs contain masked key (last 4 chars visible), not full key

### 3.4 Verification Steps
1. Run tests: `pytest tests/unit/test_icaet_client.py -v`
2. Verify all 10 tests pass
3. Run linters: `ruff check src/icsaet_mcp/tools.py`
4. Run type checker: `mypy src/icsaet_mcp/tools.py`
5. Verify no linter errors
6. Check that API key never appears in full in any log output

---

## 4. Verification

**All acceptance criteria from task-03.md must be met**:

### Functional Requirements
- [ ] `ICAETClient` initializes with Settings instance
- [ ] Uses httpx.Client with 20-second timeout
- [ ] Base URL: `https://icaet-dev.wesleyreisz.com`
- [ ] POST requests to `/query` endpoint work correctly
- [ ] Headers include `Content-Type: application/json` and `x-api-key`
- [ ] Request body format: `{"email": "...", "question": "..."}`
- [ ] Returns parsed JSON as `dict[str, Any]`

### Error Handling
- [ ] `httpx.TimeoutException` caught → raises `TimeoutError` with clear message
- [ ] `httpx.HTTPStatusError` caught → raises `RuntimeError` with status code
- [ ] `httpx.RequestError` caught → raises `ConnectionError` with network hint
- [ ] Empty question → raises `ValueError`
- [ ] All error messages are user-friendly

### Logging & Security
- [ ] Logger uses `logging.getLogger(__name__)`
- [ ] INFO log on query start with masked API key
- [ ] DEBUG log with question length (not full question)
- [ ] ERROR logs for failures
- [ ] API key always masked (only last 4 chars visible or `***`)
- [ ] No email addresses in DEBUG logs
- [ ] No hardcoded credentials anywhere
- [ ] HTTPS enforced (no HTTP fallback)

### Testing
- [ ] All 10 unit tests pass
- [ ] Tests use `respx` for mocking httpx
- [ ] Tests follow AAA pattern with comments
- [ ] Tests verify success scenario
- [ ] Tests verify all error scenarios
- [ ] Tests verify request format (headers and body)
- [ ] Tests verify API key masking in logs

### Code Quality
- [ ] Full type hints on all methods and attributes
- [ ] Docstrings on class and public methods
- [ ] No code comments (code is self-documenting)
- [ ] Passes `ruff check`
- [ ] Passes `black --check`
- [ ] Passes `mypy` type checking
- [ ] Line count reasonable (file under 300 lines)

---

## Implementation Checklist

1. [ ] Add `httpx` to dependencies in `pyproject.toml`
2. [ ] Add `respx` to dev dependencies in `pyproject.toml`
3. [ ] Implement `ICAETClient.__init__()` in `tools.py`
4. [ ] Implement `ICAETClient._mask_api_key()` in `tools.py`
5. [ ] Implement `ICAETClient.query()` with validation in `tools.py`
6. [ ] Implement `ICAETClient.query()` request logic in `tools.py`
7. [ ] Implement `ICAETClient.query()` error handling in `tools.py`
8. [ ] Implement `ICAETClient.__enter__()` and `__exit__()` in `tools.py`
9. [ ] Create `tests/unit/test_icaet_client.py`
10. [ ] Write test fixtures in `test_icaet_client.py`
11. [ ] Write success test in `test_icaet_client.py`
12. [ ] Write validation tests (empty/whitespace) in `test_icaet_client.py`
13. [ ] Write HTTP error tests (401, 500) in `test_icaet_client.py`
14. [ ] Write timeout test in `test_icaet_client.py`
15. [ ] Write network error test in `test_icaet_client.py`
16. [ ] Write header verification test in `test_icaet_client.py`
17. [ ] Write body format test in `test_icaet_client.py`
18. [ ] Write API key masking test in `test_icaet_client.py`
19. [ ] Run all tests and verify they pass
20. [ ] Run linters (ruff, black, mypy) and fix any issues
21. [ ] Verify all acceptance criteria from task-03.md

---

**Ready for Task 04 when**: All checklist items complete, all tests passing, linters report zero errors, and API client can query ICAET API with proper error handling and logging.

