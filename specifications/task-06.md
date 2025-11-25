# Task 06: MCP Server Setup and Integration

**Story**: SCRUM-5 - Cursor MCP Server for ICAET Query Access  
**Task Sequence**: 6 of 9  
**Dependencies**: Task 04 (prompts complete), Task 05 (query tool complete)

---

## Objective

Implement the fastmcp server in `server.py` that registers the query tool, prompts, and handles server lifecycle for integration with Cursor IDE.

---

## Scope

- Create FastMCP server instance in `server.py`
- Register the query tool from `tools.py`
- Register the three prompts from `prompts.py`
- Configure server metadata (name, version)
- Implement server lifecycle (startup, shutdown)
- Add logging for server events
- Export server instance for use by `__main__.py`

---

## Acceptance Criteria

1. **Server Instance Creation**
   - [ ] FastMCP instance created with name "icsaet"
   - [ ] Server version matches package version
   - [ ] Proper type hints for server instance

2. **Tool Registration**
   - [ ] Query tool imported from `tools.py`
   - [ ] Tool registered with server using fastmcp patterns
   - [ ] Tool appears in server's tool list
   - [ ] Tool is callable through MCP protocol

3. **Prompt Registration**
   - [ ] All three prompts imported from `prompts.py`
   - [ ] Prompts registered with server
   - [ ] Each prompt has unique name
   - [ ] Prompts accessible through MCP protocol
   - [ ] Prompt metadata (name, description) properly set

4. **Server Configuration**
   - [ ] Server name: "icsaet"
   - [ ] Server description: "ICAET knowledge base query interface"
   - [ ] Version info available
   - [ ] Proper logging configuration

5. **Lifecycle Management**
   - [ ] Server starts cleanly
   - [ ] Server stops gracefully on shutdown
   - [ ] Resources cleaned up on exit
   - [ ] Startup logged at INFO level
   - [ ] Shutdown logged at INFO level

6. **Logging**
   - [ ] Logger configured: `logging.getLogger(__name__)`
   - [ ] INFO log on server startup
   - [ ] INFO log when tools/prompts registered
   - [ ] INFO log on shutdown
   - [ ] No sensitive data in logs

7. **Error Handling**
   - [ ] Handles configuration errors at startup
   - [ ] Clear error messages for setup failures
   - [ ] Validates required components available
   - [ ] Fails fast with helpful messages

8. **Testing**
   - [ ] Unit test: Server instance creates successfully
   - [ ] Unit test: Tools registered correctly
   - [ ] Unit test: Prompts registered correctly
   - [ ] Unit test: Server metadata is correct
   - [ ] Integration test: Server can handle tool calls (optional)

9. **Code Quality**
   - [ ] Full type hints
   - [ ] Module docstring explaining server purpose
   - [ ] Follows Python style guide
   - [ ] Passes ruff, black, mypy checks
   - [ ] Clean module structure

---

## Required Inputs

**From Task 05**:
- Working query tool function decorated for fastmcp
- Tool metadata and schema

**From Task 04**:
- Three prompt definitions ready for registration
- Prompt content and metadata

**From Task 01**:
- Package version from `__init__.py`
- Project structure

---

## Expected Outputs

### Implemented server.py
```python
# Key components (not full implementation):
- FastMCP server instance
- Tool registration
- Prompt registration  
- Server configuration
- Exported server object
```

### Server Interface
- Server instance exported for use by `__main__.py`
- All tools and prompts registered
- Server ready to run via MCP protocol

### Test file
- `tests/unit/test_server.py` with server setup tests
- Verification of tool and prompt registration
- Server lifecycle tests

---

## Handoff Criteria

**Ready for Task 07 when**:
1. All acceptance criteria met
2. All tests passing
3. Server instance properly configured
4. Query tool registered and accessible
5. All three prompts registered and accessible
6. Server starts and stops cleanly
7. Logging works correctly
8. Linters report zero errors
9. Can import server instance: `from icsaet_mcp.server import mcp`

**Artifacts for Next Task**:
- Configured FastMCP server instance
- Pattern for running server via `__main__.py`
- Server lifecycle handling
- Complete integration of tools and prompts

---

## Task-Specific Constraints

- Server name must be "icsaet" (for Cursor configuration)
- Use fastmcp framework's standard patterns
- Server communicates via stdio (MCP protocol requirement)
- No HTTP server (MCP uses stdio)
- Server must be importable for testing
- Follow fastmcp documentation for tool/prompt registration
- Keep server.py focused on configuration (business logic elsewhere)

---

## Integration Pattern

Expected usage in `__main__.py`:
```python
from icsaet_mcp.server import mcp

if __name__ == "__main__":
    mcp.run()
```

Ensure server is structured to support this pattern.

---

## Notes

**fastmcp Server Pattern**:
- Create FastMCP instance
- Use decorators or registration methods for tools/prompts
- Server handles MCP protocol communication
- Server manages stdio for Cursor integration
- Refer to fastmcp documentation for exact API

