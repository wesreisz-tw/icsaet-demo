# Task 05 Implementation Plan: MCP Query Tool Implementation

**Story**: SCRUM-5  
**Task ID**: Task 05  
**Task Dependencies**: Task 03 (ICAET API client complete), Task 02 (Configuration complete)  
**Created**: 2025-11-25

---

## 1. Issue

Need to implement the MCP `query` tool that integrates the ICAET API client with fastmcp framework, providing a user-facing interface for querying the ICAET knowledge base from Cursor with proper error handling and validation.

---

## 2. Solution

Create a fastmcp-decorated tool function in `tools.py` that accepts a question parameter, validates input, creates an ICAETClient instance, calls the API, and returns formatted responses with user-friendly error messages for any failures.

**Technical Rationale**:
- Use fastmcp @mcp.tool() decorator for automatic MCP protocol integration
- Delegate API communication to ICAETClient (separation of concerns)
- Validate question parameter before making API calls
- Convert exceptions to user-friendly messages (users see these in Cursor)
- Keep tool function thin (business logic in ICAETClient)
- Return string responses (compatible with MCP protocol)

---

## 3. Implementation Steps

### Step 1: Import Required Dependencies
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/src/icsaet_mcp/tools.py`
- Replace entire file content with:
  ```python
  """MCP tool definitions for ICAET queries."""

  import logging
  from typing import Any

  import httpx
  from fastmcp import FastMCP
  from pydantic import ValidationError

  from icsaet_mcp.config import Settings, get_settings

  logger = logging.getLogger(__name__)
  mcp = FastMCP("icsaet")
  ```

### Step 2: Add ICAETClient Class
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/src/icsaet_mcp/tools.py`
- After imports, add:
  ```python


  class ICAETClient:
      """Client for interacting with ICAET API."""

      BASE_URL = "https://icaet-dev.wesleyreisz.com"

      def __init__(self, settings: Settings) -> None:
          self.settings = settings
          self._client = httpx.Client(timeout=30.0, base_url=self.BASE_URL)

      def query(self, question: str) -> dict[str, Any]:
          """Query the ICAET knowledge base."""
          headers = {"x-api-key": self.settings.icaet_api_key}
          payload = {"email": self.settings.user_email, "question": question}

          try:
              response = self._client.post("/query", json=payload, headers=headers)
              response.raise_for_status()
              return response.json()
          except httpx.TimeoutException as e:
              logger.error(f"Request timeout: {e}")
              raise RuntimeError(
                  "Request timed out. The ICAET API is taking too long to respond."
              ) from e
          except httpx.HTTPStatusError as e:
              logger.error(f"HTTP error {e.response.status_code}: {e}")
              if e.response.status_code == 401:
                  raise RuntimeError(
                      "Authentication failed. Please check your ICAET_API_KEY."
                  ) from e
              elif e.response.status_code == 400:
                  raise RuntimeError(
                      "Invalid request. Please check your question format and email."
                  ) from e
              else:
                  raise RuntimeError(
                      f"API error: {e.response.status_code}. Please try again later."
                  ) from e
          except httpx.RequestError as e:
              logger.error(f"Network error: {e}")
              raise RuntimeError(
                  "Network error. Please check your internet connection."
              ) from e
  ```

### Step 3: Add Query Tool Function
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/src/icsaet_mcp/tools.py`
- After ICAETClient class, add:
  ```python


  @mcp.tool()
  def query(question: str) -> str:
      """Query the ICAET knowledge base.

      Args:
          question: A natural language question about ICAET conference content,
                   speakers, topics, or sessions.

      Returns:
          Answer from the ICAET knowledge base.

      Raises:
          ValueError: If question is empty or invalid.
          RuntimeError: If API call fails or configuration is invalid.
      """
      if not question or not question.strip():
          raise ValueError("Question cannot be empty. Please provide a valid question.")

      try:
          settings = get_settings()
      except ValidationError as e:
          logger.error(f"Configuration error: {e}")
          raise RuntimeError(
              "Missing configuration. Please set ICAET_API_KEY and USER_EMAIL "
              "environment variables in your Cursor MCP settings."
          ) from e

      try:
          client = ICAETClient(settings)
          result = client.query(question.strip())

          if isinstance(result, dict) and "answer" in result:
              return result["answer"]
          elif isinstance(result, dict):
              return str(result)
          else:
              return str(result)

      except RuntimeError:
          raise
      except Exception as e:
          logger.error(f"Unexpected error: {e}")
          raise RuntimeError(
              f"An unexpected error occurred: {str(e)}. Please try again."
          ) from e
  ```

### Step 4: Add Module Exports
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/src/icsaet_mcp/tools.py`
- At end of file, add:
  ```python


  __all__ = ["mcp", "query", "ICAETClient"]
  ```

### Step 5: Create Test File
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/tests/unit/test_tools.py`
- Create new file with content:
  ```python
  """Unit tests for MCP tools."""

  from unittest.mock import MagicMock, patch

  import httpx
  import pytest
  from pydantic import ValidationError

  from icsaet_mcp.tools import ICAETClient, query


  def test_query_with_valid_question():
      """Arrange: Valid question and mocked successful API response
      Act: Call query tool
      Assert: Returns answer from API response"""
      with patch("icsaet_mcp.tools.get_settings") as mock_settings, patch(
          "httpx.Client"
      ) as mock_client:
          mock_settings.return_value = MagicMock(
              icaet_api_key="test-key",
              user_email="test@example.com",
          )
          mock_response = MagicMock()
          mock_response.json.return_value = {"answer": "Test answer"}
          mock_client.return_value.post.return_value = mock_response

          result = query("What did Leslie talk about?")

          assert result == "Test answer"


  def test_query_with_empty_question():
      """Arrange: Empty question string
      Act: Call query tool
      Assert: Raises ValueError with helpful message"""
      with pytest.raises(ValueError) as exc_info:
          query("")

      assert "cannot be empty" in str(exc_info.value)


  def test_query_with_whitespace_question():
      """Arrange: Whitespace-only question
      Act: Call query tool
      Assert: Raises ValueError"""
      with pytest.raises(ValueError) as exc_info:
          query("   ")

      assert "cannot be empty" in str(exc_info.value)


  def test_query_with_missing_configuration():
      """Arrange: Missing environment variables (ValidationError from settings)
      Act: Call query tool
      Assert: Raises RuntimeError with configuration guidance"""
      with patch("icsaet_mcp.tools.get_settings") as mock_settings:
          mock_settings.side_effect = ValidationError.from_exception_data(
              "Settings", [{"type": "missing", "loc": ("ICAET_API_KEY",), "input": {}}]
          )

          with pytest.raises(RuntimeError) as exc_info:
              query("test question")

          assert "Missing configuration" in str(exc_info.value)
          assert "ICAET_API_KEY" in str(exc_info.value)


  def test_query_with_api_timeout():
      """Arrange: API call times out
      Act: Call query tool
      Assert: Raises RuntimeError with timeout message"""
      with patch("icsaet_mcp.tools.get_settings") as mock_settings, patch(
          "httpx.Client"
      ) as mock_client:
          mock_settings.return_value = MagicMock(
              icaet_api_key="test-key",
              user_email="test@example.com",
          )
          mock_client.return_value.post.side_effect = httpx.TimeoutException("Timeout")

          with pytest.raises(RuntimeError) as exc_info:
              query("test question")

          assert "timed out" in str(exc_info.value).lower()


  def test_query_with_401_error():
      """Arrange: API returns 401 Unauthorized
      Act: Call query tool
      Assert: Raises RuntimeError with authentication message"""
      with patch("icsaet_mcp.tools.get_settings") as mock_settings, patch(
          "httpx.Client"
      ) as mock_client:
          mock_settings.return_value = MagicMock(
              icaet_api_key="invalid-key",
              user_email="test@example.com",
          )
          mock_response = MagicMock()
          mock_response.status_code = 401
          mock_client.return_value.post.side_effect = httpx.HTTPStatusError(
              "Unauthorized", request=MagicMock(), response=mock_response
          )

          with pytest.raises(RuntimeError) as exc_info:
              query("test question")

          assert "Authentication failed" in str(exc_info.value)


  def test_icaet_client_query_success():
      """Arrange: ICAETClient with valid settings and mocked successful response
      Act: Call client.query()
      Assert: Returns parsed JSON response"""
      settings = MagicMock(
          icaet_api_key="test-key",
          user_email="test@example.com",
      )
      
      with patch("httpx.Client") as mock_client:
          mock_response = MagicMock()
          mock_response.json.return_value = {"answer": "Test answer"}
          mock_client.return_value.post.return_value = mock_response
          
          client = ICAETClient(settings)
          result = client.query("test question")

          assert result == {"answer": "Test answer"}


  def test_icaet_client_strips_whitespace():
      """Arrange: Question with leading/trailing whitespace
      Act: Call query tool
      Assert: Whitespace is stripped before API call"""
      with patch("icsaet_mcp.tools.get_settings") as mock_settings, patch(
          "httpx.Client"
      ) as mock_client:
          mock_settings.return_value = MagicMock(
              icaet_api_key="test-key",
              user_email="test@example.com",
          )
          mock_response = MagicMock()
          mock_response.json.return_value = {"answer": "Test"}
          mock_client.return_value.post.return_value = mock_response

          query("  test question  ")

          call_args = mock_client.return_value.post.call_args.kwargs
          assert call_args["json"]["question"] == "test question"
  ```

### Step 6: Run Tests
**Command**: `pytest tests/unit/test_tools.py -v`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: All tests pass

### Step 7: Run Linter
**Command**: `ruff check src/icsaet_mcp/tools.py tests/unit/test_tools.py`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: Zero errors

### Step 8: Run Formatter
**Command**: `black --check src/icsaet_mcp/tools.py tests/unit/test_tools.py`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: No changes needed

### Step 9: Run Type Checker
**Command**: `mypy src/icsaet_mcp/tools.py`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: Zero type errors

### Step 10: Verify Tool Registration
**Command**: `python -c "from icsaet_mcp.tools import mcp; print(f'Tools registered: {len(mcp._tools)}')"`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: Prints "Tools registered: 1"

---

## 4. Verification

### Tool Function Implementation
- Function name is `query`
- Decorated with `@mcp.tool()`
- Function signature: `(question: str) -> str`
- Full type hints on parameters and return value
- Comprehensive docstring with Args, Returns, Raises sections

### Parameter Validation
- Rejects empty strings with ValueError
- Rejects whitespace-only strings with ValueError
- Strips leading/trailing whitespace before processing
- Clear error message guides user to provide valid question

### ICAETClient Integration
- Creates ICAETClient instance with settings
- Calls `client.query(question)` method
- Extracts "answer" field from JSON response
- Handles various response formats (dict with answer, other dict, other types)

### Error Handling
- Catches ValidationError from get_settings() and converts to RuntimeError
- Catches TimeoutException and provides user-friendly message
- Catches HTTPStatusError and provides specific messages for 401, 400, other codes
- Catches RequestError and provides network error message
- Catches general Exception and provides fallback error message
- All error messages guide users to resolution

### Code Quality
- All tests pass
- ruff reports zero errors
- black reports no formatting changes needed
- mypy reports zero type errors
- Tool is registered with fastmcp (mcp._tools contains 1 tool)
- Follows AAA test pattern with comments

---

## IMPLEMENTATION CHECKLIST

:white_check_mark: 1. Add imports (logging, typing, httpx, fastmcp, pydantic, config)
:white_check_mark: 2. Create logger instance
:white_check_mark: 3. Create FastMCP instance named "icsaet"
:white_check_mark: 4. Implement ICAETClient class with __init__ and query methods
:white_check_mark: 5. Add comprehensive error handling in ICAETClient.query (timeout, HTTP errors, network errors)
:white_check_mark: 6. Implement @mcp.tool() decorated query function
:white_check_mark: 7. Add docstring to query function with Args, Returns, Raises
:white_check_mark: 8. Add question validation (empty/whitespace check)
:white_check_mark: 9. Add configuration validation (catch ValidationError from get_settings)
:white_check_mark: 10. Add API call with error handling
:white_check_mark: 11. Add response formatting (extract "answer" field)
:white_check_mark: 12. Add __all__ exports
:white_check_mark: 13. Create test_tools.py with 9 test cases
:white_check_mark: 14. Run pytest and verify all tests pass
:white_check_mark: 15. Run ruff and verify zero errors
:white_check_mark: 16. Run black and verify no changes needed
:white_check_mark: 17. Run mypy and verify zero type errors
:white_check_mark: 18. Verify tool is registered with fastmcp

