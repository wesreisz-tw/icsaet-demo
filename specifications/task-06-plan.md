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

Import the FastMCP instance from `tools.py`, register the three prompts from `prompts.py`, configure server metadata, and add logging for server lifecycle events. The server will be exported for use by `__main__.py`.

**Technical Rationale**:
- Reuse FastMCP instance from tools.py (tool already registered via decorator)
- Use fastmcp prompt registration API for static prompts
- Configure logging for operational visibility
- Keep server.py focused on configuration (business logic elsewhere)
- Export server instance for entry point to use

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

### Step 2: Register ICAET Overview Prompt
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/src/icsaet_mcp/server.py`
- After imports, add:
  ```python


  @mcp.prompt()
  def icaet_overview() -> str:
      """Explains what ICAET is and how to use the knowledge base from Cursor."""
      return ICAET_OVERVIEW
  ```

### Step 3: Register Example Questions Prompt
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/src/icsaet_mcp/server.py`
- After icaet_overview function, add:
  ```python


  @mcp.prompt()
  def example_questions() -> str:
      """Provides diverse example questions for querying ICAET."""
      return EXAMPLE_QUESTIONS
  ```

### Step 4: Register Formatting Guidance Prompt
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/src/icsaet_mcp/server.py`
- After example_questions function, add:
  ```python


  @mcp.prompt()
  def formatting_guidance() -> str:
      """Tips for writing better questions to get more targeted answers."""
      return FORMATTING_GUIDANCE
  ```

### Step 5: Add Logging for Registration
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/src/icsaet_mcp/server.py`
- After all prompt functions, add:
  ```python


  logger.info("ICAET MCP server configured with 1 tool and 3 prompts")
  ```

### Step 6: Add Module Exports
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/src/icsaet_mcp/server.py`
- At end of file, add:
  ```python


  __all__ = ["mcp"]
  ```

### Step 7: Create Server Tests
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/tests/unit/test_server.py`
- Create new file with content:
  ```python
  """Unit tests for MCP server setup."""

  from icsaet_mcp.server import mcp


  def test_server_instance_exists():
      """Arrange: Import server module
      Act: Access mcp instance
      Assert: Instance exists and is FastMCP type"""
      assert mcp is not None
      assert hasattr(mcp, "run")
      assert hasattr(mcp, "_tools")
      assert hasattr(mcp, "_prompts")


  def test_server_has_query_tool():
      """Arrange: Server configured with tools
      Act: Check tools list
      Assert: query tool is registered"""
      assert len(mcp._tools) == 1
      tool_names = [tool.name for tool in mcp._tools]
      assert "query" in tool_names


  def test_server_has_all_prompts():
      """Arrange: Server configured with prompts
      Act: Check prompts list
      Assert: All three prompts are registered"""
      assert len(mcp._prompts) >= 3
      prompt_names = [prompt.name for prompt in mcp._prompts]
      assert "icaet_overview" in prompt_names
      assert "example_questions" in prompt_names
      assert "formatting_guidance" in prompt_names


  def test_icaet_overview_prompt_content():
      """Arrange: Server with registered prompts
      Act: Get icaet_overview prompt function
      Assert: Returns ICAET overview content"""
      from icsaet_mcp.server import icaet_overview

      content = icaet_overview()

      assert "ICAET" in content
      assert "knowledge base" in content.lower()
      assert len(content) > 100


  def test_example_questions_prompt_content():
      """Arrange: Server with registered prompts
      Act: Get example_questions prompt function
      Assert: Returns example questions content"""
      from icsaet_mcp.server import example_questions

      content = example_questions()

      assert "example" in content.lower() or "question" in content.lower()
      assert len(content) > 100


  def test_formatting_guidance_prompt_content():
      """Arrange: Server with registered prompts
      Act: Get formatting_guidance prompt function
      Assert: Returns formatting guidance content"""
      from icsaet_mcp.server import formatting_guidance

      content = formatting_guidance()

      assert "tip" in content.lower() or "do" in content.lower()
      assert len(content) > 100


  def test_server_name():
      """Arrange: Server instance
      Act: Access server name
      Assert: Name is 'icsaet'"""
      assert mcp.name == "icsaet"
  ```

### Step 8: Run Tests
**Command**: `pytest tests/unit/test_server.py -v`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: All 7 tests pass

### Step 9: Run Linter
**Command**: `ruff check src/icsaet_mcp/server.py tests/unit/test_server.py`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: Zero errors

### Step 10: Run Formatter
**Command**: `black --check src/icsaet_mcp/server.py tests/unit/test_server.py`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: No changes needed

### Step 11: Run Type Checker
**Command**: `mypy src/icsaet_mcp/server.py`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: Zero type errors

### Step 12: Verify Server Import
**Command**: `python -c "from icsaet_mcp.server import mcp; print(f'Server: {mcp.name}, Tools: {len(mcp._tools)}, Prompts: {len(mcp._prompts)}')"`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: Prints server name "icsaet", 1 tool, 3 prompts

### Step 13: Verify Prompt Content
**Command**: `python -c "from icsaet_mcp.server import icaet_overview; print(len(icaet_overview()))"`
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
- Can access mcp._tools and verify 1 tool present
- Tool name is "query"

### Prompt Registration
- All three prompts registered with @mcp.prompt() decorator
- icaet_overview prompt returns ICAET_OVERVIEW content
- example_questions prompt returns EXAMPLE_QUESTIONS content
- formatting_guidance prompt returns FORMATTING_GUIDANCE content
- Each prompt has descriptive docstring
- Prompt functions are simple wrappers (return constants)

### Logging
- Logger configured using __name__
- INFO log message confirms tool and prompt count
- No sensitive data in logs

### Code Quality
- All 7 tests pass
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
:white_check_mark: 3. Implement icaet_overview prompt function with @mcp.prompt() decorator
:white_check_mark: 4. Implement example_questions prompt function with @mcp.prompt() decorator
:white_check_mark: 5. Implement formatting_guidance prompt function with @mcp.prompt() decorator
:white_check_mark: 6. Add docstring to each prompt function
:white_check_mark: 7. Add logger.info message confirming configuration
:white_check_mark: 8. Add __all__ export with mcp instance
:white_check_mark: 9. Create test_server.py with 7 test cases
:white_check_mark: 10. Run pytest and verify all tests pass
:white_check_mark: 11. Run ruff and verify zero errors
:white_check_mark: 12. Run black and verify no changes needed
:white_check_mark: 13. Run mypy and verify zero type errors
:white_check_mark: 14. Verify server has correct name "icsaet"
:white_check_mark: 15. Verify 1 tool registered
:white_check_mark: 16. Verify 3 prompts registered
:white_check_mark: 17. Verify each prompt returns correct content

