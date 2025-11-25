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

  import httpx
  import pytest

  from icsaet_mcp.tools import query_icaet


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
          mock_client.return_value.post.return_value = mock_response

          from icsaet_mcp.config import get_settings

          get_settings.cache_clear()

          result = query_icaet("What is ICAET?")

          assert result == "Integration test answer"
          mock_client.return_value.post.assert_called_once()


  @pytest.mark.integration
  def test_full_query_flow_with_missing_config():
      """Arrange: Missing environment variables
      Act: Call query tool
      Assert: Raises RuntimeError with configuration guidance"""
      from icsaet_mcp.config import get_settings

      get_settings.cache_clear()

      with patch.dict("os.environ", {}, clear=True):
          with pytest.raises(RuntimeError) as exc_info:
              query_icaet("test question")

          assert "Missing configuration" in str(exc_info.value)
          assert "ICAET_API_KEY" in str(exc_info.value)


  @pytest.mark.integration
  def test_full_query_flow_with_api_error(monkeypatch):
      """Arrange: Valid config but API returns error
      Act: Call query tool
      Assert: Raises RuntimeError with helpful message"""
      monkeypatch.setenv("ICAET_API_KEY", "test-key-12345")
      monkeypatch.setenv("USER_EMAIL", "test@example.com")

      with patch("httpx.Client") as mock_client:
          mock_response = MagicMock()
          mock_response.status_code = 500
          mock_client.return_value.post.side_effect = httpx.HTTPStatusError(
              "Server error", request=MagicMock(), response=mock_response
          )

          from icsaet_mcp.config import get_settings

          get_settings.cache_clear()

          with pytest.raises(RuntimeError) as exc_info:
              query_icaet("test question")

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


  @pytest.mark.integration
  def test_prompt_content_integration():
      """Arrange: Server with registered prompts
      Act: Call each prompt function
      Assert: All prompts return substantial content"""
      from icsaet_mcp.server import (
          get_example_questions,
          get_formatting_guidance,
          get_icaet_overview,
      )

      overview = get_icaet_overview()
      examples = get_example_questions()
      guidance = get_formatting_guidance()

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

  from icsaet_mcp.tools import query_icaet


  @pytest.mark.real_api
  @pytest.mark.skipif(
      not os.getenv("ICAET_API_KEY") or not os.getenv("USER_EMAIL"),
      reason="Requires ICAET_API_KEY and USER_EMAIL environment variables",
  )
  def test_query_against_real_api():
      """Arrange: Real ICAET credentials in environment
      Act: Call query tool with real question
      Assert: Returns response from real API"""
      result = query_icaet("What is ICAET?")

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

  ### Run With Coverage
  ```bash
  pytest --cov=icsaet_mcp --cov-report=term-missing
  ```

  ### Run Real API Tests (Optional)
  ```bash
  # Set environment variables first
  export ICAET_API_KEY="your-api-key"
  export USER_EMAIL="your-email@example.com"

  # Run real API tests
  pytest -m real_api tests/integration/test_real_api.py -v -s
  ```

  ## Test Categories

  ### Unit Tests

  Test individual components in isolation with mocked dependencies:

  - **test_config.py**: Configuration loading and validation
  - **test_tools.py**: ICAETClient HTTP client and query tool
  - **test_server.py**: FastMCP server setup and prompt registration
  - **test_main.py**: Entry point and server lifecycle

  ### Integration Tests

  Test component interactions and full workflows:

  - **test_query_flow.py**: End-to-end query flow with mocked API
  - **test_real_api.py**: Optional real API test (requires credentials)

  ## Writing Tests

  All tests follow the AAA (Arrange-Act-Assert) pattern with explicit comments:

  ```python
  def test_example():
      """Arrange: Setup test conditions
      Act: Execute the action being tested
      Assert: Verify the results"""
      # Arrange
      input_data = "test"
      
      # Act
      result = function_under_test(input_data)
      
      # Assert
      assert result == expected_output
  ```

  ## Test Configuration

  Test configuration is managed through:
  - `pytest.ini`: Pytest configuration and markers
  - `pyproject.toml`: Test dependencies and coverage settings
  - Environment variables: Test credentials and settings

  ## CI/CD

  Tests run in CI with the following characteristics:
  - All unit tests run on every commit
  - Integration tests run with mocked dependencies
  - Real API tests are skipped (require credentials)
  - Coverage threshold: Critical paths covered (not 100%)
  ```

### Step 7: Run All Unit Tests
**Command**: `pytest tests/unit/ -v`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: All unit tests pass (from previous tasks)

### Step 8: Run Integration Tests
**Command**: `pytest -m integration -v`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: All 5 integration tests pass

### Step 9: Run All Tests Together
**Command**: `pytest -v`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: All tests pass (unit + integration)

### Step 10: Generate Coverage Report
**Command**: `pytest --cov=icsaet_mcp --cov-report=term-missing`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: Shows coverage report for all modules

### Step 11: Run Linters on All Tests
**Command**: `ruff check tests/`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: Zero errors

### Step 12: Format Check on All Tests
**Command**: `black --check tests/`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: No changes needed

### Step 13: Verify SCRUM-5 Functional DoD
**Manual Check**:
- [x] MCP server connects to Cursor (verify server starts without errors)
- [x] Query tool returns ICAET results (verify tests pass)
- [x] Missing credentials show clear errors (verify test_main.py passes)
- [x] Multi-turn conversations work (MCP protocol handles this)
- [x] Prompts display correctly (verify prompt tests pass)

### Step 14: Verify SCRUM-5 Security DoD
**Manual Check**:
- [x] No credentials in code (check no hardcoded keys in files)
- [x] HTTPS communication (verify BASE_URL uses https://)
- [x] No sensitive data logged (check logger calls don't log questions/keys)
- [x] Environment variables isolated (verify config.py uses pydantic-settings)

### Step 15: Verify SCRUM-5 Operational DoD
**Manual Check**:
- [x] Simple installation process (verify pyproject.toml correct)
- [x] MCP server starts/stops cleanly (verify main.py handles signals)
- [x] End-to-end test passes (verify integration tests pass)

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
:white_check_mark: 3. Create test_query_flow.py with 5 integration tests using query_icaet
:white_check_mark: 4. Create test_real_api.py with optional real API test using query_icaet
:white_check_mark: 5. Create pytest.ini with test markers configuration
:white_check_mark: 6. Create tests/README.md with comprehensive test documentation
:white_check_mark: 7. Run unit tests and verify all pass
:white_check_mark: 8. Run integration tests and verify all pass
:white_check_mark: 9. Run all tests together and verify all pass
:white_check_mark: 10. Generate coverage report and verify reasonable coverage
:white_check_mark: 11. Run ruff on all tests and verify zero errors
:white_check_mark: 12. Run black on all tests and verify no changes needed
:white_check_mark: 13. Verify SCRUM-5 Functional DoD (5 items)
:white_check_mark: 14. Verify SCRUM-5 Security DoD (4 items)
:white_check_mark: 15. Verify SCRUM-5 Operational DoD (3 items)
:white_check_mark: 16. Verify no flaky tests
:white_check_mark: 17. Verify tests complete in reasonable time

