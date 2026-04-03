# Architecture

**Analysis Date:** 2026-04-03

## Pattern Overview

**Overall:** Schema-only library with hierarchical domain models

**Key Characteristics:**
- Domain-driven module organization (languages, employment, education, skills)
- Base model inheritance for shared functionality
- Barrel file pattern for public API
- Computed properties for derived values (e.g., CEFR level from exam scores)

## Layers

**Domain Models (`src/pydanticcv/`):**
- Purpose: Core business entities (CV, employment, education, skills, languages)
- Location: `src/pydanticcv/`
- Contains: Pydantic BaseModel subclasses
- Depends on: Pydantic core, pydantic-extra-types, pycountry
- Used by: Consumer applications importing the library

**Utilities (`src/pydanticcv/utils/`):**
- Purpose: Shared validation and transformation helpers
- Location: `src/pydanticcv/utils/`
- Contains: Date parsing, location handling
- Depends on: Pydantic validators

**Language Certificates (`src/pydanticcv/languages/certificates/`):**
- Purpose: Language proficiency exam models (IELTS, TOEFL, DELF, etc.)
- Location: `src/pydanticcv/languages/certificates/`
- Contains: Exam-specific Pydantic models with score validation
- Depends on: Base certificate model, CEFR types, PastDate

## Data Flow

**Model Instantiation:**
1. Consumer creates CV model instance
2. Validation runs on all fields
3. Computed properties calculate derived values
4. Model is ready for serialization/export

**Certificate Processing:**
1. Import specific exam model (IELTS, TOEFLITP, etc.)
2. Provide exam scores and date
3. Model validates score ranges
4. CEFR level computed from scores

## Key Abstractions

**LanguageProficiencyCertificate:**
- Purpose: Abstract base for all language exam records
- Examples: `src/pydanticcv/languages/certificates/base.py:23`
- Pattern: Inheritance + computed_field for CEFR

**PastDate:**
- Purpose: Validate past dates with multiple format support
- Examples: `src/pydanticcv/utils/date.py:66`
- Pattern: Annotated type with BeforeValidator

**CV:**
- Purpose: Root aggregate for complete resume
- Examples: `src/pydanticcv/cv/cv.py:34`
- Pattern: Composition of domain models

## Entry Points

**Main Entry:**
- Location: `src/pydanticcv/__init__.py`
- Triggers: `import pydanticcv`
- Responsibilities: Package initialization (empty)

**CV Model:**
- Location: `src/pydanticcv/cv/cv.py:34`
- Triggers: Import and instantiate CV
- Responsibilities: Compose all CV sections

**Language Certificates:**
- Location: `src/pydanticcv/languages/certificates/__init__.py`
- Triggers: Import exam models
- Responsibilities: Re-export all certificate types

## Error Handling

**Strategy:** Pydantic validation errors

**Patterns:**
- Field-level validation via field validators
- Model-level validation via model_validator
- Custom error messages for invalid inputs

## Cross-Cutting Concerns

**Validation:** Pydantic v2 built-in validators
**Serialization:** Pydantic model_dump() / model_json_schema()
**Documentation:** pdoc auto-generated from docstrings

---

*Architecture analysis: 2026-04-03*