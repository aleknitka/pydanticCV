# Requirements

## v1 Requirements

### New Language Certificates

- [ ] **LANG-01**: Add HSK Chinese exam model with score validation and CEFR mapping
- [ ] **LANG-02**: Add CELPIP Canadian English exam model with score validation and CEFR mapping
- [ ] **LANG-03**: Add TEF French-Canadian exam model with score validation and CEFR mapping

### Certifications CV Section

- [ ] **CERT-01**: Create `SkillCertificate` model with name, issuer, date, verification URL
- [ ] **CERT-02**: Add `SkillCertificate` list field to CV model
- [ ] **CERT-03**: Add issuer validation with curated allowlist (AWS, Azure, GCP, PMI, ISC2, CompTIA)

### Social/Profile Links CV Section

- [ ] **SOCIAL-01**: Expand existing social links in PersonalInfo to support all major platforms
- [ ] **SOCIAL-02**: Add platform auto-detection from URL patterns
- [ ] **SOCIAL-03**: Support ORCID, Google Scholar, ResearchGate, Behance, Dribbble

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
| LANG-01 | Phase 1 | pending |
| LANG-02 | Phase 2 | pending |
| LANG-03 | Phase 2 | pending |
| CERT-01 | Phase 3 | pending |
| CERT-02 | Phase 3 | pending |
| CERT-03 | Phase 3 | pending |
| SOCIAL-01 | Phase 4 | pending |
| SOCIAL-02 | Phase 4 | pending |
| SOCIAL-03 | Phase 4 | pending |

---

*Traceability updated: 2026-04-03*