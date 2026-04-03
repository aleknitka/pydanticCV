# Domain Pitfalls

**Domain:** Pydantic v2 schema library for CV/resume data
**Researched:** 2026-04-03

## Critical Pitfalls

Mistakes that cause rewrites or major issues.

### Pitfall 1: Circular Import Chains with CEFR Types

**What goes wrong:** Importing `CEFRLevel` (StrEnum) from `levels.py` inside certificate modules creates circular dependency when models inherit from base classes that import from `levels.py`.

**Why it happens:** The codebase already has `CEFRLiteral` in `base.py` as the correct solution, but new certificate modules may incorrectly try to import from `levels.py`.

**Consequences:**
- Import-time failures
- Type resolution errors at runtime
- `ImportError` or `ModuleNotFoundError` during model instantiation

**Prevention:**
- Always use `CEFRLiteral` from `pydanticcv.languages.certificates.base` in new certificate modules
- Never import from `levels.py` inside certificate submodules
- Verify import graph with `python -c "from pydanticcv.languages.certificates import *"`

**Detection:** Run import test after adding any new certificate module.

**Phase:** Language certificate addition phase.

---

### Pitfall 2: Incorrect Score-to-CEFR Mapping Thresholds

**What goes wrong:** Using incorrect threshold boundaries for CEFR level computation. For example, misplacing the B2/C1 boundary or using wrong score ranges.

**Why it happens:**
- Different exam bodies use different scales (IELTS 0-9, TOEFL 0-120, Goethe 0-100)
- Each has unique CEFR mapping tables from official documentation
- Copy-pasting thresholds from wrong exam type

**Consequences:**
- Users get incorrect CEFR levels
- CV data becomes unreliable
- Requires data migration for existing records

**Prevention:**
- Always verify thresholds against official ETS, IELTS, or Goethe documentation
- For IELTS: C1≥8.5, B2≥5.5, B1≥4.5, A2/A1<4.5 (per ielts.py line 112-122)
- For TOEFL (new 1-6): C2≥6.0, C1≥5.0, B2≥4.0, B1≥3.0, A2≥2.0 (per toefl_ibt.py line 60-71)
- Create unit tests that assert known score-to-level mappings

**Detection:** Add explicit threshold tests: `assert IELTS(scores=..., overall=8.5).CEFRLevel == "C1"`

**Phase:** Language certificate addition phase.

---

### Pitfall 3: Reverse Lookup Table Approximation Errors

**What goes wrong:** The TOEFL conversion uses reverse tables that map to max-legacy-values, causing data loss when converting new→legacy→new roundtrip.

**Why it happens:** Multiple legacy scores (0-30) map to same new score (1-6), so reverse is not unique. The code correctly uses upper-bound approximation, but this isn't documented clearly.

**Consequences:**
- `to_legacy().to_new()` produces different scores than original
- Users unaware of approximation may rely on conversion for exact values
- Data accuracy issues in migration scenarios

**Prevention:**
- Document that reverse conversion is approximate (already done in toefl_ibt.py line 227-229)
- Add explicit warning in conversion method docstrings
- Consider adding roundtrip test that asserts approximation is within tolerance
- For new certificate conversions, decide upfront: exact or approximate?

**Detection:** Run roundtrip conversion test: `original.to_legacy().to_new() == original`

**Phase:** Any certificate conversion feature.

---

### Pitfall 4: Missing Validation in Computed Fields

**What goes wrong:** Computed fields like `CEFRLevel` or `Total` don't validate when their source fields are invalid, because computation happens after validation.

**Why it happens:** Pydantic v2 `computed_field` with `@property` runs after all field validation. If invalid data slips through (edge case), computation may produce unexpected results or crash.

**Consequences:**
- Runtime errors for edge-case invalid inputs
- Silent wrong values if validation order is incorrect

**Prevention:**
- Use `@model_validator(mode="after")` to validate consistency between computed and source fields (like IELTS `check_overall_is_consistent` in ielts.py line 64-85)
- Add defensive checks in computed properties
- Test with boundary values: min/max scores, invalid combinations

**Detection:** Fuzz test with invalid score combinations.

**Phase:** Language certificate addition phase.

---

### Pitfall 5: URL Validation Too Permissive or Too Strict

**What goes wrong:** Using `AnyUrl` without constraints may accept invalid URLs (missing scheme, malformed). Using overly strict regex blocks valid variations.

**Why it happens:** Pydantic's `AnyUrl` is permissive by default (accepts any scheme). Certificate links need specific validation (should be HTTPS, specific domains).

**Consequences:**
- Invalid links in CV data
- External systems rejecting exported data
- User confusion when valid certificate URLs are rejected

**Prevention:**
- For certificate links: use `AnyUrl` with `scheme="https"` constraint: `Annotated[AnyUrl, UrlConstraints(scheme="https")]`
- Add allowed host validation for known exam providers (e.g., `ieltS.org`, `ets.org`)
- Document expected URL format in model docstring

**Detection:** Try creating model with HTTP (non-SSL) URL, or malformed URL.

**Phase:** Adding new certificate types, adding social links section.

---

## Moderate Pitfalls

### Pitfall 6: Inheritance Hierarchy Mismatch

**What goes wrong:** New certificate model doesn't inherit from correct base (`LanguageProficiencyCertificate` or language-specific base like `EnglishLanguageProficiencyCertificate`), breaking shared fields (`DateTaken`, `Link`).

**Why it happens:** Copy-pasting from non-certificate models (e.g., `EmploymentRecord`) which have different field requirements.

**Prevention:**
- Verify inheritance: `class IELTS(EnglishLanguageProficiencyCertificate)`
- Check that base class provides required fields
- New language certificates need language-specific base (e.g., for HSK: `ChineseLanguageProficiencyCertificate`)

**Phase:** Adding new language certificates.

---

### Pitfall 7: Module `__all__` Incomplete or Missing

**What goes wrong:** New certificate module doesn't export all public types in `__all__`, breaking `from pydanticcv.languages.certificates import *` pattern.

**Prevention:**
- Always declare `__all__` with all public names (follow existing pattern in ielts.py line 17)
- Include base types, score types, model classes, and literals

**Phase:** Any new module addition.

---

### Pitfall 8: Docstring Style Inconsistency

**What goes wrong:** New module lacks Google-style docstrings with `Attributes:`, `Args:`, `Returns:`, breaking project convention.

**Prevention:**
- Follow existing docstring format (see ielts.py lines 1-15)
- Include table of contents in module docstring

**Phase:** Any new module addition.

---

## Minor Pitfalls

### Pitfall 9: Hardcoded Score Validation Ranges

**What goes wrong:** Hardcoding score bounds instead of using constants, making it harder to update when exam scoring changes (as happened with TOEFL 2026).

**Prevention:** For exam scoring subject to change, consider:
- Document source (e.g., "ETS 2026 scoring scale")
- Add comment about when scoring may change
- Consider version parameter if exam body changes frequently

**Example:** TOEFL iBT 2026+ uses 1-6 scale (per toefl_ibt.py), while legacy was 0-30. The module correctly distinguishes both.

**Phase:** Adding any exam with known scoring changes.

---

### Pitfall 10: Type Annotation Forward Reference Issues

**What goes wrong:** Using string forward references (`"IELTSScores"`) without proper handling, causing `NameError` at runtime.

**Why it happens:** For methods that return the model class itself, need proper forward reference handling.

**Prevention:**
- Use `from __future__ import annotations` at module top (as done in toefl_ibt.py line 20)
- This enables PEP 563 deferred evaluation

**Phase:** Any model with self-referential methods.

---

## Phase-Specific Warnings

| Phase Topic | Likely Pitfall | Mitigation |
|-------------|---------------|------------|
| Add HSK Chinese certificates | Pitfall 1 (circular import) | Use CEFRLiteral from base.py |
| Add DELE Spanish | Pitfall 2 (wrong CEFR thresholds) | Verify against Instituto Cervantes official tables |
| Add social links section | Pitfall 5 (URL validation) | Use HTTPS constraint, consider platform-specific validation |
| Add certifications section | Pitfall 6 (inheritance) | Define base model first with shared fields |
| Add any new language | Pitfall 6 (inheritance) | Create language-specific base before certificate models |

---

## Sources

- Project existing code: `src/pydanticcv/languages/certificates/eng/ielts.py`, `toefl_ibt.py`, `toefl_ibt_conversion.py`
- Pydantic v2 computed fields: https://docs.pydantic.dev/2.3/usage/computed_fields/
- IELTS official band descriptors: https://ielts.org/take-a-test/preparation/resources/band-descriptors
- ETS TOEFL score conversion: https://www.ets.org/toefl/institutions/ibt/score-scale-update.html