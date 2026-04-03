# Coding Conventions

**Analysis Date:** 2026-04-03

## Naming Patterns

**Files:**
- snake_case.py: All Python modules
- Example: `ielts.py`, `toefl_ibt.py`, `personal_info.py`

**Functions:**
- snake_case: Private helpers
- Example: `_parse_and_validate_date` in `utils/date.py`

**Variables:**
- snake_case: Local variables and parameters

**Types:**
- PascalCase: All model classes
- Example: `IELTS`, `CV`, `LanguageProficiencyCertificate`

## Code Style

**Formatting:**
- Ruff (via pre-commit hooks)
- Config: `pyproject.toml` + `prek.toml`

**Linting:**
- Ruff with `--fix` and `ruff-format`
- Type checking: ty

## Import Organization

**Order:**
1. Standard library
2. Third-party packages
3. Local imports (pydanticcv.*)

**Example (from `eng/ielts.py`):**
```python
from typing import Annotated, Literal
from pydantic import BaseModel, StringConstraints, computed_field, model_validator
from pydantic.functional_validators import AfterValidator
from pydanticcv.utils.date import PastDate
from pydanticcv.languages.certificates.eng.base import EnglishLanguageProficiencyCertificate
```

## Error Handling

**Patterns:**
- Validation via Pydantic validators (BeforeValidator, AfterValidator)
- Model validation via @model_validator
- Custom error messages with ValueError

## Comments

**When to Comment:**
- Document every public class with Google-style docstrings
- Include Args:, Returns:, Raises:, Attributes: sections

**Type Hints:**
- Use type annotations throughout
- Use Annotated for constrained types

## Function Design

**Size:** Single-responsibility functions

**Parameters:** Typed parameters with clear names

**Return Values:** Explicit return type annotations

## Module Design

**Exports:** Use `__all__` to list public names

**Barrel Files:** Re-export from `__init__.py` (e.g., `certificates/__init__.py`)

---

*Convention analysis: 2026-04-03*