# Codebase Structure

**Analysis Date:** 2026-04-03

## Directory Layout

```
pydanticCV/
├── src/pydanticcv/           # Main package
│   ├── __init__.py           # Package init (empty)
│   ├── utils/                # Shared utilities
│   │   ├── date.py           # PastDate type
│   │   └── locations.py      # Location helpers
│   ├── cv/                   # CV root model
│   │   ├── cv.py             # CV class
│   │   └── personal_info.py  # PersonalInfo model
│   ├── employment/          # Employment history
│   │   ├── history.py        # EmploymentHistory
│   │   ├── record.py        # EmploymentRecord
│   │   ├── breaks.py        # EmploymentGap
│   │   └── types.py         # Employment type enums
│   ├── education/           # Education records (TODO)
│   ├── skills/               # Skills & certificates
│   │   ├── skill.py         # Skill model
│   │   ├── levels.py        # Skill level enums
│   │   └── certificates/    # Skill certifications
│   ├── languages/           # Language models
│   │   ├── languages.py     # NativeLanguage, etc.
│   │   ├── self_reported.py # Self-reported CEFR
│   │   └── certificates/    # Language exam certs
│   │       ├── base.py     # LanguageProficiencyCertificate
│   │       ├── eng/        # English exams (IELTS, TOEFL)
│   │       ├── fra/        # French exams (DELF, DALF, TCF)
│   │       └── deu/        # German exams (Goethe)
│   ├── projects/            # Portfolio projects
│   ├── publications/        # Academic publications
│   │   ├── base.py         # Publication base
│   │   ├── journal.py     # Journal article
│   │   └── arxiv.py        # ArXiv paper
│   ├── activities/         # Volunteering
│   ├── references/         # Professional references
│   └── awards/             # Awards & honors
├── tests/                   # Test suite
├── docs/                   # pdoc output
└── .planning/codebase/     # GSD planning docs
```

## Directory Purposes

**Core Package (`src/pydanticcv/`):**
- Purpose: Main library code
- Contains: Pydantic schema models
- Key files: `cv/cv.py`, `languages/certificates/__init__.py`

**Utilities (`src/pydanticcv/utils/`):**
- Purpose: Shared validation helpers
- Contains: Date parsing, location types

**Domain Modules:**
- Purpose: Each maps to a CV section
- Contains: Domain-specific Pydantic models

## Key File Locations

**Entry Points:**
- `src/pydanticcv/cv/cv.py`: Root CV model
- `src/pydanticcv/languages/certificates/__init__.py`: Certificate types

**Configuration:**
- `pyproject.toml`: Package manifest, dependencies, tox config
- `prek.toml`: Pre-commit hooks

**Testing:**
- `tests/`: Test files (test_*.py)
- `conftest.py`: Pytest fixtures

## Naming Conventions

**Files:**
- snake_case.py: Modules
- domain_name.py: Single-class modules
- domain_plural.py: Multiple-class modules

**Directories:**
- snake_case: All directories

**Classes:**
- PascalCase: All model classes

**Fields:**
- PascalCase: All Pydantic fields (e.g., `DateTaken`, `CEFRLevel`)

## Where to Add New Code

**New Feature:**
- Primary code: `src/pydanticcv/{domain}/`
- Tests: `tests/test_{domain}.py`

**New Certificate Type:**
- Implementation: `src/pydanticcv/languages/certificates/{lang}/`
- Public export: `src/pydanticcv/languages/certificates/__init__.py`

**Utilities:**
- Shared helpers: `src/pydanticcv/utils/`

## Special Directories

**`.planning/codebase/`:**
- Purpose: GSD planning documents
- Generated: Yes
- Committed: Yes (in git)

**`docs/`:**
- Purpose: pdoc HTML output
- Generated: Yes
- Committed: No (in .gitignore)

---

*Structure analysis: 2026-04-03*