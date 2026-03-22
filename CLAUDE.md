# pydanticCV — Claude Code Notes

## Project overview
Pydantic v2 schema library for structured CV/resume data. Python ≥ 3.13, managed with `uv`.

## Package layout
```
src/pydanticcv/
├── utils/
│   └── date.py                     # PastDate annotated type
└── languages/
    ├── levels.py                   # CEFRLevel (StrEnum), CEFR model
    ├── exams.py                    # STALE — do not import from here
    └── _exams_types/
        ├── base.py                 # LanguageProficiencyCertificate, CEFRLiteral
        └── eng/                    # English exam models
            ├── ielts.py
            ├── toefl_ibt.py
            ├── toefl_ibt_conversion.py
            └── toefl_itp.py
```

Public API: import from `pydanticcv.languages._exams_types` (the package `__init__.py` re-exports everything).

## Key types

### `PastDate` (`utils/date.py`)
`Annotated[date, BeforeValidator]` — accepts `date` objects or strings in 8 formats (ISO, `YYYY/MM/DD`, `YYYY.MM.DD`, European `DD/MM/YYYY`, US `MM/DD/YYYY`, and dash/dot variants). European order takes priority for ambiguous slash inputs. Rejects future dates.

### `LanguageProficiencyCertificate` (`_exams_types/base.py`)
Base model inherited by all exam records. Fields: `DateTaken: PastDate`, `Link: AnyUrl`.

### `CEFRLiteral` (`_exams_types/base.py`)
`Literal["A1", "A2", "B1", "B2", "C1", "C2"]` — used for `CEFRLevel` computed fields on all exam models. Do **not** import `CEFRLevel` from `levels.py` inside exam modules (circular import risk).

### IELTS (`eng/ielts.py`)
- `IELTSBandScore`: float 0–9 in 0.5 steps
- `IELTSTestCentreCode`: `^[A-Z]{2}\d+$` (e.g. `GB123`)
- `IELTSScores`: 4 sections + `Overall`; `@model_validator` checks overall = rounded average
- `IELTS`: adds `ExamType` (`"Academic"` | `"General Training"`), optional `TestCentreCode`, computed `CEFRLevel`

### TOEFL iBT (`eng/toefl_ibt.py` + `eng/toefl_ibt_conversion.py`)
Two models covering the pre-2026 and 2026+ scoring scales:
- `TOEFLiBTLegacy`: sections 0–30 (int), total 0–120. `CEFRLevel` via total lookup table.
- `TOEFLiBT`: sections 1–6 (float, 0.5 steps), overall = avg rounded to 0.5. `CEFRLevel` directly from overall.
- Conversion: `.to_new()` / `.to_legacy()` — use per-section ETS lookup tables in `toefl_ibt_conversion.py`.
- Reverse tables use **max** old value mapping to each new value (upper-bound approximation).
- `from __future__ import annotations` must be the **first line** after the module docstring (forward refs for conversion methods).

### TOEFL ITP (`eng/toefl_itp.py`)
- Three sections only (no Speaking): `ListeningComprehension`, `StructureWrittenExpression`, `ReadingComprehension`.
- Section scores: int 16–68. Total = `round((L + S + R) * 10 / 3)`.
- `TOEFLITP`: Level 1 (310–677) or Level 2 (200–500); `@model_validator` checks total in range.
- `CEFRLevel`: computed for Level 1 only (thresholds: C1≥543, B2≥460, B1≥337, A2≥310). Returns `None` for Level 2.

## Conventions
- **Docstrings**: Google style with `Args:`, `Returns:`, `Raises:`, `Attributes:` sections.
- **`__all__`**: every module declares `__all__` listing its public names.
- **Module docstrings**: every file starts with a module-level docstring listing its contents.
- **Pydantic v2**: use `computed_field` + `@property`, `AfterValidator`/`BeforeValidator`, `model_validator(mode="after")`.
- **Class/field naming**: PascalCase for models and fields (e.g. `DateTaken`, `CEFRLevel`).
- **No `default_factory` with `...`**: Pydantic v2 treats `...` as required; omit `default_factory` for required fields.
- **`Optional[X]` needs `= None`**: in Pydantic v2, `Optional[X]` alone is still required — always pair with `= None`.

## Running
```bash
uv run python -c "from pydanticcv.languages._exams_types import IELTS; print('OK')"
```

## Known stale file
`src/pydanticcv/languages/exams.py` — dead code referencing non-existent `IELTS_Scores`. Nothing imports it. Candidate for deletion.
