# Task 06 Implementation Plan: MCP Server Setup and Integration

**Story**: SCRUM-5 - Cursor MCP Server for ICAET Query Access  
**Task**: 06 - MCP Server Setup and Integration

---

## 1. Issue

Implement the fastmcp server in `server.py` that integrates the query tool and prompts, handling server lifecycle for Cursor IDE integration.

---

## 2. Solution

Import the `mcp` instance from `tools.py` (which already has the query tool registered) and register the prompts from `prompts.py`. Configure server metadata and export the server instance for use by `__main__.py`. The server communicates via stdio as required by MCP protocol.

---

## 3. Implementation Steps

1. Implement `src/icsaet_mcp/server.py`:
   - Import `logging`
   - Import `mcp` from `icsaet_mcp.tools` (already has FastMCP instance with query tool)
   - Import `PROMPTS` from `icsaet_mcp.prompts`
   - Import `__version__` from `icsaet_mcp`
   - Create logger: `logger = logging.getLogger(__name__)`

2. Register prompts with server:
   - Iterate over `PROMPTS` list
   - Use fastmcp's prompt registration method (likely `@mcp.prompt()` decorator or `mcp.add_prompt()`)
   - Each prompt registered with name, description, and content

3. Create prompt registration functions if needed:
   ```python
   @mcp.prompt(name="icaet_overview", description="Learn what ICAET is")
   def icaet_overview() -> str:
       return PROMPTS[0]["content"]
   ```
   - Repeat for all three prompts

4. Add server initialization logging:
   - Log INFO on module load: "ICAET MCP Server v{version} initialized"
   - Log INFO: "Registered 1 tool, 3 prompts"

5. Export `mcp` for use by `__main__.py`:
   - The `mcp` instance (imported from tools) is already the configured server
   - Module just needs to make it available: no additional export needed if importing from tools

6. Create `tests/unit/test_server.py`:
   - Test: `test_server_instance_exists` - import mcp from server, verify not None
   - Test: `test_server_name` - verify mcp.name == "icsaet"
   - Test: `test_query_tool_registered` - verify "query" tool in server's tools
   - Test: `test_prompts_registered` - verify all 3 prompts registered
   - Mock fastmcp internals as needed to inspect registrations

7. Run `pytest tests/unit/test_server.py -v`

8. Run `ruff check src/icsaet_mcp/server.py` and `mypy src/icsaet_mcp/server.py`

---

## 4. Verification

- [ ] `mcp` instance imported from tools.py (FastMCP("icsaet"))
- [ ] All three prompts registered with server
- [ ] Server name is "icsaet"
- [ ] Query tool accessible via server
- [ ] Server can be imported: `from icsaet_mcp.server import mcp`
- [ ] Initialization logging works
- [ ] All unit tests pass
- [ ] `ruff check` and `mypy` pass
