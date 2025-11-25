# Task 02 Implementation Plan: Configuration Management with Pydantic Settings

**Story**: SCRUM-5  
**Task**: Task 02 of 9  
**Dependencies**: Task 01 completed

---

## 1. Issue

Implement type-safe configuration management to validate and provide environment variables (`ICAET_API_KEY` and `USER_EMAIL`) required for ICAET API authentication using Pydantic Settings with proper validation and singleton pattern.

---

## 2. Solution

Use Pydantic v2 `BaseSettings` to create a `Settings` class that automatically loads and validates environment variables. Implement singleton pattern using `@lru_cache` to ensure single instance across application. Add field validators for non-empty strings and basic email format validation. Follow the configuration pattern from `.cursor/rules/python.mdc` lines 487-514.

---

## 3. Implementation Steps

### Step 1: Implement Settings class in `src/icsaet_mcp/config.py`
- Import required dependencies: `Field`, `field_validator` from `pydantic`, `BaseSettings`, `SettingsConfigDict` from `pydantic_settings`
- Create `Settings` class inheriting from `BaseSettings`
- Add `model_config = SettingsConfigDict(case_sensitive=False, extra="ignore")`
- Define `icaet_api_key: str` field with `Field(..., min_length=10, description="ICAET API key for authentication")`
- Define `user_email: str` field with `Field(..., min_length=5, description="User email for API requests")`
- Add `@field_validator("icaet_api_key")` classmethod to check non-empty after stripping
- Add `@field_validator("user_email")` classmethod to validate email contains "@" and "."
- Add docstring to Settings class explaining purpose and environment variable requirements

### Step 2: Implement singleton accessor in `src/icsaet_mcp/config.py`
- Import `lru_cache` from `functools`
- Create `get_settings()` function with `@lru_cache` decorator (no maxsize for single instance)
- Function returns `Settings` instance
- Add return type hint: `-> Settings`
- Add docstring explaining singleton pattern and caching behavior

### Step 3: Create test file `tests/unit/test_config.py`
- Import `pytest`, `Settings`, `get_settings` from `icsaet_mcp.config`
- Import `ValidationError` from `pydantic`
- Create fixture `@pytest.fixture` named `valid_env_vars` that uses `monkeypatch` to set ICAET_API_KEY and USER_EMAIL
- Create fixture `@pytest.fixture` named `clear_settings_cache` that clears `get_settings.cache_clear()` after each test

### Step 4: Implement success case tests in `tests/unit/test_config.py`
- Write `test_settings_loads_with_valid_env_vars(valid_env_vars)`: Create Settings instance, assert both fields populated correctly
- Write `test_get_settings_returns_same_instance(valid_env_vars)`: Call `get_settings()` twice, assert both returns are same object using `is`
- Write `test_settings_accepts_valid_email_format(monkeypatch)`: Set valid email with @, create Settings, assert no exception

### Step 5: Implement validation failure tests in `tests/unit/test_config.py`
- Write `test_missing_api_key_raises_validation_error(monkeypatch)`: Set only USER_EMAIL, expect ValidationError when creating Settings
- Write `test_missing_user_email_raises_validation_error(monkeypatch)`: Set only ICAET_API_KEY, expect ValidationError when creating Settings
- Write `test_empty_api_key_rejected(monkeypatch)`: Set ICAET_API_KEY="", expect ValidationError
- Write `test_empty_user_email_rejected(monkeypatch)`: Set USER_EMAIL="", expect ValidationError
- Write `test_invalid_email_format_rejected(monkeypatch)`: Set USER_EMAIL without "@", expect ValidationError with match pattern

### Step 6: Add type hints and docstrings
- Verify all functions have proper type hints (parameters and return values)
- Verify Settings class has docstring with Args section documenting environment variables
- Verify `get_settings()` has docstring explaining singleton pattern
- Verify all validators have docstrings explaining validation rules

### Step 7: Run tests and linters
- Execute `pytest tests/unit/test_config.py -v` to verify all tests pass
- Execute `ruff check src/icsaet_mcp/config.py tests/unit/test_config.py`
- Execute `black --check src/icsaet_mcp/config.py tests/unit/test_config.py`
- Execute `mypy src/icsaet_mcp/config.py` to verify type checking passes
- Fix any issues reported by linters

---

## 4. Verification

**Configuration Works**:
- Can instantiate Settings with valid ICAET_API_KEY and USER_EMAIL
- ValidationError raised with clear message for missing ICAET_API_KEY
- ValidationError raised with clear message for missing USER_EMAIL
- Empty strings rejected with validation error
- Invalid email format (missing @) rejected with validation error

**Singleton Pattern Works**:
- `get_settings()` returns same instance on multiple calls
- Can verify with `id()` or `is` comparison

**Tests Pass**:
- All 8+ unit tests pass successfully
- Test coverage on config.py is 100%
- No linter errors (ruff, black, mypy)

**Code Quality**:
- All functions and classes have type hints
- Docstrings present on Settings class and get_settings()
- Follows project Python style guide
- No hardcoded secrets or example values in code

