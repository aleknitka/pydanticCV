# Feature Landscape

**Domain:** CV Schema Library — Language Certificates, Certifications, Social Links
**Researched:** 2026-04-03
**Confidence:** MEDIUM (ecosystem well-established; specific exam score ranges need verification)

## Executive Summary

This research covers three feature areas for the pydanticCV library:

1. **Language certificates** — Beyond existing IELTS, TOEFL, DELF, Goethe, TCF — HSK (Chinese), CELPIP (Canadian), Cambridge, TEF/TEFaCM
2. **Professional certifications** — Cloud (AWS/Azure/GCP), project management, security, DevOps
3. **Social profile links** — LinkedIn, GitHub, portfolio sites, validated with platform detection

The CV schema ecosystem (notably JSON Resume) provides clear patterns for all three. Existing architecture with `LanguageProficiencyCertificate` base class and computed CEFR levels is well-suited to extensions.

---

## Table Stakes

Features users expect. Missing = library feels incomplete.

### Language Certificate Exams

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| **HSK (Chinese)** | Major global language test, required for Chinese university/work visas | Medium | 6 levels (new HSK 3.0), CEFR mapping exists |
| **CELPIP (Canadian)** | Required for Canadian immigration (Express Entry), now accepted in Australia | Medium | 4 skills, CLB/CEFR conversion tables needed |
| **Cambridge (CPE/CAE/FCE)** | Widely accepted in UK/Europe, no expiration | Low | Direct CEFR level from exam name |
| **TEF/TEFaCM (French)** | Required for Canadian immigration (Quebec) | Medium | Different from TCF, separate scoring |
| **Cambridge OET** | Healthcare-specific English test | Low | Niche but established |

### Professional Certifications Section

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| **Certifications list** | Standard CV section for IT/professional roles | Low | Name, issuer, date, optional URL |
| **Certification categories** | Cloud, Security, Project Mgmt, etc. | Medium | Enum or string with validation |
| **Expiry tracking** | Many certifications expire | Low | Optional expiry date field |

### Social/Profile Links Section

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| **Profile links array** | Standard in modern CVs | Low | Network name + URL |
| **URL validation** | Must be valid URLs | Low | AnyUrl validator |
| **Common platforms** | LinkedIn, GitHub, personal site | Low | Platform detection as computed field |

---

## Differentiators

Features that set the library apart. Not expected, but valued.

### Language Certificates

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| **CEFR level computation** | Unique among CV libraries — compute CEFR from raw scores | Medium | Already implemented for existing certs, extend to new |
| **Score validation** | Reject invalid score combinations (e.g., IELTS speaking 9.5) | Medium | Each exam has specific ranges |
| **Score conversion** | Convert between legacy/new TOEFL formats | Medium | Already exists for TOEFL |

### Professional Certifications

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| **Issuer catalog validation** | Validate against known issuers (AWS, Azure, etc.) | Medium | Curated list, not enum (too many) |
| **Credential URL parsing** | Extract credential ID from verification URL | High | Complex, variable formats |
| **Expiry notifications** | Warn about expiring certifications | Low | Date comparison at serialization time |

### Social Links

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| **Platform auto-detection** | Detect LinkedIn/GitHub from URL, validate username format | Medium | Regex patterns per platform |
| **QR code generation** | Generate QR for personal website | High | Separate library dependency |
| **Link preview metadata** | Fetch OpenGraph data for URLs | High | Network call, caching concerns |

---

## Anti-Features

Features to explicitly NOT build.

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| **Credential verification** | Would require network calls, complex async handling | Document as limitation, let consumer handle |
| **Automated scraping** | Legal/ethical concerns, rate limits | Accept credential URLs as input only |
| **Certification expiry reminders** | Not a schema concern — consumer can add via post-init hooks | Document pattern for extension |
| **Link click tracking** | Privacy concerns, not a schema concern | Out of scope |
| **Multi-language CV templates** | Schema-only library, UI out of scope | JSON Resume handles this ecosystem |

---

## Feature Dependencies

```
Language Certificate Exam Model
  └── Base model (LanguageProficiencyCertificate)
      ├── PastDate (DateTaken)
      ├── AnyUrl (Link)
      └── Computed CEFR level

Professional Certification
  └── Simple model (no base class needed)
      ├── issuer: str
      ├── date: PastDate  
      └── url: Optional[AnyUrl]

Social Profile Link
  └── Simple model
      ├── network: Literal[known platforms]
      ├── url: AnyUrl
      └── username: Optional[str]
```

### Dependency Notes

- **HSK**: Requires CEFR mapping (new HSK 3.0 differs from old 1-6 levels)
- **CELPIP**: Requires CLB-to-CEF conversion table (CLB 4-12 maps to A1-C2)
- **TEF**: Similar structure to TCF but different scoring (0-900 scale)
- **Profile links**: Should integrate with existing `basics` section in CV model

---

## MVP Recommendation

**Phase 1 — Language Certificates:**
Prioritize:
1. **HSK** — High demand, well-documented CEFR mapping
2. **CELPIP** — Canadian immigration driver, clear CLB conversion
3. **TEF/TEFaCM** — Quebec immigration requirement

Defer:
- Cambridge (just labels, no scores to validate)
- OET (niche healthcare, complex speaking rubric)

**Phase 2 — Professional Certifications:**
Prioritize:
1. Basic certifications model (name, issuer, date, url)
2. Issuer allowlist (AWS, Azure, GCP, PMI, ISC2, CompTIA)

Defer:
- Credential parsing (too variable)
- Expiry tracking (validation only, no notifications)

**Phase 3 — Social Profile Links:**
Prioritize:
1. Profile model with network + url + username
2. Platform detection from URL
3. Common platforms: LinkedIn, GitHub, Twitter, personal website

Defer:
- QR code generation (out of scope)
- OpenGraph metadata (network calls)

---

## Sources

- **JSON Resume Schema** — Community standard, validates feature expectations
- **CELPIP official** — Test structure and CLB conversion requirements
- **HSK 3.0** — New exam format (2026), CEFR mapping documentation
- **Canada Express Entry** — Language test requirements for immigration
- **Goethe, DELF, DELE** — Existing implementations in codebase confirm pattern

---

## Research Gaps

- **TEF exact scoring**: TEF has 6 sections (reading, listening, writing, speaking, vocabulary, structure) — need official score ranges
- **HSK 3.0 CEFR mapping**: Preliminary mapping exists but not officially published by Hanban/Chinese Testing International
- **CELPIP vs CELPIP-LS distinction**: General test vs Listening/Speaking only — both accepted for immigration