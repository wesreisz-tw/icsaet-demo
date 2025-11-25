# Task 05: MCP Query Tool Implementation

**Story**: SCRUM-5 - Cursor MCP Server for ICAET Query Access  
**Task Sequence**: 5 of 9  
**Dependencies**: Task 03 (ICAET API client complete)

---

## Objective

Implement the MCP `query` tool that integrates the ICAET API client with fastmcp framework, providing a user-facing interface for querying the ICAET knowledge base from Cursor.

---

## Scope

- Create MCP tool function in `tools.py` (alongside ICAETClient)
- Register tool with fastmcp using decorators
- Define tool schema (name, description, parameters)
- Integrate ICAETClient for API calls
- Handle errors gracefully with user-friendly messages
- Return formatted responses to Cursor
- Add basic validation for question parameter

---

## Acceptance Criteria

1. **Tool Function Definition**
   - [ ] Function name: `query_icaet` or similar
   - [ ] Decorated with fastmcp tool decorator
   - [ ] Function signature: `(question: str) -> str` or returns dict
   - [ ] Proper type hints on parameters and return value

2. **Tool Metadata**
   - [ ] Tool name: `query` (as specified in SCRUM-5)
   - [ ] Clear description: "Query the ICAET knowledge base"
   - [ ] Parameter description explains what questions to ask
   - [ ] Metadata visible in Cursor's tool list

3. **Parameter Validation**
   - [ ] Question parameter is required
   - [ ] Rejects empty or whitespace-only questions
   - [ ] Validates question is a string
   - [ ] Returns clear error for invalid input

4. **Integration with ICAETClient**
   - [ ] Creates/gets ICAETClient instance with settings
   - [ ] Calls `client.query(question)` method
   - [ ] Passes question through without modification
   - [ ] Returns API response to Cursor

5. **Error Handling**
   - [ ] Catches configuration errors (missing env vars)
   - [ ] Catches API client errors (network, timeout, HTTP errors)
   - [ ] Returns user-friendly error messages (not stack traces)
   - [ ] Includes troubleshooting hints in error messages
   - [ ] Distinguishes between config errors vs API errors

6. **Response Formatting**
   - [ ] Returns API response in Cursor-friendly format
   - [ ] JSON responses are properly formatted
   - [ ] Large responses are handled gracefully
   - [ ] Response includes relevant information from API

7. **Testing**
   - [ ] Unit test: Valid question returns expected response
   - [ ] Unit test: Empty question returns error
   - [ ] Unit test: API client error handled gracefully
   - [ ] Unit test: Missing configuration handled gracefully
   - [ ] Unit test: Tool metadata is correct
   - [ ] Tests mock ICAETClient and settings

8. **Code Quality**
   - [ ] Full type hints
   - [ ] Docstring on tool function
   - [ ] Follows Python style guide
   - [ ] Passes ruff, black, mypy checks
   - [ ] Self-documenting code (no comments)

---

## Required Inputs

**From Task 03**:
- Working `ICAETClient` class with `query()` method
- Error handling patterns
- Test patterns for mocking API client

**From Task 02**:
- Working `get_settings()` function
- Configuration validation

---

## Expected Outputs

### Tool Implementation in tools.py
```python
# Key components (not full implementation):
- @mcp.tool() decorated function
- Tool name: "query"
- Parameter: question (string, required)
- Integration with ICAETClient
- Error handling and user-friendly messages
```

### Test file
- Update `tests/unit/test_tools.py` (or create if needed)
- Tests for tool function behavior
- Mock ICAETClient for testing
- Test error scenarios

### Tool Interface
- MCP tool visible in Cursor
- Tool accepts question parameter
- Returns ICAET API results
- Errors are user-friendly

---

## Handoff Criteria

**Ready for Task 06 when**:
1. All acceptance criteria met
2. All tests passing
3. Tool function properly decorated for fastmcp
4. ICAETClient integration working
5. Error handling provides clear user messages
6. Parameter validation prevents bad inputs
7. Linters report zero errors
8. Can call tool function directly in tests

**Artifacts for Next Task**:
- Working MCP tool function ready for server registration
- Tool metadata (name, description, schema)
- Error handling patterns
- Integration example between tool and API client

---

## Task-Specific Constraints

- Tool name must be `query` (per SCRUM-5 spec)
- Single parameter: `question` (string, required)
- Return type should work with fastmcp/MCP protocol
- Error messages shown to users (must be helpful, not technical)
- No logging of user questions in full (privacy)
- Tool must work with fastmcp framework's tool registration
- Keep tool function focused (business logic in ICAETClient)

---

## Integration Notes

**fastmcp Tool Pattern**:
```python
from fastmcp import FastMCP

mcp = FastMCP("icsaet")

@mcp.tool()
def query(question: str) -> str:
    """Query the ICAET knowledge base."""
    # Implementation here
```

Ensure the tool decorator and registration work with fastmcp's expected patterns.

