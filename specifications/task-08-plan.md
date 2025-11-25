# Task 08 Implementation Plan: Testing and Verification

**Story**: SCRUM-5 - Cursor MCP Server for ICAET Query Access  
**Task**: 08 - Testing and Verification

---

## 1. Issue

Create comprehensive test coverage for the MCP server, verify all components work together via integration tests, and ensure all SCRUM-5 Definition of Done criteria are met.

---

## 2. Solution

Review and consolidate unit tests from Tasks 02-07, add integration tests for end-to-end flows, create shared test fixtures in `conftest.py`, and optionally add a real API test (skipped by default). Document test patterns and verify against SCRUM-5 acceptance criteria.

---

## 3. Implementation Steps

1. Create `tests/conftest.py` with shared fixtures (replacing inline mocks from earlier tasks):
   - `@pytest.fixture` for `mock_settings` - returns MagicMock with valid icaet_api_key and user_email
   - `@pytest.fixture` for `mock_env_vars` - uses monkeypatch to set ICAET_API_KEY and USER_EMAIL
   - `@pytest.fixture` for `clear_settings_cache` - calls `get_settings.cache_clear()` in setup/teardown
   - `@pytest.fixture` for `mock_httpx_client` - returns mocked httpx.Client with configurable responses

2. Refactor existing unit tests to use shared fixtures:
   - `tests/unit/test_config.py` (from Task 02) - use `mock_env_vars`, `clear_settings_cache`
   - `tests/unit/test_icaet_client.py` (from Task 03) - replace inline mock with `mock_settings`
   - `tests/unit/test_tools.py` (from Task 05) - use `mock_settings`, `mock_httpx_client`
   - `tests/unit/test_server.py` (from Task 06) - no changes needed
   - `tests/unit/test_main.py` (from Task 07) - use `clear_settings_cache`
   - Add any missing edge case tests

3. Create `tests/integration/test_query_flow.py`:
   - Test: `test_full_query_flow_success` - set env vars, mock httpx, call query_icaet(), verify response
   - Test: `test_query_flow_missing_config` - no env vars, verify config error returned
   - Test: `test_query_flow_api_timeout` - mock timeout, verify error message
   - Test: `test_query_flow_api_error` - mock 500 response, verify error handling
   - Test: `test_error_propagation` - verify errors flow correctly through layers

4. Create `tests/integration/test_real_api.py` (optional, skipped by default):
   - Add `pytest.mark.integration` marker
   - Add skip condition: `@pytest.mark.skipif(not os.getenv("ICAET_API_KEY"), reason="No API key")`
   - Test: `test_real_api_query` - make actual API call with real credentials
   - Document expected response format in docstring

5. Create `tests/README.md`:
   - How to run tests: `pytest`
   - How to run with coverage: `pytest --cov=src/icsaet_mcp`
   - How to run integration tests: `pytest -m integration`
   - How to run real API test: `ICAET_API_KEY=xxx USER_EMAIL=xxx pytest tests/integration/test_real_api.py`
   - Mock patterns and fixture usage

6. Update `pyproject.toml` for pytest markers:
   ```toml
   [tool.pytest.ini_options]
   markers = [
       "integration: marks tests as integration tests",
   ]
   ```

7. Run full test suite: `pytest -v`

8. Run coverage: `pytest --cov=src/icsaet_mcp --cov-report=term-missing`

9. Verify SCRUM-5 DoD checklist manually

---

## 4. Verification

- [ ] All unit tests from previous tasks pass
- [ ] Integration tests cover full query flow
- [ ] `conftest.py` provides reusable fixtures
- [ ] `tests/README.md` documents test running
- [ ] `pytest -v` runs all tests successfully
- [ ] Coverage is reasonable on critical paths
- [ ] No flaky tests (deterministic results)
- [ ] Optional real API test skipped by default
- [ ] SCRUM-5 Definition of Done verified:
  - [ ] MCP server connects to Cursor
  - [ ] Queries return ICAET results
  - [ ] Missing credentials show clear errors
  - [ ] Prompts display correctly
  - [ ] No credentials in code
  - [ ] HTTPS communication
  - [ ] No sensitive data logged
