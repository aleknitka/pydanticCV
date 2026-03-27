# pydanticCV

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

### IELTS

```python
from pydanticcv.languages.certificates import IELTS

cert = IELTS(
    DateTaken="2024-11-15",
    Link="https://results.britishcouncil.org/my-results",
    ExamType="Academic",
    TestCentreCode="GB001",
    Scores={
        "Listening": 8.5,
        "Reading": 8.0,
        "Writing": 7.5,
        "Speaking": 8.0,
        "Overall": 8.0,
    },
)

print(cert.CEFRLevel)   # C1
print(cert.Scores.Overall)  # 8.0
```

### TOEFL iBT (2026+ scale)

```python
from pydanticcv.languages.certificates import TOEFLiBT

cert = TOEFLiBT(
    DateTaken="2025-03-10",
    Link="https://scores.ets.org/toefl/12345",
    Scores={
        "Reading": 5.0,
        "Listening": 5.5,
        "Speaking": 4.5,
        "Writing": 5.0,
    },
)

print(cert.Scores.Overall)  # 5.0
print(cert.CEFRLevel)       # C1
```

### TOEFL iBT — legacy scale with conversion

```python
from pydanticcv.languages.certificates import TOEFLiBTLegacy

legacy = TOEFLiBTLegacy(
    DateTaken="2023-06-20",
    Link="https://scores.ets.org/toefl/99999",
    Scores={
        "Reading": 28,
        "Listening": 27,
        "Speaking": 26,
        "Writing": 27,
    },
)

print(legacy.Scores.Overall)  # 108
print(legacy.CEFRLevel)       # C1

new = legacy.to_new()
print(new.Scores.Overall)     # 5.5
```

### TOEFL ITP

```python
from pydanticcv.languages.certificates import TOEFLITP

cert = TOEFLITP(
    DateTaken="2024-04-01",
    Link="https://www.ets.org/toefl/itp",
    Level="Level 1",
    Scores={
        "ListeningComprehension": 60,
        "StructureWrittenExpression": 58,
        "ReadingComprehension": 56,
    },
)

print(cert.Scores.Total)  # 580
print(cert.CEFRLevel)     # C1
```

## Date formats

`DateTaken` accepts date objects or strings in any of these formats:

| Format | Example |
|---|---|
| ISO | `2024-11-15` |
| Numeric slash | `2024/11/15` |
| Numeric dot | `2024.11.15` |
| European | `15/11/2024` |
| US | `11/15/2024` |
| European dash | `15-11-2024` |
| US dash | `11-15-2024` |
| European dot | `15.11.2024` |

For ambiguous slash formats (e.g. `01/03/2024`) European order (DD/MM) is assumed.
Future dates are always rejected.

## CEFR levels

All certificate models expose a computed `CEFRLevel` field:

| Exam | A1 | A2 | B1 | B2 | C1 | C2 |
|---|---|---|---|---|---|---|
| IELTS | < 4.5 | — | 4.5–5.0 | 5.5–6.5 | 7.0–8.0 | ≥ 8.5 |
| TOEFL iBT (1-6) | < 2.0 | 2.0–2.5 | 3.0–3.5 | 4.0–4.5 | 5.0–5.5 | 6.0 |
| TOEFL ITP L1 | — | ≥ 310 | ≥ 337 | ≥ 460 | ≥ 543 | — |
| TOEFL ITP L2 | — | None | — | — | — | — |

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
