# ICAET MCP Server Tests

This directory contains unit and integration tests for the ICAET MCP server.

## Test Structure

```
tests/
├── unit/               # Unit tests for individual modules
│   ├── test_config.py
│   ├── test_tools.py
│   ├── test_server.py
│   └── test_main.py
└── integration/        # Integration tests for component interactions
    ├── test_query_flow.py
    └── test_real_api.py (optional)
```

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Only Unit Tests
```bash
pytest tests/unit/
```

### Run Only Integration Tests
```bash
pytest -m integration
```

### Run With Coverage
```bash
pytest --cov=icsaet_mcp --cov-report=term-missing
```

### Run Real API Tests (Optional)
```bash
# Set environment variables first
export ICAET_API_KEY="your-api-key"
export USER_EMAIL="your-email@example.com"

# Run real API tests
pytest -m real_api tests/integration/test_real_api.py -v -s
```

## Test Categories

### Unit Tests

Test individual components in isolation with mocked dependencies:

- **test_config.py**: Configuration loading and validation
- **test_tools.py**: ICAETClient HTTP client and query tool
- **test_server.py**: FastMCP server setup and prompt registration
- **test_main.py**: Entry point and server lifecycle

### Integration Tests

Test component interactions and full workflows:

- **test_query_flow.py**: End-to-end query flow with mocked API
- **test_real_api.py**: Optional real API test (requires credentials)

## Writing Tests

All tests follow the AAA (Arrange-Act-Assert) pattern with explicit comments:

```python
def test_example():
    """Arrange: Setup test conditions
    Act: Execute the action being tested
    Assert: Verify the results"""
    # Arrange
    input_data = "test"
    
    # Act
    result = function_under_test(input_data)
    
    # Assert
    assert result == expected_output
```

## Test Configuration

Test configuration is managed through:
- `pytest.ini`: Pytest configuration and markers
- `pyproject.toml`: Test dependencies and coverage settings
- Environment variables: Test credentials and settings

## CI/CD

Tests run in CI with the following characteristics:
- All unit tests run on every commit
- Integration tests run with mocked dependencies
- Real API tests are skipped (require credentials)
- Coverage threshold: Critical paths covered (not 100%)

