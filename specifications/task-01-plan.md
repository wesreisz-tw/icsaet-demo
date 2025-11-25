# Task 01 Implementation Plan: Project Setup and Dependencies

**Story**: SCRUM-5 - Cursor MCP Server for ICAET Query Access  
**Task**: 01 - Project Setup and Dependencies

---

## 1. Issue

Set up the foundational project structure for the ICAET MCP server by renaming the package, creating the directory structure with placeholder files, and configuring all required dependencies.

---

## 2. Solution

Update `pyproject.toml` to rename package from `icsaet-demo` to `icsaet-mcp`, add production dependencies (`fastmcp`, `httpx`, `pydantic-settings`), update dev dependencies with `pytest-asyncio`, and configure the new entry point. Create the `src/icsaet_mcp/` directory with six placeholder Python files containing minimal valid code and module docstrings.

---

## 3. Implementation Steps

1. Update `pyproject.toml`:
   - Change `name = "icsaet-demo"` to `name = "icsaet-mcp"`
   - Update `description` to `"MCP server for querying the ICAET knowledge base from Cursor IDE"`
   - Verify `requires-python = ">=3.13"` (already set)
   - Add dependencies: `"fastmcp>=0.1.0"`, `"httpx>=0.24.0"`, `"pydantic-settings>=2.0.0"`
   - Add dev dependency: `"pytest-asyncio>=0.21.0"`
   - Change entry point to: `icsaet-mcp = "icsaet_mcp.__main__:main"`
   - Update `[tool.setuptools.packages.find]` to `where = ["src"]` and `include = ["icsaet_mcp*"]`
   - Add keywords: `["mcp", "cursor", "icaet", "knowledge-base"]`
   - Add classifiers for Python 3.13

2. Create `src/icsaet_mcp/__init__.py`:
   - Module docstring explaining package purpose
   - Export `__version__ = "0.1.0"`

3. Create `src/icsaet_mcp/__main__.py`:
   - Module docstring
   - Stub `main()` function with `pass` body
   - `if __name__ == "__main__"` block calling `main()`

4. Create `src/icsaet_mcp/config.py`:
   - Module docstring: "Configuration management using Pydantic Settings"
   - Empty placeholder (ready for Task 02)

5. Create `src/icsaet_mcp/server.py`:
   - Module docstring: "FastMCP server setup and configuration"
   - Empty placeholder (ready for Task 06)

6. Create `src/icsaet_mcp/tools.py`:
   - Module docstring: "MCP tool implementations for ICAET queries"
   - Empty placeholder (ready for Task 03 and Task 05)

7. Create `src/icsaet_mcp/prompts.py`:
   - Module docstring: "MCP prompt definitions for ICAET guidance"
   - Empty placeholder (ready for Task 04)

8. Run `pip install -e ".[dev]"` to verify installation

9. Run `python -m icsaet_mcp` to verify entry point works

10. Run `ruff check src/icsaet_mcp` and `black --check src/icsaet_mcp` to verify code quality

---

## 4. Verification

- [ ] `pip install -e ".[dev]"` succeeds without errors
- [ ] `python -m icsaet_mcp` runs without import errors
- [ ] All six module files exist in `src/icsaet_mcp/`
- [ ] Each file has a module docstring
- [ ] `ruff check .` passes with no errors
- [ ] `black --check .` shows no changes needed
- [ ] Package version accessible: `from icsaet_mcp import __version__`

