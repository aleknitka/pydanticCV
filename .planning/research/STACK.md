# Technology Stack: Pydantic v2 Schema Library Patterns

**Project:** pydanticCV
**Researched:** 2026-04-03
**Confidence:** HIGH

## Executive Summary

This document codifies the standard patterns and best practices for building Pydantic v2 schema libraries. The existing pydanticCV codebase already follows these patterns correctly. This research validates the current approach and provides guidance for adding new features (language certificates, certifications, social links).

## Recommended Patterns

### 1. Base Model Inheritance

**Pattern:** Use abstract base models for shared fields across related models.

```python
class LanguageProficiencyCertificate(BaseModel):
    """Base for all language exam records."""
    DateTaken: PastDate
    Link: AnyUrl
    LanguageCertified: ISO639_3
```

**Why:** Single source of truth for common fields (`DateTaken`, `Link`). Changes to shared validation only need to happen in one place.

**When to use:** When multiple models share identical fields (e.g., all language certificates have date + link).

**Confidence:** HIGH — Documented in Pydantic v2 official docs.

---

### 2. Annotated Type Aliases

**Pattern:** Define constrained types using `Annotated` with validators.

```python
IELTSBandScore = Annotated[float, AfterValidator(_validate_band_score)]
```

**Why:** Composable, reusable type constraints. Can be applied to multiple fields.

**When to use:** For any field with specific validation rules (score ranges, string patterns, date formats).

**Confidence:** HIGH — Core Pydantic v2 pattern from official docs.

---

### 3. Field Validators via Annotated

**Pattern:** Use `BeforeValidator`/`AfterValidator` in `Annotated` for type transformation.

```python
from pydantic import BaseModel
from pydantic.functional_validators import BeforeValidator

def parse_date(v):
    # Parse string to date object
    return date.fromisoformat(v)

DateType = Annotated[date, BeforeValidator(parse_date)]
```

**Why:** Clean separation of parsing logic from model definition. Reusable across fields.

**When to use:** For custom parsing that should happen before type validation (e.g., string → date).

**Example in codebase:** `PastDate` in `utils/date.py` uses `BeforeValidator`.

**Confidence:** HIGH — Official Pydantic v2 pattern.

---

### 4. Model Validators (mode="after")

**Pattern:** Use `@model_validator(mode="after")` for cross-field validation.

```python
@model_validator(mode="after")
def check_overall_is_consistent(self) -> "IELTSScores":
    expected = round((self.Listening + self.Reading + self.Writing + self.Speaking) / 4 * 2) / 2
    if self.Overall != expected:
        raise ValueError("Overall does not match component average")
    return self
```

**Why:** Validates relationships between fields. Runs after all field validation completes.

**When to use:** When validation depends on multiple fields (e.g., "overall must equal average of components").

**Example in codebase:** `IELTSScores.check_overall_is_consistent` — correctly implemented.

**Confidence:** HIGH — Official Pydantic v2 pattern.

---

### 5. Computed Fields with @computed_field

**Pattern:** Use `@computed_field` + `@property` for derived values.

```python
@computed_field
@property
def CEFRLevel(self) -> Literal["A1", "A2", "B1", "B2", "C1", "C2"]:
    """Derive CEFR level from score."""
    # logic here
```

**Why:** Includes computed values in serialization (`model_dump`). Clear derivation logic.

**When to use:** For values computed from other fields (e.g., CEFR from exam score).

**Caveats:**
- Include `# type: ignore[misc]` to suppress mypy warnings about decorated properties
- Pyright handles this correctly without the ignore

**Example in codebase:** `IELTS.CEFRLevel` — correctly implemented.

**Confidence:** HIGH — Official Pydantic v2 pattern.

---

### 6. Module-Level Type Aliases for Forward References

**Pattern:** For conversion methods that reference the model class, use module-level type aliases.

```python
from __future__ import annotations  # Must be first after docstring

class TOEFLiBTLegacy(BaseModel):
    # fields...
    
    def to_new(self) -> "TOEFLiBT":
        # conversion logic
```

**Why:** Enables forward references without circular import issues.

**When to use:** When methods return or reference the model class itself.

**Example in codebase:** `TOEFLiBTLegacy.to_new()` method.

**Confidence:** HIGH — Standard Python typing pattern.

---

### 7. Domain-Driven Module Structure

**Pattern:** Organize by domain (certificates/, employment/, skills/) with `__init__.py` re-exporting public API.

```
languages/
├── __init__.py           # Re-exports public API
├── certificates/
│   ├── __init__.py       # Re-exports all certificate types
│   ├── base.py           # Base models and shared types
│   └── eng/
│       ├── __init__.py
│       ├── ielts.py
│       └── toefl_ibt.py
```

**Why:** Clear separation of concerns. Users import from package root (`from pydanticcv.languages.certificates import IELTS`).

**When to use:** For any library with multiple related models.

**Example in codebase:** Already correctly implemented.

**Confidence:** HIGH — Standard Python package pattern.

---

### 8. Testing with Polyfactory

**Pattern:** Use Polyfactory for generating test instances of Pydantic models.

```python
from polyfactory.factories.pydantic_factory import PydanticFactory

class IELTSFactory(PydanticFactory):
    __model__ = IELTS

# Usage
ielts = IELTSFactory.build()
```

**Why:** Type-safe test data generation. Handles nested models automatically. Reduces boilerplate.

**When to use:** For any test that needs valid model instances.

**Dependencies needed:**
- `polyfactory` (already in stack)
- `faker` (already in stack)

**Confidence:** HIGH — Official Polyfactory documentation confirms Pydantic v2 support.

---

### 9. Literal Types for Fixed Choices

**Pattern:** Use `Literal` for fixed string choices.

```python
IELTSType = Literal["Academic", "General Training"]
ExamLevel = Literal["Level 1", "Level 2"]
```

**Why:** Type-safe enumerations. Generates clean JSON schema. IDE autocomplete support.

**When to use:** For fields with a fixed set of allowed string values.

**Example in codebase:** `IELTSType`, `TOEFLITP.ExamLevel` — correctly implemented.

**Confidence:** HIGH — Standard Python typing pattern.

---

### 10. Field Ordering Matters

**Pattern:** Define fields in validation order (dependencies first).

```python
class Model(BaseModel):
    # Must be defined before fields that depend on it
    password1: str
    # Depends on password1 - defined after
    password2: str
```

**Why:** Pydantic v2 validates fields in definition order. Later validators can access earlier field values via `info.data`.

**When to use:** Always — important for cross-field validation.

**Confidence:** HIGH — Documented in Pydantic v2 migration guide.

---

## Common Dependencies

### Core Dependencies

| Package | Purpose | Version |
|---------|---------|---------|
| pydantic | Core validation framework | ^2.12 |
| pydantic-extra-types | Extended types (phonenumbers, language codes) | ^2.11 |
| pycountry | ISO country data | ^24.6 |

### Testing Dependencies

| Package | Purpose | Version |
|---------|---------|---------|
| pytest | Test runner | ^9.0 |
| pytest-cov | Coverage reporting | ^7.1 |
| polyfactory | Test data generation | ^3.3 |
| faker | Fake data provider | ^40.0 |

### Development Dependencies

| Package | Purpose | Version |
|---------|---------|---------|
| ruff | Linting and formatting | ^0.15 |
| mypy | Static type checking | (via ty) |
| pdoc | Documentation generation | ^16.0 |
| prek | Pre-commit hook management | ^0.3 |

---

## Patterns to Avoid

### 1. Using Pydantic v1 Validators

**Avoid:**
```python
# Pydantic v1 style
from pydantic import validator

class Model(BaseModel):
    value: int
    
    @validator('value')
    def check_value(cls, v):
        return v
```

**Instead:**
```python
# Pydantic v2 style
from pydantic import field_validator

class Model(BaseModel):
    value: int
    
    @field_validator('value')
    @classmethod
    def check_value(cls, v):
        return v
```

**Why:** v1 validators are deprecated. v2 uses `@field_validator` with class method pattern.

**Confidence:** HIGH — Migration guide explicitly documents this.

---

### 2. Using default=... with Optional

**Avoid:**
```python
class Model(BaseModel):
    value: Optional[str] = ...  # Wrong - still required
```

**Instead:**
```python
class Model(BaseModel):
    value: Optional[str] = None  # Correct - has default
```

**Why:** In Pydantic v2, `Optional[X]` alone doesn't make a field optional. Must provide default.

**Confidence:** HIGH — Documented in migration guide.

---

### 3. Using default_factory with ...

**Avoid:**
```python
class Model(BaseModel):
    items: List[str] = default_factory(lambda: [...])  # Don't use ... here
```

**Instead:**
```python
# For required fields, don't use default_factory with ...
class Model(BaseModel):
    items: List[str]  # Required, no default

# For optional fields with mutable defaults:
class Model(BaseModel):
    items: List[str] = Field(default_factory=list)
```

**Why:** Pydantic v2 treats `...` (Ellipsis) as "required, no default", not "use this default".

**Confidence:** HIGH — Pydantic v2 behavior.

---

## Adding New Features: Pattern Application

### New Language Certificates (HSK, DELE, CELPIP)

Follow the existing pattern:

1. **Create language-specific base** (if needed) — like `EnglishLanguageProficiencyCertificate`
2. **Create exam module** — e.g., `languages/certificates/zho/hsk.py`
3. **Define score types** — using `Annotated` + validators
4. **Define exam model** — inheriting from base, using `model_validator` for cross-field checks
5. **Add computed CEFR** — using `@computed_field`
6. **Export in `__init__.py`** — re-export from package root

### New Certifications (AWS, Azure, etc.)

1. **Create new domain module** — `src/pydanticcv/certifications/`
2. **Define certification base** — base model for all professional certs
3. **Define specific cert models** — each certification type as separate model
4. **Use model_validator** — for validity period checks, credential ID validation
5. **Export from package root** — `from pydanticcv.certifications import AWSSolutionArchitect`

### New Social/Profile Links

1. **Create new module** — `src/pydanticcv/profiles/` or extend existing
2. **Define URL-validated fields** — use `AnyUrl` with constraints
3. **Use Literal for platform types** — `Platform = Literal["LinkedIn", "GitHub", "Portfolio"]`
4. **Consider pydantic-extra-types** — `HolisticId` for ORCID, `Email` for email addresses

---

## Installation

```bash
# Core dependencies (already installed)
uv add pydantic pydantic-extra-types pycountry

# Testing
uv add -D pytest pytest-cov polyfactory faker

# Development
uv add -D ruff mypy pdoc prek tox
```

---

## Sources

- **Pydantic v2 Computed Fields**: https://docs.pydantic.dev/2.0/usage/computed_fields/ — HIGH confidence
- **Pydantic v2 Validators**: https://docs.pydantic.dev/2.0/usage/validators/ — HIGH confidence
- **Pydantic v2 Migration Guide**: https://docs.pydantic.dev/dev/migration/ — HIGH confidence
- **Polyfactory Pydantic Support**: https://polyfactory.litestar.dev/latest/reference/factories/pydantic_factory.html — HIGH confidence
