# Requirements

## v1 Requirements

### New Language Certificates

- [x] **LANG-01**: Add HSK Chinese exam model with score validation and CEFR mapping
- [x] **LANG-02**: Add CELPIP Canadian English exam model with score validation and CEFR mapping
- [x] **LANG-03**: Add TEF French-Canadian exam model with score validation and CEFR mapping

### Certifications CV Section

- [x] **CERT-01**: Create `SkillCertificate` model with name, issuer, date, verification URL
- [x] **CERT-02**: Add `SkillCertificate` list field to CV model
- [x] **CERT-03**: Add issuer validation with curated allowlist (AWS, Azure, GCP, PMI, ISC2, CompTIA)

### Social/Profile Links CV Section

- [x] **SOCIAL-01**: Expand existing social links in PersonalInfo to support all major platforms
- [x] **SOCIAL-02**: Add platform auto-detection from URL patterns
- [x] **SOCIAL-03**: Support ORCID, Google Scholar, ResearchGate, Behance, Dribbble

## v2 Requirements (Deferred)

- Cambridge English exam (CPE, CAE) — lower priority than HSK/CELPIP
- DELE Spanish — similar pattern to HSK, can add later
- Certification expiration tracking — future enhancement
- Custom URL validators per platform — future enhancement

## Out of Scope

- Web UI for CV editing — library only, no UI
- PDF/JSON export — data models only
- Resume parsing from documents — complex, out of scope
- Multi-language CV support — single language for now

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| LANG-01 | Phase 1 | ✓ Complete |
| LANG-02 | Phase 2 | ✓ Complete |
| LANG-03 | Phase 2 | ✓ Complete |
| CERT-01 | Phase 3 | ✓ Complete |
| CERT-02 | Phase 3 | ✓ Complete |
| CERT-03 | Phase 3 | ✓ Complete |
| SOCIAL-01 | Phase 4 | ✓ Complete |
| SOCIAL-02 | Phase 4 | ✓ Complete |
| SOCIAL-03 | Phase 4 | ✓ Complete |

---

*Traceability updated: 2026-04-03*