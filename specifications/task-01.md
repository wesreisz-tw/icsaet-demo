# Task 01: Project Setup and Dependencies

**Story**: SCRUM-5 - Cursor MCP Server for ICAET Query Access  
**Task Sequence**: 1 of 9  
**Dependencies**: None (foundational task)

---

## Objective

Set up the project foundation by renaming the package, creating the directory structure, and configuring all dependencies required for the MCP server implementation.

---

## Scope

- Rename package from `icsaet-demo` to `icsaet-mcp` in `pyproject.toml`
- Update Python version requirement to 3.13+
- Add production dependencies: `fastmcp>=0.1.0`, `httpx>=0.24.0`, `pydantic-settings>=2.0.0`
- Add dev dependencies: `pytest-asyncio>=0.21.0` (for future test compatibility)
- Create `src/icsaet_mcp/` directory structure
- Create placeholder files: `__init__.py`, `__main__.py`, `server.py`, `tools.py`, `prompts.py`, `config.py`
- Update README.md with basic project description
- Update package metadata (description, keywords, classifiers)

---

## Acceptance Criteria

1. **Package Configuration**
   - [ ] Package renamed to `icsaet-mcp` in `pyproject.toml`
   - [ ] `requires-python = ">=3.13"`
   - [ ] All required dependencies added to `[project.dependencies]`
   - [ ] Dev dependencies updated in `[project.optional-dependencies]`
   - [ ] Package description updated to reflect MCP server purpose
   - [ ] Entry point configured: `icsaet-mcp = "icsaet_mcp.__main__:main"`

2. **Directory Structure**
   - [ ] `src/icsaet_mcp/` directory created
   - [ ] All six module files created with minimal valid Python
   - [ ] Each file has proper module docstring
   - [ ] `__init__.py` exports package version

3. **Installation Verification**
   - [ ] `pip install -e .` succeeds without errors
   - [ ] `pip install -e ".[dev]"` installs all dev dependencies
   - [ ] `python -m icsaet_mcp` runs without import errors (even if it just exits)

4. **Code Quality**
   - [ ] `ruff check .` passes with no errors
   - [ ] `black .` runs without making changes
   - [ ] `mypy src/icsaet_mcp` passes basic type checking

---

## Required Inputs

None - this is the foundational task.

---

## Expected Outputs

### Directory Structure
```
src/icsaet_mcp/
├── __init__.py          # Package version and exports
├── __main__.py          # Entry point (minimal stub)
├── config.py            # Empty (ready for Pydantic Settings)
├── server.py            # Empty (ready for fastmcp setup)
├── tools.py             # Empty (ready for query tool)
└── prompts.py           # Empty (ready for prompt definitions)
```

### Updated pyproject.toml
- Package name: `icsaet-mcp`
- Python requirement: `>=3.13`
- Dependencies: `fastmcp`, `httpx`, `pydantic-settings`
- Entry point configured

### Verification
- Package installs cleanly
- Linters pass
- All imports resolve correctly

---

## Handoff Criteria

**Ready for Task 02 when**:
1. All acceptance criteria are met
2. Package installs without errors
3. Directory structure is in place
4. Dependencies are available for import
5. Linters report zero errors
6. Can run `python -m icsaet_mcp` (even if it does nothing yet)

**Artifacts for Next Task**:
- Working package structure
- All dependencies installed and importable
- Clean linting baseline
- `config.py` file ready for implementation

---

## Task-Specific Constraints

- Maintain compatibility with existing `icsaet_demo` package (don't delete it)
- Use `src/` layout as specified in SCRUM-5
- Keep existing dev tools (black, ruff, mypy) with same configuration
- Don't implement any business logic yet - this is pure setup

