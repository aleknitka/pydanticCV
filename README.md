# pydanticCV

[![codecov](https://codecov.io/github/aleknitka/pydanticCV/branch/main/graph/badge.svg?token=BLSHNSUJX1)](https://codecov.io/github/aleknitka/pydanticCV)

Structured Pydantic v2 schemas for CV/resume data — type-safe, validated, and ready to serialise.

## Overview

pydanticCV provides Pydantic models for the structured data that appears in a CV or resume.
The first focus area is **language proficiency certificates**: IELTS, TOEFL iBT (both legacy 0-120 and current 1-6 scales), and TOEFL ITP.

Every model validates its inputs on construction, computes derived fields (overall scores, CEFR levels) automatically, and serialises cleanly to JSON.

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Installation

```bash
pip install pydanticcv
```

Or with uv:

```bash
uv add pydanticcv
```

## Quick start

```python
from pydanticcv.languages.certificates import IELTS

cert = IELTS(
    DateTaken="2024-11-15",
    Link="https://results.britishcouncil.org/my-results",
    ExamType="Academic",
    Scores={"Listening": 8.5, "Reading": 8.0, "Writing": 7.5, "Speaking": 8.0, "Overall": 8.0},
)

print(cert.CEFRLevel)   # C1
```

See [languages/certificates/eng/README.md](src/pydanticcv/languages/certificates/eng/README.md) for examples of all supported exams (IELTS, TOEFL iBT, TOEFL ITP).

## Package layout

```
src/pydanticcv/
├── utils/
│   └── date.py                         # PastDate annotated type
└── languages/
    ├── levels.py                       # CEFRLevel enum, CEFR model
    └── certificates/
        ├── base.py                     # LanguageProficiencyCertificate base
        └── eng/                        # English language certificates
            ├── base.py                 # EnglishLanguageProficiencyCertificate
            ├── ielts.py
            ├── toefl_ibt.py
            ├── toefl_ibt_conversion.py # ETS official lookup tables
            └── toefl_itp.py
```

## Development

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src/pydanticcv --cov-report=term-missing

# Lint and format
uv run ruff check --fix src/ tests/
uv run ruff format src/ tests/

# Type check
uv run ty check src/
```

## License

See [LICENSE](LICENSE).
Note: This repository uses CI workflows to validate code changes, including a dedicated tox workflow to test multiple Python versions on PRs and main/release merges.
