# Codebase Concerns

**Analysis Date:** 2026-04-03

## Tech Debt

**Education Module:**
- Issue: Incomplete implementation, marked with TODO
- Files: `src/pydanticcv/education/__init__.py`, `src/pydanticcv/education/education.py`
- Impact: Cannot be fully used in CV model
- Fix approach: Complete the EducationRecord model implementation

**Stale File Reference:**
- Issue: CLAUDE.md mentions `exams.py` as stale file that references non-existent `IELTSScores`
- Files: `CLAUDE.md` references `src/pydanticcv/languages/exams.py` but file doesn't exist
- Impact: Confusion about codebase state, stale documentation
- Fix approach: Remove reference from CLAUDE.md or verify/cleanup

## Known Bugs

**None identified** — Code appears stable for current functionality.

## Security Considerations

**None** — Pure schema validation library, no security concerns.

## Performance Bottlenecks

**None** — Schema validation is in-memory and fast.

## Fragile Areas

**Certificate Conversion Methods:**
- Files: `src/pydanticcv/languages/certificates/eng/toefl_ibt.py`, `src/pydanticcv/languages/certificates/eng/toefl_ibt_conversion.py`
- Why fragile: Uses reverse lookup tables with max-values for approximation
- Safe modification: Test thoroughly with edge cases
- Test coverage: Limited to existing test cases in `tests/test_toefl_ibt.py`

## Scaling Limits

**None** — Library scales with consumer application's data volume.

## Dependencies at Risk

**None identified** — All dependencies are stable, widely-used packages.

## Missing Critical Features

**None** — Core functionality for CV schema appears complete.

## Test Coverage Gaps

**Education module:**
- What's not tested: EducationRecord model
- Files: `src/pydanticcv/education/education.py`
- Risk: Validation bugs go unnoticed
- Priority: Medium (module marked TODO)

**Languages certificates (other than English):**
- What's not tested: German (Goethe), French (DELF/DALF/TCF) certificate models
- Files: `src/pydanticcv/languages/certificates/deu/`, `src/pydanticcv/languages/certificates/fra/`
- Risk: Validation bugs in non-English certificate handling
- Priority: Medium

---

*Concerns audit: 2026-04-03*