# Project Research Summary

**Project:** pydanticCV
**Domain:** Pydantic v2 Schema Library for CV/Resume Data
**Researched:** 2026-04-03
**Confidence:** HIGH

## Executive Summary

pydanticCV is a schema library providing Pydantic v2 models for structured CV/resume data. The existing codebase already follows all recommended Pydantic v2 patterns correctly — the library is well-architected. Research confirms the three feature areas for extension: **language certificates** (beyond existing IELTS/TOEFL: HSK, CELPIP, TEF, Cambridge), **professional certifications** (AWS, Azure, PMI), and **social profile links**.

The key insight: **this is a mature, well-designed library extending existing patterns**. No architectural changes needed. The roadmap should prioritize new language certificates (high demand for immigration: HSK for Chinese, CELPIP for Canada, TEF for Quebec), then professional certifications, then social links. The main risks are incorrect CEFR threshold mappings and circular import issues with new modules — both preventable with the documented patterns.

## Key Findings

### Recommended Stack

The codebase already uses all recommended Pydantic v2 patterns correctly:
- **Base model inheritance** via `LanguageProficiencyCertificate` 
- **`Annotated` type aliases** for constrained types (e.g., `IELTSBandScore`)
- **`BeforeValidator`** for string→date parsing (e.g., `PastDate`)
- **`@model_validator(mode="after")`** for cross-field validation (e.g., IELTS score consistency)
- **`@computed_field` + `@property`** for CEFR computation
- **Module-level type aliases** for forward references (TOEFL conversion methods)

**Core dependencies** (already in place): pydantic ^2.12, pydantic-extra-types ^2.11, pycountry ^24.6, polyfactory ^3.3 for testing.

### Expected Features

**Must have (table stakes):**
- **HSK (Chinese)** — Major global language test, required for Chinese university/work visas
- **CELPIP (Canadian)** — Required for Canadian Express Entry immigration
- **TEF/TEFaCM (French)** — Quebec immigration requirement, distinct from TCF
- **Professional certification model** — Name, issuer, date, optional URL with issuer validation
- **Social profile links** — Platform + URL with URL validation and platform detection

**Should have (differentiators):**
- **CEFR computation** — Already implemented, extend to new exams
- **Score validation** — Reject invalid score combinations per exam rules
- **Issuer allowlist** — Validate against known issuers (AWS, Azure, GCP, PMI, ISC2)

**Defer (v2+):**
- Credential URL parsing (too variable across issuers)
- QR code generation for personal sites (out of scope)
- OpenGraph metadata fetching (network calls, async complexity)

### Architecture Approach

The codebase uses a **three-level inheritance pattern** for language certificates:
```
LanguageProficiencyCertificate (universal base)
    └── EnglishLanguageProficiencyCertificate (language base)
            └── IELTS, TOEFLiBT, TOEFLITP (exam models with CEFR)
```

For new languages (Chinese, Spanish), create a language-specific base first, then exam models. Professional certifications extend `SkillCertificate` already in `skills/certificates/base.py`. Social links already exist in `cv/personal_info.py`.

**Key pattern:** Always use `CEFRLiteral` from `certificates/base.py` — never import from `levels.py` (circular import risk).

### Critical Pitfalls

1. **Circular imports with CEFR types** — Use `CEFRLiteral` from `base.py`, never from `levels.py`
2. **Incorrect score-to-CEFR thresholds** — Must verify against official ETS/IELTS/Goethe documentation; each exam has unique mapping
3. **Reverse lookup approximation** — TOEFL new↔legacy conversion loses precision (documented, but users may not expect)
4. **URL validation too permissive** — Use `AnyUrl` with `scheme="https"` constraint for certificate links
5. **Missing `__all__` exports** — Every new module must declare public exports

## Implications for Roadmap

Based on research, suggested phase structure:

### Phase 1: Chinese Language Certificates (HSK)
**Rationale:** High demand for Chinese language certification in immigration contexts. HSK 3.0 is well-documented with CEFR mapping. Can establish the pattern for adding new language certificates.

**Delivers:** `ChineseLanguageProficiencyCertificate` base class, `HSK` exam model with CEFR computation (HSK5→C1, HSK4→B2, HSK3→B1, HSK1-2→A2)

**Avoids:** Pitfall 1 (use CEFRLiteral from base.py), Pitfall 2 (verify thresholds against Hanban documentation)

**Research needed:** HSK 3.0 CEFR mapping is preliminary — verify against official sources before implementing.

### Phase 2: Additional Language Certificates (CELPIP, TEF)
**Rationale:** Strong immigration driver — CELPIP for Canada Express Entry, TEF for Quebec. Both follow established pattern after Phase 1.

**Delivers:** CELPIP model (CLB 4-12 → A1-C2 mapping), TEF model (0-900 scale, 6 sections)

**Avoids:** Pitfall 2 (CELPIP CLB→CEFR tables well-documented; TEF needs verification of 6-section scoring)

**Research needed:** TEF exact scoring ranges (6 sections); CELPIP vs CELPIP-LS distinction

### Phase 3: Professional Certifications
**Rationale:** Standard CV section, simple models extending existing `SkillCertificate`. Low complexity, high value.

**Delivers:** Certification model with issuer validation (allowlist: AWS, Azure, GCP, PMI, ISC2, CompTIA), expiry date tracking

**Avoids:** Pitfall 5 (URL validation), Pitfall 6 (inheritance from SkillCertificate)

### Phase 4: Social Profile Links
**Rationale:** Already partially implemented in `cv/personal_info.py`. Extend with platform detection and validation.

**Delivers:** Platform detection from URL, username validation per platform, additional platforms beyond existing LinkedIn/GitHub

**Avoids:** Pitfall 5 (use HTTPS constraint, platform-specific validation)

### Phase Ordering Rationale

- **Language certificates first** — Highest complexity (CEFR mapping, score validation), most value for immigration use cases
- **Certifications second** — Simple extension of existing pattern, straightforward implementation
- **Social links last** — Already partially exists, lower priority

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | All patterns verified against Pydantic v2 official docs; existing code already correct |
| Features | MEDIUM | Ecosystem well-established (JSON Resume); specific exam thresholds need verification |
| Architecture | HIGH | Three-level pattern validated against existing codebase |
| Pitfalls | HIGH | All pitfalls identified from existing code patterns and migration guide |

**Overall confidence:** HIGH

### Gaps to Address

- **HSK 3.0 CEFR mapping:** Not officially published by Hanban — use preliminary mapping but flag as needs verification
- **TEF exact scoring:** Need official score ranges for 6 sections — document as research task for Phase 2
- **CELPIP vs CELPIP-LS:** Both accepted for immigration — decide if both models needed or single model with optional Listening/Speaking

## Sources

### Primary (HIGH confidence)
- Pydantic v2 Computed Fields docs — https://docs.pydantic.dev/2.0/usage/computed_fields/
- Pydantic v2 Validators docs — https://docs.pydantic.dev/2.0/usage/validators/
- Pydantic v2 Migration Guide — https://docs.pydantic.dev/dev/migration/
- Existing codebase patterns — `ielts.py`, `toefl_ibt.py`, `toefl_ibt_conversion.py`

### Secondary (MEDIUM confidence)
- JSON Resume Schema — community standard for feature expectations
- IELTS official band descriptors — https://ielts.org/take-a-test/preparation/resources/band-descriptors
- ETS TOEFL score conversion — https://www.ets.org/toefl/institutions/ibt/score-scale-update.html

### Tertiary (LOW confidence)
- HSK 3.0 CEFR mapping — preliminary, not officially published
- TEF 6-section scoring ranges — need verification from official source

---
*Research completed: 2026-04-03*
*Ready for roadmap: yes*