# English Language Certificates

Structured Pydantic models for English language proficiency exams.

## IELTS

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

print(cert.CEFRLevel)       # C1
print(cert.Scores.Overall)  # 8.0
```

## TOEFL iBT (2026+ scale)

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

## TOEFL iBT — legacy scale with conversion

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

## TOEFL ITP

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

## CEFR level mappings

| Exam | A1 | A2 | B1 | B2 | C1 | C2 |
|---|---|---|---|---|---|---|
| IELTS | < 4.5 | — | 4.5–5.0 | 5.5–6.5 | 7.0–8.0 | ≥ 8.5 |
| TOEFL iBT (1-6) | < 2.0 | 2.0–2.5 | 3.0–3.5 | 4.0–4.5 | 5.0–5.5 | 6.0 |
| TOEFL ITP L1 | — | ≥ 310 | ≥ 337 | ≥ 460 | ≥ 543 | — |
| TOEFL ITP L2 | — | None | — | — | — | — |
