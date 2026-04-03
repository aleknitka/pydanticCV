# Testing Patterns

**Analysis Date:** 2026-04-03

## Test Framework

**Runner:**
- pytest 9.0.2
- Config: `pyproject.toml` `[tool.pytest.ini_options]`

**Assertion Library:**
- pytest built-in assertions
- Pydantic ValidationError for validation testing

**Run Commands:**
```bash
pytest -v                    # Run all tests with verbose output
pytest --cov=pydanticcv      # Run with coverage
tox                          # Run multi-version tests (py311, py312, py313)
```

## Test File Organization

**Location:**
- Co-located in `tests/` directory (separate from source)

**Naming:**
- `test_{domain}.py` pattern
- Examples: `test_ielts.py`, `test_toefl_ibt.py`, `test_date.py`

**Structure:**
```
tests/
├── __init__.py
├── conftest.py              # Fixtures and factories
├── test_ielts.py
├── test_toefl_ibt.py
├── test_toefl_itp.py
├── test_date.py
├── test_cv.py
├── test_employment.py
├── test_reference.py
└── test_volunteering.py
```

## Test Structure

**Suite Organization:**
```python
class TestIELTSBandScoreValidation:
    """Tests for IELTSBandScore type validation."""

    def test_accepts_valid_band_scores(self) -> None:
        # Test implementation
```

**Patterns:**
- Class-based test organization with descriptive class names
- Docstrings for test methods (Google style with Args/Returns)
- Parametrize decorators for multiple inputs

## Mocking

**Framework:** Not heavily used — schema validation is direct

**Patterns:**
- Use Polyfactory/Faker for test data generation
- factories defined in `conftest.py`

## Fixtures and Factories

**Test Data:**
```python
# From conftest.py
class IELTSFactory(Factory):
    class Config:
        model = IELTS

# Usage in tests
ielts = IELTSFactory.create()
```

**Location:**
- `tests/conftest.py` — Shared fixtures and factory definitions

## Coverage

**Requirements:** 60% minimum (fail_under = 60)

**View Coverage:**
```bash
tox -e coverage           # Generate HTML and terminal reports
coverage report --show-missing
```

## Test Types

**Unit Tests:**
- Validation of individual fields and types
- Model validator testing
- Computed property testing (e.g., CEFRLevel)

**Integration Tests:**
- Complete model validation (e.g., full IELTS record)
- Cross-field validation (e.g., Overall vs average of sections)

## Common Patterns

**Async Testing:** N/A (synchronous Pydantic validation)

**Error Testing:**
```python
with pytest.raises(ValidationError, match="error message pattern"):
    Model(field=invalid_value)
```

---

*Testing analysis: 2026-04-03*