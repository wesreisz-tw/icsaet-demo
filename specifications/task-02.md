# Task 02: Configuration Management with Pydantic Settings

**Story**: SCRUM-5 - Cursor MCP Server for ICAET Query Access  
**Task Sequence**: 2 of 9  
**Dependencies**: Task 01 (project setup complete)

---

## Objective

Implement type-safe configuration management using Pydantic Settings to validate and provide environment variables (`ICAET_API_KEY` and `USER_EMAIL`) required for ICAET API authentication.

---

## Scope

- Implement `Settings` class in `config.py` using `pydantic-settings.BaseSettings`
- Define required fields: `icaet_api_key` and `user_email`
- Add validation for non-empty strings
- Implement singleton pattern with `@lru_cache` for settings access
- Add clear error messages for missing environment variables
- Create unit tests for configuration validation

---

## Acceptance Criteria

1. **Settings Class Implementation**
   - [ ] `Settings` class inherits from `BaseSettings`
   - [ ] `icaet_api_key: str` field with validation (non-empty)
   - [ ] `user_email: str` field with validation (non-empty, basic email format)
   - [ ] Model configuration includes case-insensitive env var matching
   - [ ] Custom error messages for missing/invalid values

2. **Settings Access Pattern**
   - [ ] `get_settings()` function with `@lru_cache` decorator
   - [ ] Singleton pattern ensures single Settings instance
   - [ ] Function returns `Settings` type (proper type hints)

3. **Validation Rules**
   - [ ] Both fields are required (no defaults)
   - [ ] Empty strings are rejected with clear error message
   - [ ] Email has basic format validation (contains @)
   - [ ] API key length validation (minimum reasonable length)

4. **Error Handling**
   - [ ] Missing `ICAET_API_KEY` raises ValidationError with helpful message
   - [ ] Missing `USER_EMAIL` raises ValidationError with helpful message
   - [ ] Error messages guide user to set environment variables

5. **Testing**
   - [ ] Unit test: Settings loads successfully with valid env vars
   - [ ] Unit test: Missing API key raises ValidationError
   - [ ] Unit test: Missing email raises ValidationError
   - [ ] Unit test: Empty string values are rejected
   - [ ] Unit test: Invalid email format is rejected
   - [ ] Unit test: `get_settings()` returns same instance (singleton)

6. **Code Quality**
   - [ ] Full type hints on all functions and class attributes
   - [ ] No hardcoded secrets or example values
   - [ ] Follows project's Python style guide
   - [ ] Passes ruff, black, mypy checks

---

## Required Inputs

**From Task 01**:
- Working `src/icsaet_mcp/config.py` file (empty stub)
- `pydantic-settings` dependency installed
- Test directory structure ready
- Linting tools configured

---

## Expected Outputs

### Implemented config.py
```python
# Key components (not full implementation):
- Settings class with icaet_api_key and user_email fields
- Field validators for both fields
- get_settings() function with @lru_cache
- Type hints for all public APIs
```

### Test file
- `tests/unit/test_config.py` with comprehensive coverage
- Tests for success and failure cases
- Tests for validation rules
- Singleton pattern verification

### Documentation
- Docstrings on Settings class and get_settings()
- Clear examples in docstrings

---

## Handoff Criteria

**Ready for Task 03 when**:
1. All acceptance criteria met
2. All tests passing (100% coverage on config.py)
3. Can successfully instantiate Settings with valid env vars
4. ValidationError raised with clear messages for missing/invalid config
5. Linters report zero errors
6. `get_settings()` function is ready to use in other modules

**Artifacts for Next Task**:
- Working `config.py` module with `get_settings()` function
- Validated environment variable access pattern
- Test examples showing how to mock configuration
- Clear error messages for debugging

---

## Task-Specific Constraints

- No sensitive data in code (no example API keys)
- Follow project's configuration pattern from `.cursor/rules/python.mdc`
- Use modern Pydantic v2+ features
- Environment variable names must match SCRUM-5 spec: `ICAET_API_KEY`, `USER_EMAIL`
- Keep configuration simple - only the two required fields
- No .env file loading in production (Cursor provides env vars)

