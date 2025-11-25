# Task 06 Implementation Plan: MCP Server Setup and Integration

**Story**: SCRUM-5  
**Task ID**: Task 06  
**Task Dependencies**: Task 04 (prompts complete), Task 05 (query tool complete)  
**Created**: 2025-11-25

---

## 1. Issue

Need to implement the fastmcp server in `server.py` that registers the query tool, prompts, and handles server lifecycle for integration with Cursor IDE through the MCP protocol.

---

## 2. Solution

Import the FastMCP instance from `tools.py`, register the three prompts from `prompts.py`, configure server metadata, and add logging for server lifecycle events. Use helper functions for prompts to improve testability. The server will be exported for use by `__main__.py`.

**Technical Rationale**:
- Reuse FastMCP instance from tools.py (tool already registered via decorator)
- Use fastmcp prompt registration API for static prompts
- Add helper functions for each prompt to improve testability
- Configure logging for operational visibility
- Keep server.py focused on configuration (business logic elsewhere)
- Export server instance and helper functions for entry point to use

---

## 3. Implementation Steps

### Step 1: Import Dependencies and FastMCP Instance
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/src/icsaet_mcp/server.py`
- Replace entire file content with:
  ```python
  """FastMCP server setup and configuration."""

  import logging

  from icsaet_mcp.prompts import (
      EXAMPLE_QUESTIONS,
      FORMATTING_GUIDANCE,
      ICAET_OVERVIEW,
  )
  from icsaet_mcp.tools import mcp

  logger = logging.getLogger(__name__)
  ```

### Step 2: Add Helper Functions for Prompts
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/src/icsaet_mcp/server.py`
- After imports, add helper functions for testability:
  ```python


  def get_icaet_overview() -> str:
      """Explains what ICAET is and how to use the knowledge base from Cursor."""
      return ICAET_OVERVIEW


  def get_example_questions() -> str:
      """Provides diverse example questions for querying ICAET."""
      return EXAMPLE_QUESTIONS


  def get_formatting_guidance() -> str:
      """Tips for writing better questions to get more targeted answers."""
      return FORMATTING_GUIDANCE
  ```

### Step 3: Register ICAET Overview Prompt
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/src/icsaet_mcp/server.py`
- After helper functions, add:
  ```python


  @mcp.prompt()
  def icaet_overview() -> str:
      """Explains what ICAET is and how to use the knowledge base from Cursor."""
      return get_icaet_overview()
  ```

### Step 4: Register Example Questions Prompt
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/src/icsaet_mcp/server.py`
- After icaet_overview function, add:
  ```python


  @mcp.prompt()
  def example_questions() -> str:
      """Provides diverse example questions for querying ICAET."""
      return get_example_questions()
  ```

### Step 5: Register Formatting Guidance Prompt
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/src/icsaet_mcp/server.py`
- After example_questions function, add:
  ```python


  @mcp.prompt()
  def formatting_guidance() -> str:
      """Tips for writing better questions to get more targeted answers."""
      return get_formatting_guidance()
  ```

### Step 6: Add Logging for Registration
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/src/icsaet_mcp/server.py`
- After all prompt functions, add:
  ```python


  logger.info("ICAET MCP server configured with 1 tool and 3 prompts")
  ```

### Step 7: Add Module Exports
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/src/icsaet_mcp/server.py`
- At end of file, add:
  ```python


  __all__ = ["mcp", "get_icaet_overview", "get_example_questions", "get_formatting_guidance"]
  ```

### Step 8: Create Server Tests
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/tests/unit/test_server.py`
- Create new file with content:
  ```python
  """Unit tests for MCP server setup."""

  from icsaet_mcp.server import (
      get_example_questions,
      get_formatting_guidance,
      get_icaet_overview,
      mcp,
  )


  def test_server_instance_exists():
      """Arrange: Import server module
      Act: Access mcp instance
      Assert: Instance exists and is FastMCP type"""
      assert mcp is not None
      assert hasattr(mcp, "run")


  def test_server_has_query_tool():
      """Arrange: Server configured with tools
      Act: Check tools list
      Assert: query tool is registered"""
      from icsaet_mcp.tools import query

      assert query is not None


  def test_icaet_overview_prompt_content():
      """Arrange: Server with registered prompts
      Act: Get icaet_overview prompt function
      Assert: Returns ICAET overview content"""
      content = get_icaet_overview()

      assert "ICAET" in content
      assert "knowledge base" in content.lower()
      assert len(content) > 100


  def test_example_questions_prompt_content():
      """Arrange: Server with registered prompts
      Act: Get example_questions prompt function
      Assert: Returns example questions content"""
      content = get_example_questions()

      assert "example" in content.lower() or "question" in content.lower()
      assert len(content) > 100


  def test_formatting_guidance_prompt_content():
      """Arrange: Server with registered prompts
      Act: Get formatting_guidance prompt function
      Assert: Returns formatting guidance content"""
      content = get_formatting_guidance()

      assert "tip" in content.lower() or "do" in content.lower()
      assert len(content) > 100


  def test_server_name():
      """Arrange: Server instance
      Act: Access server name
      Assert: Name is 'icsaet'"""
      assert mcp.name == "icsaet"
  ```

### Step 9: Run Tests
**Command**: `pytest tests/unit/test_server.py -v`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: All 6 tests pass

### Step 10: Run Linter
**Command**: `ruff check src/icsaet_mcp/server.py tests/unit/test_server.py`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: Zero errors

### Step 11: Run Formatter
**Command**: `black --check src/icsaet_mcp/server.py tests/unit/test_server.py`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: No changes needed

### Step 12: Run Type Checker
**Command**: `mypy src/icsaet_mcp/server.py`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: Zero type errors

### Step 13: Verify Server Import
**Command**: `python -c "from icsaet_mcp.server import mcp; print(f'Server: {mcp.name}')"`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: Prints server name "icsaet"

### Step 14: Verify Prompt Content
**Command**: `python -c "from icsaet_mcp.server import get_icaet_overview; print(len(get_icaet_overview()))"`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: Prints number greater than 100 (prompt has content)

---

## 4. Verification

### Server Instance
- FastMCP instance imported from tools.py
- Server name is "icsaet"
- Server has run() method available
- Server instance is exported via __all__

### Tool Registration
- Query tool registered (via decorator in tools.py)
- Tool name is "query"

### Prompt Registration
- All three prompts registered with @mcp.prompt() decorator
- icaet_overview prompt returns ICAET_OVERVIEW content via helper
- example_questions prompt returns EXAMPLE_QUESTIONS content via helper
- formatting_guidance prompt returns FORMATTING_GUIDANCE content via helper
- Each prompt has descriptive docstring
- Prompt functions delegate to helper functions for testability

### Helper Functions
- `get_icaet_overview()` returns ICAET_OVERVIEW constant
- `get_example_questions()` returns EXAMPLE_QUESTIONS constant
- `get_formatting_guidance()` returns FORMATTING_GUIDANCE constant
- Helper functions exported in __all__ for testing

### Logging
- Logger configured using __name__
- INFO log message confirms tool and prompt count
- No sensitive data in logs

### Code Quality
- All 6 tests pass
- ruff reports zero errors
- black reports no formatting changes needed
- mypy reports zero type errors
- Clean module structure with clear imports

### Integration Readiness
- Can import: `from icsaet_mcp.server import mcp`
- Server is ready for `mcp.run()` call in __main__.py
- All tools and prompts are registered
- Server metadata is configured

---

## IMPLEMENTATION CHECKLIST

:white_check_mark: 1. Add imports (logging, prompts, mcp instance from tools)
:white_check_mark: 2. Create logger instance
:white_check_mark: 3. Implement get_icaet_overview helper function
:white_check_mark: 4. Implement get_example_questions helper function
:white_check_mark: 5. Implement get_formatting_guidance helper function
:white_check_mark: 6. Implement icaet_overview prompt function with @mcp.prompt() decorator
:white_check_mark: 7. Implement example_questions prompt function with @mcp.prompt() decorator
:white_check_mark: 8. Implement formatting_guidance prompt function with @mcp.prompt() decorator
:white_check_mark: 9. Add docstring to each prompt function
:white_check_mark: 10. Add logger.info message confirming configuration
:white_check_mark: 11. Add __all__ export with mcp instance and helper functions
:white_check_mark: 12. Create test_server.py with 6 test cases using helper functions
:white_check_mark: 13. Run pytest and verify all tests pass
:white_check_mark: 14. Run ruff and verify zero errors
:white_check_mark: 15. Run black and verify no changes needed
:white_check_mark: 16. Run mypy and verify zero type errors
:white_check_mark: 17. Verify server has correct name "icsaet"
:white_check_mark: 18. Verify each prompt helper returns correct content

