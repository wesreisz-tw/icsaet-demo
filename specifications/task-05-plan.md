# Task 05 Implementation Plan: MCP Query Tool Implementation

**Story**: SCRUM-5 - Cursor MCP Server for ICAET Query Access  
**Task**: 05 - MCP Query Tool Implementation

---

## 1. Issue

Implement the MCP `query` tool that integrates `ICAETClient` with the fastmcp framework, providing the user-facing interface for querying ICAET from Cursor.

---

## 2. Solution

Add the `query_icaet()` tool function in `tools.py` using fastmcp's `@mcp.tool()` decorator. The function validates input, creates `ICAETClient` with settings, calls the API, and returns formatted results. Error handling converts all exceptions to user-friendly messages suitable for display in Cursor.

---

## 3. Implementation Steps

1. Update `src/icsaet_mcp/tools.py` to add query tool:
   - Import `json` for response formatting
   - Import `pydantic.ValidationError` for config error handling
   - Add at module level: `mcp = FastMCP("icsaet")` (will be imported by server.py)
   - Note: FastMCP import and initialization will be done here so tools can use the decorator

2. Implement `query_icaet()` function (before ICAETClient class):
   ```python
   @mcp.tool(name="query", description="Query the ICAET knowledge base")
   def query_icaet(question: str) -> str:
   ```
   - Docstring: "Query the ICAET knowledge base with a natural language question."
   - Parameter `question`: the question to ask (required string)
   - Return type: `str` (JSON-formatted response)

3. Implement function body:
   - Validate question: if empty or whitespace-only, return error message string (single validation point - ICAETClient trusts this)
   - Try block:
     - Call `get_settings()` to get configuration
     - Create `ICAETClient(settings)`
     - Call `client.query(question)`
     - Return `json.dumps(result, indent=2)` for readable output
   - Except `ValidationError`: return "Configuration error: Please ensure ICAET_API_KEY and USER_EMAIL are set in your Cursor MCP configuration."
   - Except `RuntimeError` as e: return `str(e)` (already user-friendly from ICAETClient)
   - Except `Exception`: log exception, return "An unexpected error occurred. Please try again."

4. Create/update `tests/unit/test_tools.py`:
   - Import pytest, unittest.mock (patch, MagicMock)
   - Test: `test_query_success` - mock ICAETClient.query to return dict, verify JSON response
   - Test: `test_query_empty_question` - pass "", verify returns error message
   - Test: `test_query_whitespace_question` - pass "   ", verify returns error message
   - Test: `test_query_config_error` - mock get_settings to raise ValidationError, verify message
   - Test: `test_query_api_error` - mock ICAETClient.query to raise RuntimeError, verify message propagated
   - Test: `test_tool_metadata` - verify tool has name "query" and description

5. Run `pytest tests/unit/test_tools.py -v`

6. Run `ruff check src/icsaet_mcp/tools.py` and `mypy src/icsaet_mcp/tools.py`

---

## 4. Verification

- [ ] Tool decorated with `@mcp.tool(name="query")`
- [ ] Tool accepts single `question` parameter (string)
- [ ] Empty/whitespace questions return error message (not exception)
- [ ] Configuration errors return helpful setup message
- [ ] API errors return user-friendly messages
- [ ] Successful queries return JSON-formatted response
- [ ] All unit tests pass
- [ ] `ruff check` and `mypy` pass
- [ ] Tool is callable directly for testing
