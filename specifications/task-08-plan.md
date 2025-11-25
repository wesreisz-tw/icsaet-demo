# Task 08 Implementation Plan: Testing and Verification

**Story**: SCRUM-5  
**Task ID**: Task 08  
**Task Dependencies**: Task 07 (entry point complete), all previous tasks  
**Created**: 2025-11-25

---

## 1. Issue

Need to create comprehensive test coverage with integration tests, verify all SCRUM-5 acceptance criteria are met, create test documentation, and ensure the complete MCP server functions correctly end-to-end.

---

## 2. Solution

Add integration tests for full query flow, create optional real API test, add test documentation, verify existing unit tests cover critical paths, and systematically check all SCRUM-5 Definition of Done items.

**Technical Rationale**:
- Integration tests verify component interactions
- Use pytest markers to separate unit/integration tests
- Mock external dependencies (httpx) in tests
- Optional real API test can be skipped in CI
- Focus on critical paths (not 100% coverage goal)
- Systematic DoD verification ensures completeness

---

## 3. Implementation Steps

### Step 1: Create Integration Test Directory
**Location**: `/Users/wesleyreisz/work/mcp/icsaet-demo/tests/`
- Create directory: `integration/`

### Step 2: Create Integration Test Init File
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/tests/integration/__init__.py`
- Create empty file

### Step 3: Create End-to-End Query Flow Test
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/tests/integration/test_query_flow.py`
- Create new file with content:
  ```python
  """Integration tests for full query flow."""

  from unittest.mock import MagicMock, patch

  import pytest

  from icsaet_mcp.tools import query


  @pytest.mark.integration
  def test_full_query_flow_with_valid_config(monkeypatch):
      """Arrange: Valid environment variables and mocked API response
      Act: Call query tool through full stack
      Assert: Returns answer from API"""
      monkeypatch.setenv("ICAET_API_KEY", "test-api-key-12345")
      monkeypatch.setenv("USER_EMAIL", "test@example.com")

      with patch("httpx.Client") as mock_client:
          mock_response = MagicMock()
          mock_response.json.return_value = {"answer": "Integration test answer"}
          mock_client.return_value.__enter__.return_value.post.return_value = (
              mock_response
          )

          result = query("What is ICAET?")

          assert result == "Integration test answer"
          mock_client.return_value.__enter__.return_value.post.assert_called_once()


  @pytest.mark.integration
  def test_full_query_flow_with_missing_config():
      """Arrange: Missing environment variables
      Act: Call query tool
      Assert: Raises RuntimeError with configuration guidance"""
      with patch.dict("os.environ", {}, clear=True):
          with pytest.raises(RuntimeError) as exc_info:
              query("test question")

          assert "Missing configuration" in str(exc_info.value)
          assert "ICAET_API_KEY" in str(exc_info.value)


  @pytest.mark.integration
  def test_full_query_flow_with_api_error(monkeypatch):
      """Arrange: Valid config but API returns error
      Act: Call query tool
      Assert: Raises RuntimeError with helpful message"""
      monkeypatch.setenv("ICAET_API_KEY", "test-key")
      monkeypatch.setenv("USER_EMAIL", "test@example.com")

      with patch("httpx.Client") as mock_client:
          import httpx

          mock_response = MagicMock()
          mock_response.status_code = 500
          mock_client.return_value.__enter__.return_value.post.side_effect = (
              httpx.HTTPStatusError(
                  "Server error", request=MagicMock(), response=mock_response
              )
          )

          with pytest.raises(RuntimeError) as exc_info:
              query("test question")

          assert "API error" in str(exc_info.value)


  @pytest.mark.integration
  def test_server_startup_validation(monkeypatch):
      """Arrange: Valid configuration environment
      Act: Import server module
      Assert: Server initializes without errors"""
      monkeypatch.setenv("ICAET_API_KEY", "test-key")
      monkeypatch.setenv("USER_EMAIL", "test@example.com")

      from icsaet_mcp.server import mcp

      assert mcp is not None
      assert mcp.name == "icsaet"
      assert len(mcp._tools) == 1
      assert len(mcp._prompts) >= 3


  @pytest.mark.integration
  def test_prompt_content_integration():
      """Arrange: Server with registered prompts
      Act: Call each prompt function
      Assert: All prompts return substantial content"""
      from icsaet_mcp.server import (
          example_questions,
          formatting_guidance,
          icaet_overview,
      )

      overview = icaet_overview()
      examples = example_questions()
      guidance = formatting_guidance()

      assert len(overview) > 200
      assert len(examples) > 200
      assert len(guidance) > 200

      assert "ICAET" in overview
      assert "question" in examples.lower()
      assert "tip" in guidance.lower() or "do" in guidance.lower()
  ```

### Step 4: Create Optional Real API Test
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/tests/integration/test_real_api.py`
- Create new file with content:
  ```python
  """Optional integration test against real ICAET API.

  This test is skipped by default and requires:
  - ICAET_API_KEY environment variable
  - USER_EMAIL environment variable
  - Network access to ICAET API

  Run with: pytest -m real_api tests/integration/test_real_api.py
  """

  import os

  import pytest

  from icsaet_mcp.tools import query


  @pytest.mark.real_api
  @pytest.mark.skipif(
      not os.getenv("ICAET_API_KEY") or not os.getenv("USER_EMAIL"),
      reason="Requires ICAET_API_KEY and USER_EMAIL environment variables",
  )
  def test_query_against_real_api():
      """Arrange: Real ICAET credentials in environment
      Act: Call query tool with real question
      Assert: Returns response from real API"""
      result = query("What is ICAET?")

      assert isinstance(result, str)
      assert len(result) > 0

      print(f"\nReal API Response:\n{result}\n")
  ```

### Step 5: Create Pytest Configuration
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/pytest.ini`
- Create new file with content:
  ```ini
  [pytest]
  markers =
      integration: Integration tests that test component interactions
      real_api: Optional tests against real ICAET API (skipped by default)

  testpaths = tests
  python_files = test_*.py
  python_classes = Test*
  python_functions = test_*
  ```

### Step 6: Create Test Documentation
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/tests/README.md`
- Create new file with content:
  ```markdown
  # ICAET MCP Server Tests

  This directory contains unit and integration tests for the ICAET MCP server.

  ## Test Structure

  ```
  tests/
  ├── unit/               # Unit tests for individual modules
  │   ├── test_config.py
  │   ├── test_icaet_client.py (in test_tools.py)
  │   ├── test_tools.py
  │   ├── test_server.py
  │   └── test_main.py
  └── integration/        # Integration tests for component interactions
      ├── test_query_flow.py
      └── test_real_api.py (optional)
  ```

  ## Running Tests

  ### Run All Tests
  ```bash
  pytest
  ```

  ### Run Only Unit Tests
  ```bash
  pytest tests/unit/
  ```

  ### Run Only Integration Tests
  ```bash
  pytest -m integration
  ```

  ### Run with Coverage
  ```bash
  pytest --cov=src/icsaet_mcp --cov-report=html
  ```

  ### Run Optional Real API Test
  Requires `ICAET_API_KEY` and `USER_EMAIL` environment variables:
  ```bash
  export ICAET_API_KEY="your-key"
  export USER_EMAIL="your-email"
  pytest -m real_api tests/integration/test_real_api.py -v
  ```

  ## Test Patterns

  ### AAA Pattern
  All tests follow the Arrange-Act-Assert pattern with comments:

  ```python
  def test_example():
      """Arrange: Description of setup
      Act: Description of action
      Assert: Description of expected result"""
      # Arrange
      setup_code()
      
      # Act
      result = function_under_test()
      
      # Assert
      assert result == expected
  ```

  ### Mocking External Dependencies
  Tests mock external dependencies (httpx, API calls):

  ```python
  from unittest.mock import patch

  def test_with_mock():
      with patch("httpx.Client") as mock_client:
          mock_client.return_value.__enter__.return_value.post.return_value.json.return_value = {"answer": "test"}
          result = query("test")
          assert result == "test"
  ```

  ### Fixtures
  Use pytest fixtures for common setup in `conftest.py` (if needed).

  ## Adding New Tests

  1. Determine if test is unit or integration
  2. Create test file in appropriate directory
  3. Follow AAA pattern with comments
  4. Mock external dependencies
  5. Use descriptive test names
  6. Run tests to verify they pass

  ## Coverage Goals

  Focus on testing critical paths:
  - Configuration validation
  - API client error handling
  - Tool function validation
  - Server initialization
  - Entry point error handling

  Not aiming for 100% coverage, but ensuring important behavior is tested.
  ```

### Step 7: Create Shared Fixtures (if needed)
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/tests/conftest.py`
- Create new file with content:
  ```python
  """Shared pytest fixtures for all tests."""

  import pytest


  @pytest.fixture
  def mock_settings():
      """Provide mock ICAET settings for testing."""
      from unittest.mock import MagicMock

      settings = MagicMock()
      settings.api_key = "test-api-key-12345"
      settings.user_email = "test@example.com"
      settings.api_url = "https://api.example.com/query"
      return settings
  ```

### Step 8: Run All Unit Tests
**Command**: `pytest tests/unit/ -v`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: All unit tests pass (from previous tasks)

### Step 9: Run Integration Tests
**Command**: `pytest -m integration -v`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: All 5 integration tests pass

### Step 10: Run All Tests Together
**Command**: `pytest -v`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: All tests pass (unit + integration)

### Step 11: Generate Coverage Report
**Command**: `pytest --cov=src/icsaet_mcp --cov-report=term-missing`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: Shows coverage report for all modules

### Step 12: Run Linters on All Tests
**Command**: `ruff check tests/`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: Zero errors

### Step 13: Format Check on All Tests
**Command**: `black --check tests/`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: No changes needed

### Step 14: Verify SCRUM-5 Functional DoD
**Manual Check**:
- [ ] MCP server connects to Cursor (verify server starts without errors)
- [ ] Query tool returns ICAET results (verify tests pass)
- [ ] Missing credentials show clear errors (verify test_main.py passes)
- [ ] Multi-turn conversations work (MCP protocol handles this)
- [ ] Prompts display correctly (verify prompt tests pass)

### Step 15: Verify SCRUM-5 Security DoD
**Manual Check**:
- [ ] No credentials in code (check no hardcoded keys in files)
- [ ] HTTPS communication (verify api_url uses https://)
- [ ] No sensitive data logged (check logger calls don't log questions/keys)
- [ ] Environment variables isolated (verify config.py uses pydantic-settings)

### Step 16: Verify SCRUM-5 Operational DoD
**Manual Check**:
- [ ] Simple installation process (verify pyproject.toml correct)
- [ ] MCP server starts/stops cleanly (verify main.py handles signals)
- [ ] End-to-end test passes (verify integration tests pass)

---

## 4. Verification

### Test Coverage
- Unit tests exist for config, tools, server, main
- Integration tests verify full query flow
- Optional real API test available (skipped by default)
- Test documentation complete
- All tests follow AAA pattern with comments

### Test Execution
- `pytest` runs all tests successfully
- `pytest -m integration` runs integration tests
- `pytest --cov` shows reasonable coverage
- All tests complete in under 30 seconds
- No flaky tests

### SCRUM-5 Definition of Done
- All functional DoD items verified
- All security DoD items verified
- All operational DoD items verified
- Tests provide confidence in correctness

### Code Quality
- All test files pass ruff
- All test files pass black
- Tests are deterministic
- No commented-out tests
- Clean fixtures and setup

### Documentation
- tests/README.md explains test structure
- Running tests documented
- Adding new tests documented
- Mock patterns documented

---

## IMPLEMENTATION CHECKLIST

:white_check_mark: 1. Create tests/integration/ directory
:white_check_mark: 2. Create tests/integration/__init__.py
:white_check_mark: 3. Create test_query_flow.py with 5 integration tests
:white_check_mark: 4. Create test_real_api.py with optional real API test
:white_check_mark: 5. Create pytest.ini with test markers configuration
:white_check_mark: 6. Create tests/README.md with comprehensive test documentation
:white_check_mark: 7. Create tests/conftest.py with shared fixtures
:white_check_mark: 8. Run unit tests and verify all pass
:white_check_mark: 9. Run integration tests and verify all pass
:white_check_mark: 10. Run all tests together and verify all pass
:white_check_mark: 11. Generate coverage report and verify reasonable coverage
:white_check_mark: 12. Run ruff on all tests and verify zero errors
:white_check_mark: 13. Run black on all tests and verify no changes needed
:white_check_mark: 14. Verify SCRUM-5 Functional DoD (5 items)
:white_check_mark: 15. Verify SCRUM-5 Security DoD (4 items)
:white_check_mark: 16. Verify SCRUM-5 Operational DoD (3 items)
:white_check_mark: 17. Verify no flaky tests
:white_check_mark: 18. Verify tests complete in reasonable time

