---
phase: "2"
plan: "additional-language-certificates-celpip-tef"
subsystem: "languages/certificates"
tags:
  - celpip
  - tef
  - language-certificates
  - pydantic
dependency_graph:
  requires:
    - "LANG-02"
    - "LANG-03"
  provides:
    - "CELPIP model with CLB validation"
    - "TEF model with 6-section validation"
  affects:
    - "pydanticcv.languages.certificates"
    - "src/pydanticcv/languages/certificates/eng/__init__.py"
    - "src/pydanticcv/languages/certificates/fra/__init__.py"
tech_stack:
  added:
    - "CELPIP CLB score validation (4-12)"
    - "TEF section score validation (0-20)"
    - "CEFR level computation for both models"
key_files:
  created:
    - "src/pydanticcv/languages/certificates/eng/celpip.py"
    - "src/pydanticcv/languages/certificates/fra/tef.py"
    - "tests/test_celpip.py"
    - "tests/test_tef.py"
  modified:
    - "src/pydanticcv/languages/certificates/__init__.py"
    - "src/pydanticcv/languages/certificates/eng/__init__.py"
    - "src/pydanticcv/languages/certificates/fra/__init__.py"
decisions:
  - "CELPIP computes CEFR from average CLB score (rounded)"
  - "TEF computes CEFR from average of 6 section scores (rounded)"
metrics:
  duration: "3 min 39 sec"
  completed: "2026-04-03T09:16:18Z"
  tasks_completed: "4"
  test_count: "56"
---

# Phase 2 Plan: Additional Language Certificates (CELPIP, TEF) Summary

## One-Liner

CELPIP (Canadian English) and TEF (French) language certificate models with validated CLB/section scores and computed CEFR levels.

## Task Completion

| Task | Name                              | Commit | Files                      |
| ---- | --------------------------------- |--------|----------------------------|
| 1    | CELPIP module structure           | 6cc34a0| celpip.py                  |
| 2    | CELPIP score types (CLB 4-12)    | 6cc34a0| celpip.py                  |
| 3    | CELPIP scores model               | 6cc34a0| celpip.py                  |
| 4    | CELPIP main model + CEFR          | 6cc34a0| celpip.py                  |
| 5    | TEF module structure             | 6cc34a0| tef.py                     |
| 6    | TEF score types (0-20)           | 6cc34a0| tef.py                     |
| 7    | TEF scores model (6 sections)    | 6cc34a0| tef.py                     |
| 8    | TEF main model + CEFR            | 6cc34a0| tef.py                     |
| 9    | Export from certificates package | 6cc34a0| __init__.py files          |
| 10   | CELPIP tests                      | 6cc34a0| test_celpip.py             |
| 11   | TEF tests                         | 6cc34a0| test_tef.py                |

## Acceptance Criteria Status

- [x] CELPIP CLB score validation (4-12 range)
- [x] CELPIP CEFR level computation
- [x] TEF 6-section score validation (0-20 each)
- [x] TEF CEFR level computation
- [x] Tests pass (56 tests)
- [x] Exports work from public API

## CEFR Mappings

### CELPIP (from average CLB 4-12)
- CLB 12 → C2
- CLB 10-11 → C1
- CLB 8-9 → B2
- CLB 7 → B1
- CLB 4-6 → A2

### TEF (from average score 0-20)
- 14-20 → C2
- 10-13 → C1
- 8-9 → B2
- 6-7 → B1
- 4-5 → A2
- 0-3 → A1

## Deviations from Plan

None - plan executed exactly as written.

## Test Results

```
============================= test session starts ==============================
tests/test_celpip.py .....
tests/test_tef.py ......
============================== 56 passed in 0.41s ==============================
```

## Self-Check: PASSED

- All created files verified
- Commit hash verified: 6cc34a0
- Public API exports verified
