# Task 08: Testing and Verification

**Story**: SCRUM-5 - Cursor MCP Server for ICAET Query Access  
**Task Sequence**: 8 of 9  
**Dependencies**: Task 07 (entry point complete)

---

## Objective

Create comprehensive test coverage for the MCP server, verify all components work together, add integration tests, and ensure the Definition of Done criteria are met.

---

## Scope

- Review and complete unit test coverage for all modules
- Add integration tests for end-to-end flows
- Create optional manual test against real ICAET API
- Verify all acceptance criteria from SCRUM-5
- Test error scenarios and edge cases
- Validate logging and configuration
- Create test documentation

---

## Acceptance Criteria

1. **Unit Test Coverage**
   - [ ] `test_config.py`: Settings validation tests (from Task 02)
   - [ ] `test_icaet_client.py`: API client tests (from Task 03)
   - [ ] `test_tools.py`: Query tool tests (from Task 05)
   - [ ] `test_server.py`: Server setup tests (from Task 06)
   - [ ] `test_main.py`: Entry point tests (from Task 07)
   - [ ] All tests passing
   - [ ] Reasonable coverage (focus on critical paths)

2. **Integration Tests**
   - [ ] Test: Full query flow (config → tool → API client → response)
   - [ ] Test: Server startup with valid configuration
   - [ ] Test: Server startup with missing configuration
   - [ ] Test: Tool execution through server
   - [ ] Test: Error propagation through layers
   - [ ] File: `tests/integration/test_query_flow.py`

3. **Edge Case Testing**
   - [ ] Empty question handling
   - [ ] Very long questions (stress test)
   - [ ] Special characters in questions
   - [ ] Network timeout simulation
   - [ ] API error responses (401, 500, etc.)
   - [ ] Missing environment variables
   - [ ] Invalid email format

4. **Mocking Patterns**
   - [ ] httpx responses mocked consistently
   - [ ] Settings mocked for testing without env vars
   - [ ] FastMCP server mocked where appropriate
   - [ ] No external API calls in unit tests
   - [ ] Consistent mock patterns across test files

5. **Optional Integration Test**
   - [ ] `tests/integration/test_real_api.py` (marked as optional)
   - [ ] Skipped by default (requires env vars)
   - [ ] Can be run manually with: `pytest -m integration`
   - [ ] Tests real ICAET API call
   - [ ] Documents expected response format

6. **Test Documentation**
   - [ ] `tests/README.md` explaining test structure
   - [ ] How to run tests
   - [ ] How to run with coverage
   - [ ] How to run integration tests
   - [ ] How to mock API responses

7. **Verification Against SCRUM-5**
   - [ ] Functional DoD: All items verified
     - MCP server connects to Cursor ✓
     - Queries return ICAET results ✓
     - Missing credentials show clear errors ✓
     - Multi-turn conversations work ✓
     - Prompts display correctly ✓
   - [ ] Security DoD: All items verified
     - No credentials in code ✓
     - HTTPS communication ✓
     - No sensitive data logged ✓
     - Environment variables isolated ✓
   - [ ] Operational DoD: Verified in tests
     - Simple installation process ✓
     - MCP server starts/stops cleanly ✓
     - End-to-end test passes ✓

8. **Test Execution**
   - [ ] `pytest` runs all unit tests successfully
   - [ ] `pytest --cov=src/icsaet_mcp` shows reasonable coverage
   - [ ] `pytest tests/integration/` runs integration tests
   - [ ] All tests complete in reasonable time (<30 seconds)
   - [ ] No flaky tests

9. **Code Quality**
   - [ ] All test files pass ruff, black checks
   - [ ] Tests follow AAA pattern (Arrange, Act, Assert)
   - [ ] Test names are descriptive
   - [ ] No commented-out tests
   - [ ] Clean fixtures and setup

---

## Required Inputs

**From Previous Tasks**:
- All implemented modules (config, tools, server, main)
- Existing unit tests from individual tasks
- Working MCP server

**Test Patterns**:
- Mock patterns from earlier tasks
- Error handling examples
- Configuration validation patterns

---

## Expected Outputs

### Comprehensive Test Suite
```
tests/
├── README.md                          # Test documentation
├── conftest.py                        # Shared fixtures
├── unit/
│   ├── test_config.py                 # Settings tests
│   ├── test_icaet_client.py          # API client tests
│   ├── test_tools.py                  # Query tool tests
│   ├── test_server.py                 # Server tests
│   └── test_main.py                   # Entry point tests
└── integration/
    ├── test_query_flow.py             # End-to-end tests
    └── test_real_api.py               # Optional real API test
```

### Test Documentation
- How to run tests
- How to add new tests
- Mock patterns and examples
- Integration test setup

### Coverage Report
- Reasonable coverage on critical paths
- Config, tools, client well tested
- Server and main tested

---

## Handoff Criteria

**Ready for Task 09 when**:
1. All acceptance criteria met
2. All unit tests passing
3. Integration tests implemented and passing
4. Test documentation complete
5. Coverage is reasonable (not necessarily 100%)
6. All SCRUM-5 Definition of Done items verified
7. No flaky or skipped tests (except optional real API test)
8. Linters pass on all test files
9. Can run tests in CI/CD environment

**Artifacts for Next Task**:
- Complete test suite
- Test documentation
- Coverage report
- Verification of all acceptance criteria
- Confidence in code quality and correctness

---

## Task-Specific Constraints

- Focus on critical paths (not 100% coverage goal)
- Unit tests must be fast (<1 second each)
- No external dependencies in unit tests
- Integration tests can be slower
- Real API test is optional (skip by default)
- Use pytest markers: `@pytest.mark.integration`
- Follow project's test patterns (AAA pattern)
- Mock all external services (httpx, API calls)
- Tests must be deterministic (no random failures)

---

## Test Examples

**Unit Test Pattern**:
```python
def test_query_with_valid_question(mock_settings, mock_httpx):
    # Arrange
    client = ICAETClient(mock_settings)
    mock_httpx.post.return_value.json.return_value = {"answer": "..."}
    
    # Act
    result = client.query("What did Leslie talk about?")
    
    # Assert
    assert "answer" in result
    mock_httpx.post.assert_called_once()
```

**Integration Test Pattern**:
```python
def test_full_query_flow(monkeypatch):
    # Arrange: Set env vars
    monkeypatch.setenv("ICAET_API_KEY", "test-key")
    monkeypatch.setenv("USER_EMAIL", "test@example.com")
    
    # Act: Call through full stack
    with patch("httpx.Client") as mock_client:
        mock_client.return_value.__enter__.return_value.post.return_value.json.return_value = {"answer": "test"}
        result = query_icaet("test question")
    
    # Assert: Response returned
    assert result is not None
```

---

## Success Metrics

- All tests pass consistently
- Code behaves as specified in SCRUM-5
- Error messages are helpful
- Configuration validation works
- API integration works (mocked and optionally real)
- Ready for documentation and release

