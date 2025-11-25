# Task 03 Implementation Plan: ICAET API Client Implementation

**Story**: SCRUM-5 - Cursor MCP Server for ICAET Query Access  
**Task**: 03 - ICAET API Client Implementation

---

## 1. Issue

Implement a synchronous HTTP client for the ICAET API that handles authentication, request/response processing, error handling, and logging with sensitive data masking.

---

## 2. Solution

Create `ICAETClient` class in `tools.py` using `httpx.Client` with 20-second timeout. Implement `query()` method that POSTs to `https://icaet-dev.wesleyreisz.com/query` with proper headers and body format. Handle all error scenarios (timeout, HTTP errors, network errors) with user-friendly messages. Mask API keys in all log output.

---

## 3. Implementation Steps

1. Implement `ICAETClient` class in `src/icsaet_mcp/tools.py`:
   - Import `logging`, `httpx`, `typing.Any`, and `Settings` from config
   - Create module-level logger: `logger = logging.getLogger(__name__)`
   - Define `BASE_URL = "https://icaet-dev.wesleyreisz.com"`
   - Define `TIMEOUT_SECONDS = 20.0`
   - Create `ICAETClient` class:
     - `__init__(self, settings: Settings)` - store settings instance
     - `_mask_api_key(self, key: str) -> str` - return `"***" + key[-4:]` if len >= 4, else `"***"`
     - `query(self, question: str) -> dict[str, Any]` method

2. Implement `query()` method:
   - Log INFO: "Querying ICAET API (key: {masked_key})"
   - Log DEBUG: "Question length: {len(question)} chars"
   - Create `httpx.Client(timeout=TIMEOUT_SECONDS)` context manager
   - POST to `f"{BASE_URL}/query"` with:
     - Headers: `{"Content-Type": "application/json", "x-api-key": self.settings.icaet_api_key}`
     - JSON body: `{"email": self.settings.user_email, "question": question}`
   - Call `response.raise_for_status()`
   - Return `response.json()`

3. Implement error handling in `query()`:
   - Catch `httpx.TimeoutException`: log ERROR, raise `RuntimeError("ICAET API request timed out. Please try again.")`
   - Catch `httpx.HTTPStatusError`: log ERROR with status code, raise `RuntimeError(f"ICAET API error (HTTP {status}): {message}")`
   - Catch `httpx.RequestError`: log ERROR, raise `RuntimeError("Network error connecting to ICAET API. Check your connection.")`

4. Create `tests/unit/test_icaet_client.py`:
   - Import `pytest`, `httpx`, `unittest.mock.MagicMock`
   - Create inline mock Settings using `MagicMock(icaet_api_key="test-key", user_email="test@example.com")`
   - Test: `test_query_success` - mock httpx.Client.post to return valid JSON, verify response
   - Test: `test_query_timeout_handled` - mock to raise `httpx.TimeoutException`, expect RuntimeError
   - Test: `test_query_http_401_handled` - mock 401 response, expect RuntimeError with status code
   - Test: `test_query_http_500_handled` - mock 500 response, expect RuntimeError
   - Test: `test_query_network_error_handled` - mock `httpx.RequestError`, expect RuntimeError
   - Test: `test_api_key_in_header` - verify header contains correct x-api-key
   - Test: `test_request_body_format` - verify body has email and question fields

5. Run `pytest tests/unit/test_icaet_client.py -v`

6. Run `ruff check src/icsaet_mcp/tools.py` and `mypy src/icsaet_mcp/tools.py`

---

## 4. Verification

- [ ] `ICAETClient` initializes with Settings instance
- [ ] `query()` makes POST to correct endpoint with proper headers and body
- [ ] 20-second timeout configured on httpx.Client
- [ ] All httpx exceptions caught and converted to user-friendly RuntimeError
- [ ] API key masked in all log messages (shows only last 4 chars)
- [ ] All unit tests pass
- [ ] `ruff check` and `mypy` pass
