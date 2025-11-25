# Task 02 Implementation Plan: Configuration Management with Pydantic Settings

**Story**: SCRUM-5 - Cursor MCP Server for ICAET Query Access  
**Task**: 02 - Configuration Management with Pydantic Settings

---

## 1. Issue

Implement type-safe configuration management that validates `ICAET_API_KEY` and `USER_EMAIL` environment variables, with clear error messages for missing or invalid values.

---

## 2. Solution

Create a `Settings` class in `config.py` using Pydantic BaseSettings with field validators for non-empty strings and basic email format. Implement a singleton pattern using `@lru_cache` on `get_settings()` function. Write comprehensive unit tests covering success and failure scenarios.

---

## 3. Implementation Steps

1. Implement `src/icsaet_mcp/config.py`:
   - Import `functools.lru_cache`, `pydantic.field_validator`, `pydantic_settings.BaseSettings`, `pydantic_settings.SettingsConfigDict`
   - Create `Settings` class inheriting from `BaseSettings`:
     - `model_config = SettingsConfigDict(case_sensitive=False)`
     - `icaet_api_key: str` field (required, no default)
     - `user_email: str` field (required, no default)
   - Add `@field_validator("icaet_api_key")` to reject empty/whitespace strings
   - Add `@field_validator("user_email")` to reject empty strings and validate contains "@"
   - Create `get_settings() -> Settings` function with `@lru_cache` decorator
   - Add clear docstrings on class and function

2. Create `tests/unit/test_config.py`:
   - Import `pytest`, `unittest.mock.patch`, `pydantic.ValidationError`
   - Test: `test_settings_loads_with_valid_env_vars` - monkeypatch both env vars, verify Settings loads
   - Test: `test_missing_api_key_raises_error` - only set USER_EMAIL, expect ValidationError
   - Test: `test_missing_email_raises_error` - only set ICAET_API_KEY, expect ValidationError
   - Test: `test_empty_api_key_rejected` - set empty string, expect ValidationError
   - Test: `test_empty_email_rejected` - set empty string, expect ValidationError
   - Test: `test_invalid_email_format_rejected` - set email without "@", expect ValidationError
   - Test: `test_get_settings_returns_same_instance` - call twice, verify same object via `is`
   - Use `monkeypatch` to set environment variables in tests
   - Clear `get_settings` cache between tests with `get_settings.cache_clear()`

3. Run `pytest tests/unit/test_config.py -v` to verify tests pass

4. Run `ruff check src/icsaet_mcp/config.py` and `mypy src/icsaet_mcp/config.py`

---

## 4. Verification

- [ ] `Settings` class validates both required fields
- [ ] Empty strings rejected with clear error messages
- [ ] Invalid email format (no "@") rejected
- [ ] `get_settings()` returns cached singleton instance
- [ ] All unit tests pass
- [ ] `ruff check` and `mypy` pass
- [ ] No hardcoded secrets or example values in code

