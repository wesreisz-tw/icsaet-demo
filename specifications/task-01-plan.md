# Task 01 Implementation Plan: Project Setup and Dependencies

**Story**: SCRUM-5  
**Task ID**: Task 01  
**Created**: 2025-11-25

---

## 1. Issue

Need to establish the MCP server project foundation by creating a new `icsaet-mcp` package structure alongside the existing `icsaet-demo` package, configuring all required dependencies (fastmcp, httpx, pydantic-settings), and setting up the src-layout directory structure with placeholder modules.

---

## 2. Solution

Create a parallel package structure using src-layout (`src/icsaet_mcp/`) while maintaining the existing `icsaet_demo/` package. Update `pyproject.toml` to define the new package name, add production and dev dependencies, and configure setuptools to find packages in the src directory. Create six placeholder module files with proper docstrings and minimal valid Python to establish the codebase structure.

**Technical Rationale**:
- Use src-layout to separate source from tests and prevent accidental imports
- Keep existing `icsaet_demo` intact per task constraints
- fastmcp>=0.1.0 provides MCP protocol implementation
- httpx>=0.24.0 enables async HTTP calls to ICAET API
- pydantic-settings>=2.0.0 manages environment-based configuration
- pytest-asyncio>=0.21.0 enables async test support for future tasks

---

## 3. Implementation Steps

### Step 1: Update pyproject.toml Package Metadata
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/pyproject.toml`
- Change line 6: `name = "icsaet-demo"` to `name = "icsaet-mcp"`
- Change line 8: `description = "A minimal Python script project"` to `description = "MCP server for querying ICAET conference data"`
- Add after line 8:
  ```
  keywords = ["mcp", "icaet", "conference", "query"]
  classifiers = [
      "Development Status :: 3 - Alpha",
      "Intended Audience :: Developers",
      "Programming Language :: Python :: 3.13",
  ]
  ```

### Step 2: Add Production Dependencies
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/pyproject.toml`
- Replace line 10: `dependencies = []` with:
  ```
  dependencies = [
      "fastmcp>=0.1.0",
      "httpx>=0.24.0",
      "pydantic-settings>=2.0.0",
  ]
  ```

### Step 3: Update Dev Dependencies
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/pyproject.toml`
- In section `[project.optional-dependencies]` at line 12, add `pytest-asyncio>=0.21.0` to dev list
- Result should be:
  ```
  dev = [
      "pytest>=7.4.3",
      "pytest-asyncio>=0.21.0",
      "black>=23.11.0",
      "ruff>=0.1.6",
      "mypy>=1.7.1",
  ]
  ```

### Step 4: Update Entry Point
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/pyproject.toml`
- Change line 21: `icsaet-demo = "icsaet_demo.main:main"` to `icsaet-mcp = "icsaet_mcp.__main__:main"`

### Step 5: Update Package Finding Configuration
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/pyproject.toml`
- Change line 24: `where = ["."]` to `where = ["src"]`
- Change line 25: `include = ["icsaet_demo*"]` to `include = ["icsaet_mcp*"]`

### Step 6: Create src Directory
**Location**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
- Create directory: `src/`

### Step 7: Create Package Directory
**Location**: `/Users/wesleyreisz/work/mcp/icsaet-demo/src/`
- Create directory: `icsaet_mcp/`

### Step 8: Create __init__.py
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/src/icsaet_mcp/__init__.py`
- Content:
  ```
  """ICSAET MCP Server - Query interface for ICAET conference data."""
  
  __version__ = "0.1.0"
  ```

### Step 9: Create __main__.py
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/src/icsaet_mcp/__main__.py`
- Content:
  ```
  """Entry point for icsaet-mcp server."""
  
  
  def main():
      pass
  
  
  if __name__ == "__main__":
      main()
  ```

### Step 10: Create config.py
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/src/icsaet_mcp/config.py`
- Content:
  ```
  """Configuration management for ICSAET MCP server."""
  ```

### Step 11: Create server.py
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/src/icsaet_mcp/server.py`
- Content:
  ```
  """FastMCP server setup and configuration."""
  ```

### Step 12: Create tools.py
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/src/icsaet_mcp/tools.py`
- Content:
  ```
  """MCP tool definitions for ICAET queries."""
  ```

### Step 13: Create prompts.py
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/src/icsaet_mcp/prompts.py`
- Content:
  ```
  """MCP prompt definitions for ICAET context."""
  ```

### Step 14: Update README.md
**File**: `/Users/wesleyreisz/work/mcp/icsaet-demo/README.md`
- Replace entire content with:
  ```
  # icsaet-mcp
  
  MCP server for querying ICAET conference data.
  
  ## Overview
  
  This Model Context Protocol (MCP) server provides tools for querying the ICAET (International Conference on Software Engineering and Technology) conference data API.
  
  ## Requirements
  
  - Python 3.13 or higher
  
  ## Installation
  
  ```bash
  pip install -e .
  ```
  
  ## Development
  
  Install development dependencies:
  
  ```bash
  pip install -e ".[dev]"
  ```
  
  Run tests:
  
  ```bash
  pytest
  ```
  
  Run linter:
  
  ```bash
  ruff check .
  ```
  
  Format code:
  
  ```bash
  black .
  ```
  
  Type checking:
  
  ```bash
  mypy src/icsaet_mcp
  ```
  
  ## License
  
  MIT
  ```

### Step 15: Verify Installation
**Command**: `pip install -e .`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: Installation completes without errors

### Step 16: Verify Dev Installation
**Command**: `pip install -e ".[dev]"`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: All dev dependencies install successfully

### Step 17: Verify Entry Point
**Command**: `python -m icsaet_mcp`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: Runs without import errors, exits cleanly

### Step 18: Verify Ruff
**Command**: `ruff check .`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: Zero errors reported

### Step 19: Verify Black
**Command**: `black --check .`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: No changes needed

### Step 20: Verify Mypy
**Command**: `mypy src/icsaet_mcp`
**Working Directory**: `/Users/wesleyreisz/work/mcp/icsaet-demo/`
**Expected**: No type checking errors

---

## 4. Verification

### Installation Success
- `pip install -e .` completes without errors
- `pip install -e ".[dev]"` installs pytest-asyncio
- `python -m icsaet_mcp` runs without ImportError

### Package Structure
- Directory `src/icsaet_mcp/` exists
- All six module files exist: `__init__.py`, `__main__.py`, `config.py`, `server.py`, `tools.py`, `prompts.py`
- Each module file contains a docstring
- `__init__.py` exports `__version__ = "0.1.0"`

### Dependencies Available
- Can import: `from fastmcp import FastMCP`
- Can import: `import httpx`
- Can import: `from pydantic_settings import BaseSettings`

### Code Quality
- `ruff check .` reports zero errors
- `black --check .` reports no formatting changes needed
- `mypy src/icsaet_mcp` reports zero type errors

### Configuration
- `pyproject.toml` has `name = "icsaet-mcp"`
- `pyproject.toml` has `requires-python = ">=3.13"`
- Entry point is `icsaet-mcp = "icsaet_mcp.__main__:main"`
- Package finding set to `where = ["src"]` and `include = ["icsaet_mcp*"]`

### Documentation
- README.md describes MCP server purpose
- README.md includes installation and development instructions
- README.md references correct package name `icsaet-mcp`

---

## IMPLEMENTATION CHECKLIST

:white_check_mark: 1. Update pyproject.toml package name to `icsaet-mcp`
:white_check_mark: 2. Add package description, keywords, and classifiers to pyproject.toml
:white_check_mark: 3. Add production dependencies (fastmcp, httpx, pydantic-settings) to pyproject.toml
:white_check_mark: 4. Add pytest-asyncio to dev dependencies in pyproject.toml
:white_check_mark: 5. Update entry point to `icsaet-mcp = "icsaet_mcp.__main__:main"` in pyproject.toml
:white_check_mark: 6. Update package finding to `where = ["src"]` and `include = ["icsaet_mcp*"]` in pyproject.toml
:white_check_mark: 7. Create `src/` directory
:white_check_mark: 8. Create `src/icsaet_mcp/` directory
:white_check_mark: 9. Create `src/icsaet_mcp/__init__.py` with version export
:white_check_mark: 10. Create `src/icsaet_mcp/__main__.py` with main() function
:white_check_mark: 11. Create `src/icsaet_mcp/config.py` with docstring
:white_check_mark: 12. Create `src/icsaet_mcp/server.py` with docstring
:white_check_mark: 13. Create `src/icsaet_mcp/tools.py` with docstring
:white_check_mark: 14. Create `src/icsaet_mcp/prompts.py` with docstring
:white_check_mark: 15. Update README.md with MCP server description and instructions
:white_check_mark: 16. Run `pip install -e .` and verify success
:white_check_mark: 17. Run `pip install -e ".[dev]"` and verify success
:white_check_mark: 18. Run `python -m icsaet_mcp` and verify no import errors
:white_check_mark: 19. Run `ruff check .` and verify zero errors
:white_check_mark: 20. Run `black --check .` and verify no changes needed
:white_check_mark: 21. Run `mypy src/icsaet_mcp` and verify zero errors
:white_check_mark: 22. Verify all three production dependencies are importable
:white_check_mark: 23. Verify directory structure matches task specification
:white_check_mark: 24. Verify existing `icsaet_demo/` package remains intact

