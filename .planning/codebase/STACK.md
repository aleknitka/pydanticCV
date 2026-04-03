# Technology Stack

**Analysis Date:** 2026-04-03

## Languages

**Primary:**
- Python 3.11–3.15 — Core Pydantic schema library

**Secondary:**
- None (pure schema library, no other languages)

## Runtime

**Environment:**
- Python standard library

**Package Manager:**
- uv (latest)
- Lockfile: `uv.lock` present

## Frameworks

**Core:**
- Pydantic v2.12.5 — Data validation schemas
- pydantic-extra-types 2.11.1 — Extended types (phonenumbers, language codes)
- pycountry 24.6.1 — Country data
- prek 0.3.6 — Pre-commit hooks

**Testing:**
- pytest 9.0.2 — Test runner
- pytest-cov 7.1.0 — Coverage reporting
- polyfactory 3.3.0 — Test data generation
- faker 40.11.0 — Fake data generation

**Build/Dev:**
- tox 4.50.3 — Multi-version testing
- ruff 0.15.7 — Linting and formatting
- pdoc 16.0.0 — Documentation generation
- ty — Type checking

## Key Dependencies

**Critical:**
- pydantic[email] 2.12.5 — Core validation framework
- pydantic-extra-types[phonenumbers] 2.11.1 — Phone numbers, language codes
- pycountry 24.6.1 — ISO country data

**Infrastructure:**
- prek 0.3.6 — Pre-commit hook management

## Configuration

**Environment:**
- No runtime environment variables required
- Static schema library

**Build:**
- `pyproject.toml` — Project configuration
- `prek.toml` — Pre-commit hooks configuration

## Platform Requirements

**Development:**
- Python 3.11+

**Production:**
- Python 3.11+
- Install via: `pip install pydanticcv`

---

*Stack analysis: 2026-04-03*