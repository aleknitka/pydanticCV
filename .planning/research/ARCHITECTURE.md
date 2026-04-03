# Architecture Patterns: Adding New Certificate Types

**Research Date:** 2026-04-03
**Domain:** Language certificates, certifications, social links
**Confidence:** HIGH

## Executive Summary

The pydanticCV library uses a **hierarchical inheritance pattern** for language certificates with three levels: universal base (`LanguageProficiencyCertificate`), language-specific base (e.g., `EnglishLanguageProficiencyCertificate`), and exam-specific models (e.g., `IELTS`, `TOEFLiBT`). This pattern enables CEFR computation at the exam level while maintaining shared fields through inheritance.

For new language certificates (HSK, DELE, CELPIP), follow the established three-level pattern. For professional certifications and social links, the architecture already supports these via existing patterns that can be extended.

## Recommended Architecture

### Component Boundaries

| Component | Responsibility | Public API | Depends On |
|-----------|---------------|------------|------------|
| `languages/certificates/base.py` | Universal certificate base | `LanguageProficiencyCertificate`, `CEFRLiteral` | PastDate, ISO639_3 |
| `languages/certificates/eng/` | English exam models | IELTS, TOEFL models | eng/base.py |
| `languages/certificates/{lang}/` | Language-specific base | `{Lang}LanguageProficiencyCertificate` | languages/languages.py |
| `languages/certificates/{lang}/{exam}.py` | Exam-specific model | Exam model with CEFR computation | lang/base.py |
| `skills/certificates/` | Professional certifications | `SkillCertificate` | PastDate |
| `cv/personal_info.py` | Social links | Existing ContactInfo | AnyUrl |

### Language Certificate Pattern

```
LanguageProficiencyCertificate (base)
    │
    └── EnglishLanguageProficiencyCertificate (language base)
            │
            └── IELTS (exam model with CEFR)
            └── TOEFLiBT
            └── TOEFLITP
```

**For new languages (Chinese, Spanish, etc.):**

```
LanguageProficiencyCertificate
    │
    └── ChineseLanguageProficiencyCertificate (new)
            │
            └── HSK (new)
            └── HSKK (new)
```

### Data Flow

1. **Import:** Consumer imports exam model from `pydanticcv.languages.certificates`
2. **Instantiation:** Provide scores, date, exam metadata
3. **Validation:** Field validators → model validators → computed properties
4. **Computation:** CEFR level derived via `@computed_field` property
5. **Integration:** Certificate added to CV.LanguageCertificates list

### Build Order Implications

| Phase | Dependencies | Rationale |
|-------|--------------|------------|
| 1. Language-specific base | `LanguageProficiencyCertificate`, `Language` model | Establishes foundation for all exams in that language |
| 2. First exam model | Language base, CEFR thresholds | MVP for that language |
| 3. Additional exams | Same language base | Reuse base class |
| 4. Public API update | All exam modules | Add to `__init__.py` exports |

## Patterns to Follow

### Pattern 1: Three-Level Inheritance

**What:** Language certificates use universal base → language base → exam model

**When:** Adding any new language certificate

**Example:**

```python
# Level 1: Universal base (already exists)
class LanguageProficiencyCertificate(BaseModel):
    DateTaken: PastDate
    Link: AnyUrl
    LanguageCertified: ISO639_3

# Level 2: Language base (create for new language)
class ChineseLanguageProficiencyCertificate(LanguageProficiencyCertificate):
    CertifiedLanguage: ClassVar[Language] = Language(name="Chinese", iso=ISO639_3("zho"))

# Level 3: Exam model (create per exam)
class HSK(LanguageProficiencyCertificate):
    Level: int  # 1-6
    Score: int  # 0-100
    
    @computed_field
    @property
    def CEFRLevel(self) -> CEFRLiteral:
        # Map HSK level to CEFR
        ...
```

### Pattern 2: CEFR Computation via @computed_field

**What:** CEFR level derived from scores using @computed_field + @property

**When:** Any exam that maps to CEFR levels

**Example:**

```python
class SomeExam(LanguageBase):
    Scores: SomeScoresModel
    
    @computed_field
    @property
    def CEFRLevel(self) -> CEFRLiteral:
        # Lookup or computation logic
        ...
```

**Why:** Single source of truth; Pydantic handles caching; type-checker sees it as field.

### Pattern 3: Score Validation via Model Validator

**What:** Use `@model_validator(mode="after")` for cross-field validation

**When:** When overall score must equal sum/avg of component scores

**Example:** See `IELTSScores.check_overall_is_consistent()` in existing code.

### Pattern 4: Barrel File Exports

**What:** Single `__init__.py` re-exports all public types

**When:** Always

**Example:** `languages/certificates/__init__.py` imports from submodules and re-exports.

## Anti-Patterns to Avoid

### Anti-Pattern 1: Circular Imports via CEFRLevel Import

**What:** Importing `CEFRLevel` from `levels.py` inside exam modules

**Why:** Can cause circular import issues; existing pattern uses `CEFRLiteral` from `base.py`

**Instead:** Import `CEFRLiteral` from `certificates/base.py` or define return type as string literal.

### Anti-Pattern 2: Computed Field Without @property

**What:** Using `@computed_field` without `@property` decorator

**Why:** Pydantic v2 requires both for computed fields to work correctly

**Instead:**

```python
@computed_field
@property  # Required!
def CEFRLevel(self) -> CEFRLiteral:
    ...
```

### Anti-Pattern 3: Using default_factory with ...

**What:** Writing `default_factory=lambda: ...` or `default_factory=...` with `...`

**Why:** In Pydantic v2, `...` means required; this causes validation errors

**Instead:** Simply omit the default for required fields, or use `= None` for optional

## Scalability Considerations

| Concern | At 10 exams | At 50 exams | At 100 exams |
|---------|-------------|-------------|--------------|
| Module count | ~15 files | ~60 files | ~120 files |
| Import time | <50ms | <100ms | <200ms |
| Type checking | Fast | Fast | Consider split packages |

**Recommendation:** Current structure scales well. Each language gets its own directory, keeping module sizes manageable.

## New Certificate Implementation Guide

### For HSK (Chinese)

1. Create `src/pydanticcv/languages/certificates/zho/base.py`:
   - Define `ChineseLanguageProficiencyCertificate` extending `LanguageProficiencyCertificate`
   - Set `CertifiedLanguage` ClassVar

2. Create `src/pydanticcv/languages/certificates/zho/hsk.py`:
   - Define `HSKLevel` (1-6), `HSKScores`
   - Implement CEFR mapping: HSK5→C1, HSK4→B2, HSK3→B1, HSK1-2→A2
   - Add to `zho/__init__.py`

3. Update `languages/certificates/__init__.py` to export HSK

### For DELE (Spanish)

1. Same pattern: `src/pydanticcv/languages/certificates/esp/base.py`
2. Exam models: `dele.py` with levels A1-C2
3. CEFR direct mapping (DELE level = CEFR level)

### For CELPIP (Canadian English)

1. Extend `EnglishLanguageProficiencyCertificate` 
2. Model: CELPIP-General or CELPIP-LS (listening/speaking only)
3. CEFR mapping per CELPIP official tables

### For Professional Certifications

The `SkillCertificate` base already exists in `skills/certificates/base.py`. To add:

1. Extend `SkillCertificate` for specific certifications (optional)
2. Or use `SkillCertificate` directly with fields:
   - `CertificateName`: "AWS Solutions Architect"
   - `IssuingOrganisation`: "Amazon Web Services"
   - `DateObtained`: PastDate
   - `ExpiryDate`: Optional date
   - `Link`: Optional verification URL

3. Add to CV via `Skills` field (already accepts `Skill` with certificates)

### For Social/Profile Links

Already implemented in `cv/personal_info.py`:
- `ContactInfo` has `LinkedIn`, `GitHub`, `Portfolio` URLs
- No new module needed unless adding more social platforms

## Sources

- Existing codebase analysis: `src/pydanticcv/languages/certificates/eng/ielts.py`
- Existing base patterns: `base.py`, `eng/base.py`, `deu/base.py`
- CV composition: `cv/cv.py`
- Skills certificates: `skills/certificates/base.py`

---

*Research for roadmap: 2026-04-03*