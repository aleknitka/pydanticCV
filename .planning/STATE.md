# State

## Project Reference

**Project:** pydanticCV
**Core Value:** Validated CV schema models that can be imported and used to create type-safe resume data with built-in validation.
**Current Focus:** Phase 1: Chinese Language Certificates (HSK)

## Current Position

| Attribute | Value |
|-----------|-------|
| **Phase** | 1 |
| **Plan** | Not started |
| **Status** | Not started |
| **Progress** | ████░░░░░░░ 0% |

## Performance Metrics

| Metric | Value |
|--------|-------|
| Requirements Mapped | 0/9 |
| Plans Completed | 0/4 |
| Phases Completed | 0/4 |

## Accumulated Context

### Decisions Made

- **Phase-driven delivery**: Each phase delivers a complete, verifiable capability
- **Language-first ordering**: Language certificates (highest complexity) first, then certifications, then social links
- **CEFR as computed property**: Extend existing pattern using `@computed_field` + `@property`

### Research Findings

- HSK 3.0 CEFR mapping is preliminary (not officially published by Hanban)
- CELPIP CLB→CEFR tables well-documented for Canada Express Entry
- TEF 6-section scoring needs verification from official source
- Use CEFRLiteral from certificates/base.py (never from levels.py) to avoid circular imports

### Todos

- [ ] Plan Phase 1: HSK implementation
- [ ] Research: Verify HSK 3.0 CEFR thresholds against official Hanban documentation
- [ ] Implement ChineseLanguageProficiencyCertificate base class
- [ ] Implement HSK model with score validation and CEFR computation

### Blockers

- **HSK 3.0 CEFR mapping**: Not officially published — using preliminary mapping, need to flag as needs verification

## Session Continuity

### Last Session (2026-04-03)

**Completed:**
- Project initialization
- Research phase (4 parallel researchers + synthesis)
- Requirements defined (9 v1 requirements)
- Roadmap created (4 phases derived from requirements)

**Next:**
- Plan Phase 1 (HSK implementation)
- Execute Phase 1

---

*State updated: 2026-04-03*