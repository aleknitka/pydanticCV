---
phase: 04-social-links
plan: 01
subsystem: cv
tags: [pydantic, validation, social-links, platform-detection]

# Dependency graph
requires:
  - phase: 03-professional-certifications
    provides: CV model with skills field
provides:
  - SocialPlatform StrEnum with 10 platform types
  - ProfileLink model with URL validation and auto-detection
  - Updated ContactInfo with 7 new platform fields + ProfileLinks list
  - Public export of SocialPlatform and ProfileLink from pydanticcv.cv
affects: [contact-info, social-profiles]

# Tech tracking
tech-stack:
  added: []
  patterns: [StrEnum for platform types, computed_field for auto-detection, BeforeValidator for https enforcement]

key-files:
  created:
    - tests/cv/test_personal_info.py
  modified:
    - src/pydanticcv/cv/personal_info.py
    - src/pydanticcv/cv/__init__.py

key-decisions:
  - "Used StrEnum for SocialPlatform - clean type-safe enum matching Python 3.11+"
  - "Applied @computed_field with @property for platform auto-detection"
  - "Added BeforeValidator to enforce HTTPS scheme on ProfileLink URLs"
  - "Added ProfileLinks list for additional/unspecified profile URLs"

patterns-established:
  - "URL pattern matching for platform detection via regex"
  - "HTTPS enforcement via BeforeValidator on AnyUrl fields"
  - "Backward-compatible field expansion on existing models"

requirements-completed: []

# Metrics
duration: 2min
completed: 2026-04-03
---

# Phase 4: Social/Profile Links Summary

**ProfileLink model with automatic platform detection from URL patterns integrated into ContactInfo**

## Performance

- **Duration:** 2 min
- **Tasks:** 3/3 complete
- **Commits:** 2 (implementation + tests)

## What Was Built

### 1. SocialPlatform StrEnum
Ten platform types with case-insensitive string values:
- LinkedIn, GitHub, Twitter, Website, ORCID, GoogleScholar, ResearchGate, Behance, Dribbble, Custom

### 2. ProfileLink Model
- `url: AnyUrl` - validated to require HTTPS scheme
- `platform: SocialPlatform` - automatically detected via regex pattern matching
- `label: Optional[str]` - user-provided label for the link

Platform detection patterns:
| Platform | Regex Pattern |
| -------- | ------------- |
| LinkedIn | `linkedin.com/(in\|pub)/` |
| GitHub | `github.com/` |
| Twitter/X | `(twitter\.com\|x\.com)/` |
| ORCID | `orcid.org/` |
| Google Scholar | `scholar.google.com/` |
| ResearchGate | `researchgate.net/` |
| Behance | `behance.net/` |
| Dribbble | `dribbble.com/` |

### 3. Updated ContactInfo
New fields added:
- Twitter, ORCID, GoogleScholar, ResearchGate, Behance, Dribbble (Optional[AnyUrl])
- ProfileLinks: list[ProfileLink] for additional profile URLs

All existing fields (Email, Phone, Website, LinkedIn, GitHub, OtherUrls) remain for backward compatibility.

## Verification

- All 20 new tests pass
- 52 existing CV tests pass (backward compatibility confirmed)
- Import verification: `from pydanticcv.cv.personal_info import ProfileLink, SocialPlatform` works
- Public API exports added to `pydanticcv.cv.__init__.py`

## Deviations from Plan

None - plan executed exactly as written.

## Known Stubs

None - all features fully implemented with data sources wired.