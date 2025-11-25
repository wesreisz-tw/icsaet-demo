# Task 03: ICAET API Client Implementation

**Story**: SCRUM-5 - Cursor MCP Server for ICAET Query Access  
**Task Sequence**: 3 of 9  
**Dependencies**: Task 02 (configuration management complete)

---

## Objective

Implement a synchronous HTTP client for the ICAET API that handles authentication, request/response processing, error handling, and proper logging with sensitive data masking.

---

## Scope

- Create `ICAETClient` class in `tools.py`
- Implement `query()` method that calls ICAET API endpoint
- Configure httpx.Client with 20-second timeout
- Handle authentication via `x-api-key` header
- Implement comprehensive error handling (network errors, HTTP errors, timeouts)
- Add structured logging with API key masking
- Create unit tests with mocked API responses

---

## Acceptance Criteria

1. **ICAETClient Class**
   - [ ] Class initializes with Settings instance
   - [ ] Uses `httpx.Client` with 20-second timeout
   - [ ] Base URL configured: `https://icaet-dev.wesleyreisz.com`
   - [ ] Proper type hints on all methods

2. **Query Method**
   - [ ] Method signature: `query(question: str) -> dict[str, Any]`
   - [ ] Makes POST request to `/query` endpoint
   - [ ] Sets `Content-Type: application/json` header
   - [ ] Sets `x-api-key` header from settings
   - [ ] Request body: `{"email": user_email, "question": question}`
   - [ ] Returns parsed JSON response as dictionary

3. **Error Handling**
   - [ ] Catches `httpx.TimeoutException` with clear error message
   - [ ] Catches `httpx.HTTPStatusError` with status code in message
   - [ ] Catches `httpx.RequestError` for network issues
   - [ ] Raises descriptive exceptions that can be shown to users
   - [ ] All errors include troubleshooting hints

4. **Logging**
   - [ ] Logger configured: `logging.getLogger(__name__)`
   - [ ] INFO log when query starts (with masked API key)
   - [ ] DEBUG log with request details (question length, not full question)
   - [ ] ERROR log for API failures
   - [ ] API key always masked in logs (show only last 4 chars or use `***`)
   - [ ] No email addresses in DEBUG logs (privacy)

5. **Security**
   - [ ] No credentials hardcoded anywhere
   - [ ] API key read from Settings only
   - [ ] HTTPS enforced (no HTTP fallback)
   - [ ] Sensitive data never logged in full

6. **Testing**
   - [ ] Unit test: Successful query returns expected data
   - [ ] Unit test: Missing question raises appropriate error
   - [ ] Unit test: Empty question raises validation error
   - [ ] Unit test: HTTP 401 error handled correctly
   - [ ] Unit test: HTTP 500 error handled correctly
   - [ ] Unit test: Network timeout handled correctly
   - [ ] Unit test: API key properly set in request headers
   - [ ] Unit test: Request body format matches API contract
   - [ ] All tests use mocked httpx responses

7. **Code Quality**
   - [ ] Full type hints including return types
   - [ ] Docstrings on class and public methods
   - [ ] Follows project Python style guide
   - [ ] Passes ruff, black, mypy checks
   - [ ] No code comments (self-documenting code)

---

## Required Inputs

**From Task 02**:
- Working `config.py` with `get_settings()` function
- Settings class with `icaet_api_key` and `user_email` fields
- Pattern for mocking configuration in tests

---

## Expected Outputs

### Implemented ICAETClient
```python
# Key components (not full implementation):
- ICAETClient class
- __init__(settings: Settings) method
- query(question: str) -> dict[str, Any] method
- Proper error handling with custom exceptions
- Structured logging with masking
```

### Test file
- `tests/unit/test_icaet_client.py` with comprehensive mocking
- Tests for success and various failure scenarios
- Examples of using `respx` or similar for mocking httpx

### API Contract Verification
- Request format matches SCRUM-5 spec exactly
- Headers match specification
- Response handling works with expected JSON structure

---

## Handoff Criteria

**Ready for Task 04 when**:
1. All acceptance criteria met
2. All tests passing with mocked API
3. Can successfully make a query with valid credentials (manual test optional)
4. Error messages are clear and actionable
5. Logging works correctly with sensitive data masked
6. API contract matches SCRUM-5 specification
7. Linters report zero errors

**Artifacts for Next Task**:
- Working `ICAETClient` class ready for integration
- Query method that returns structured data
- Error handling patterns for MCP tool to use
- Test patterns for mocking API calls

---

## Task-Specific Constraints

- Use synchronous httpx.Client (no async per architecture decision)
- 20-second timeout (per architecture decision)
- Follow API contract from SCRUM-5 spec exactly:
  - Endpoint: `POST https://icaet-dev.wesleyreisz.com/query`
  - Header: `x-api-key`
  - Body: `{"email": "...", "question": "..."}`
- Mask API keys in logs (show only `***KEY_SUFFIX`)
- Error messages must be user-friendly (shown in Cursor)
- No modification to existing ICAET API

