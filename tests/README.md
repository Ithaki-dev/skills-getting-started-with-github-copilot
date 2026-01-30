# Testing Guide

## Prerequisites

Make sure you have all dependencies installed:

```bash
pip install -r requirements.txt
```

## Running Tests

### Run all tests
```bash
python -m pytest tests/
```

### Run tests with verbose output
```bash
python -m pytest tests/ -v
```

### Run tests with coverage report
```bash
python -m pytest tests/ --cov=src --cov-report=term-missing
```

### Run specific test file
```bash
python -m pytest tests/test_api.py -v
```

### Run specific test function
```bash
python -m pytest tests/test_api.py::test_signup_for_activity_success -v
```

## Test Structure

- `tests/conftest.py` - Test configuration and fixtures
- `tests/test_api.py` - Basic API endpoint tests
- `tests/test_integration.py` - Integration and workflow tests

## Test Coverage

The test suite covers:

✅ **GET /activities** - Retrieving all activities
✅ **POST /activities/{name}/signup** - Student signup functionality
✅ **DELETE /activities/{name}/unregister** - Student unregistration functionality
✅ **Error handling** - 404s, 400s, and validation errors
✅ **Integration workflows** - Complete signup/unregister cycles
✅ **Edge cases** - URL encoding, multiple students, etc.

## Test Fixtures

- `client` - FastAPI test client
- `reset_activities` - Resets activity data between tests
- `sample_emails` - Provides test email addresses

## Adding New Tests

When adding new tests:

1. Use the provided fixtures for consistency
2. Follow the naming convention: `test_description_of_what_is_tested`
3. Include both positive and negative test cases
4. Test edge cases and error conditions
5. Use the `reset_activities` fixture if your test modifies data