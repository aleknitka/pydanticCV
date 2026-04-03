# pydanticCV

## What This Is

A Pydantic v2 schema library providing structured data models for CVs/resumes. Provides validated Pydantic models for employment history, education, skills, language certificates, publications, projects, volunteering, references, and awards.

## Core Value

Validated CV schema models that can be imported and used to create type-safe resume data with built-in validation.

## Requirements

### Validated

- ✓ CV model with personal info, employment, education, skills sections — existing
- ✓ Language certificates (IELTS, TOEFL iBT, TOEFL ITP, DELF/DALF, TCF, Goethe) — existing
- ✓ PastDate validator for date parsing — existing
- ✓ CEFR level computation from exam scores — existing
- ✓ Employment history with gap detection — existing
- ✓ Publications (journal, arxiv) — existing
- ✓ Projects portfolio — existing
- ✓ Volunteering activities — existing
- ✓ Professional references — existing
- ✓ Awards and honors — existing

### Active

- [ ] Add new language certificates (HSK Chinese, DELE Spanish, CELPIP Canadian)
- [ ] Add Certifications CV section (professional certifications like AWS, Azure)
- [ ] Add Social/Profile links CV section (LinkedIn, GitHub, portfolio URLs)

### Out of Scope

- Web UI for CV editing — library only
- PDF/JSON export functionality — data models only
- Resume parsing from documents — future consideration

## Context

The project is an established Python library using Pydantic v2 with Python 3.13+ target. Already has comprehensive language certificate support for English, German, and French exams. The library follows domain-driven module organization with inheritance patterns for shared functionality.

Existing codebase map in `.planning/codebase/` documents the architecture.

## Constraints

- **Python version**: ≥3.13 — project requirement
- **Package manager**: uv — project convention
- **Validation**: All fields must be validated via Pydantic v2
- **CEFR compatibility**: Language certificates must compute CEFR levels

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Domain-driven module structure | Clear separation of concerns | ✓ Good |
| Base model inheritance for certificates | Shared fields (DateTaken, Link) | ✓ Good |
| Computed properties for CEFR levels | Single source of truth for scoring | ✓ Good |

---

*Last updated: 2026-04-03 after initialization*

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state
