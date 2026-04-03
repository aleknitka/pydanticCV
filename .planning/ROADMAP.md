# Roadmap

## Phases

- [x] **Phase 1: Chinese Language Certificates (HSK)** - HSK exam model with score validation and CEFR mapping
- [ ] **Phase 2: Additional Language Certificates (CELPIP, TEF)** - CELPIP and TEF exam models with CEFR computation
- [ ] **Phase 3: Professional Certifications** - SkillCertificate model with issuer validation
- [ ] **Phase 4: Social/Profile Links** - Expand social links with platform auto-detection

---

## Phase Details

### Phase 1: Chinese Language Certificates (HSK)

**Goal**: Users can create HSK Chinese exam records with validated scores and computed CEFR levels

**Depends on**: Nothing (first phase)

**Requirements**: LANG-01

**Success Criteria** (what must be TRUE):
  1. User can create HSK model with valid HSK level (1-6) and section scores
  2. HSK section scores are validated (listening, reading, writing within valid ranges)
  3. CEFR level is computed from HSK level using documented mapping (HSK5→C1, HSK4→B2, HSK3→B1, HSK1-2→A2)
  4. Invalid HSK score combinations are rejected with clear validation errors

**Plans**: TBD

---

### Phase 2: Additional Language Certificates (CELPIP, TEF)

**Goal**: Users can create CELPIP (Canadian) and TEF (French-Canadian) exam records with validated scores and CEFR mapping

**Depends on**: Phase 1

**Requirements**: LANG-02, LANG-03

**Success Criteria** (what must be TRUE):
  1. User can create CELPIP model with CLB score (4-12) and computed CEFR level
  2. User can create TEF model with 6 section scores and computed CEFR level
  3. Invalid CELPIP CLB scores (outside 4-12) are rejected
  4. Invalid TEF section scores are rejected with validation errors
  5. CEFR levels are correctly computed for both exam types

**Plans**: TBD

---

### Phase 3: Professional Certifications

**Goal**: Users can add professional certifications to their CV with validated issuer information

**Depends on**: Phase 2

**Requirements**: CERT-01, CERT-02, CERT-03

**Success Criteria** (what must be TRUE):
  1. User can create SkillCertificate model with name, issuer, date, verification URL
  2. CV model includes a list field for SkillCertificate entries
  3. Issuer field validates against curated allowlist (AWS, Azure, GCP, PMI, ISC2, CompTIA)
  4. Invalid issuers outside the allowlist are rejected with clear error message

**Plans**: TBD

---

### Phase 4: Social/Profile Links

**Goal**: Users can add comprehensive social and professional profile links with platform auto-detection

**Depends on**: Phase 3

**Requirements**: SOCIAL-01, SOCIAL-02, SOCIAL-03

**Success Criteria** (what must be TRUE):
  1. User can add profile links to all major platforms (LinkedIn, GitHub, Twitter/X, personal website)
  2. Platform is auto-detected from URL patterns (regex matching)
  3. User can add academic/professional profiles (ORCID, Google Scholar, ResearchGate, Behance, Dribbble)
  4. Invalid URLs are rejected with scheme validation (https required)

**Plans**: TBD

---

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Chinese Language (HSK) | 1/1 | Complete | 2026-04-03 |
| 2. Additional Languages (CELPIP, TEF) | 0/1 | Not started | - |
| 3. Professional Certifications | 0/1 | Not started | - |
| 4. Social/Profile Links | 0/1 | Not started | - |

---

*Roadmap created: 2026-04-03*
*Granularity: standard*