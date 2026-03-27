# CV Top-Level Structure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `CV` top-level Pydantic v2 model with a `PersonalInfo` section covering name, contact details, address, and photo.

**Architecture:** New `src/pydanticcv/cv/` subpackage mirroring the `languages/` structure. `CVAddress` is added to the existing `utils/locations.py`. All models follow project conventions (PascalCase fields, Google docstrings, `__all__`, module docstrings).

**Tech Stack:** Python ≥ 3.11, Pydantic v2, pydantic-extra-types (phone + existing extras), pytest + polyfactory.

---

## File Map

| Action | Path | Responsibility |
|--------|------|----------------|
| Modify | `pyproject.toml` | Add `phonenumbers` via `pydantic-extra-types[phone]` extra |
| Modify | `src/pydanticcv/utils/locations.py` | Add `CVAddress` model |
| Create | `src/pydanticcv/cv/__init__.py` | Re-export `CV`, `PersonalInfo`, `Name`, `ContactInfo` |
| Create | `src/pydanticcv/cv/personal_info.py` | `Name`, `ContactInfo`, `PersonalInfo` models |
| Create | `src/pydanticcv/cv/cv.py` | `CV` top-level model |
| Create | `tests/test_cv.py` | All tests for the new models |

---

## Task 1: Add `phonenumbers` dependency

**Files:**
- Modify: `pyproject.toml`

- [ ] **Step 1: Update the dependency in `pyproject.toml`**

Change the `pydantic-extra-types` line in the `[project]` `dependencies` list from:
```toml
"pydantic-extra-types>=2.11.1",
```
to:
```toml
"pydantic-extra-types[phone]>=2.11.1",
```

- [ ] **Step 2: Sync the lockfile**

```bash
uv sync
```
Expected: resolves successfully, `phonenumbers` appears in the environment.

- [ ] **Step 3: Verify the import works**

```bash
uv run python -c "from pydantic_extra_types.phone_numbers import PhoneNumber; print('OK')"
```
Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add pyproject.toml uv.lock
git commit -m "chore: add phonenumbers via pydantic-extra-types[phone] extra"
```

---

## Task 2: Add `CVAddress` to `utils/locations.py`

**Files:**
- Modify: `src/pydanticcv/utils/locations.py`
- Test: `tests/test_cv.py` (create file with first test class)

- [ ] **Step 1: Write the failing test**

Create `tests/test_cv.py`:

```python
"""Tests for pydanticcv.cv models.

Covers Name, ContactInfo, PersonalInfo, CVAddress, and CV.
"""

import pytest
from pydantic import ValidationError

from pydanticcv.utils.locations import CVAddress, Country


class TestCVAddress:
    """Tests for the CVAddress model."""

    def test_all_fields_none_by_default(self) -> None:
        addr = CVAddress()
        assert addr.City is None
        assert addr.Country is None

    def test_accepts_city_only(self) -> None:
        addr = CVAddress(City="London")
        assert addr.City == "London"
        assert addr.Country is None

    def test_accepts_country_only(self) -> None:
        country = Country(name="United Kingdom", iso="GBR")
        addr = CVAddress(Country=country)
        assert addr.Country.iso == "GBR"
        assert addr.City is None

    def test_accepts_both_fields(self) -> None:
        country = Country(name="France", iso="FRA")
        addr = CVAddress(City="Paris", Country=country)
        assert addr.City == "Paris"
        assert addr.Country.name == "France"
```

- [ ] **Step 2: Run the test to verify it fails**

```bash
uv run pytest tests/test_cv.py::TestCVAddress -v
```
Expected: `ImportError` — `CVAddress` not yet defined.

- [ ] **Step 3: Implement `CVAddress` in `utils/locations.py`**

The full updated file (append `CVAddress`; also add `Optional` import and expand `__all__`):

```python
"""Utilities for anything to do with locations.

Contents:
    Country: Pydantic model for a named country with ISO 3166-1 alpha-3 code.
    Location: Pydantic model for a geographic coordinate pair.
    CVAddress: Pydantic model for a human-readable CV address (city + country).
"""

from typing import Optional

from pydantic import BaseModel
from pydantic_extra_types.country import CountryAlpha3
from pydantic_extra_types.coordinate import (
    Latitude as _Latitude,
    Longitude as _Longitude,
)

__all__ = ["Country", "Location", "CVAddress"]


class Country(BaseModel):
    """A named country with its ISO 3166-1 alpha-3 code.

    Attributes:
        name: Human-readable country name (e.g. ``"United Kingdom"``).
        iso: ISO 3166-1 alpha-3 country code (e.g. ``"GBR"``).
    """

    name: str
    iso: CountryAlpha3


class Location(BaseModel):
    """A geographic coordinate pair.

    Attributes:
        Latitude: WGS-84 latitude in decimal degrees.
        Longitude: WGS-84 longitude in decimal degrees.
    """

    Latitude: _Latitude
    Longitude: _Longitude


class CVAddress(BaseModel):
    """A human-readable address for use in a CV.

    Attributes:
        City: City or town name (e.g. ``"London"``).
        Country: Country, including ISO 3166-1 alpha-3 code.
    """

    City: Optional[str] = None
    Country: Optional[Country] = None
```

- [ ] **Step 4: Run the test to verify it passes**

```bash
uv run pytest tests/test_cv.py::TestCVAddress -v
```
Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
git add src/pydanticcv/utils/locations.py tests/test_cv.py
git commit -m "feat: add CVAddress model to utils/locations"
```

---

## Task 3: Implement `Name` and `ContactInfo` in `cv/personal_info.py`

**Files:**
- Create: `src/pydanticcv/cv/__init__.py` (empty placeholder for now)
- Create: `src/pydanticcv/cv/personal_info.py`
- Modify: `tests/test_cv.py`

- [ ] **Step 1: Create the empty package `__init__.py`**

Create `src/pydanticcv/cv/__init__.py` with a single line:
```python
"""CV schema subpackage."""
```

- [ ] **Step 2: Add failing tests for `Name` and `ContactInfo`**

Append to `tests/test_cv.py`:

```python
from pydanticcv.cv.personal_info import Name, ContactInfo


class TestName:
    """Tests for the Name model."""

    def test_requires_family_name(self) -> None:
        with pytest.raises(ValidationError):
            Name()

    def test_family_name_only(self) -> None:
        name = Name(FamilyName="Smith")
        assert name.FamilyName == "Smith"
        assert name.Title is None
        assert name.GivenNames is None
        assert name.MiddleName is None
        assert name.PreferredName is None

    def test_all_fields(self) -> None:
        name = Name(
            Title="Dr.",
            FamilyName="Smith",
            GivenNames=["Alice", "Jane"],
            MiddleName="Marie",
            PreferredName="Ali",
        )
        assert name.Title == "Dr."
        assert name.GivenNames == ["Alice", "Jane"]
        assert name.MiddleName == "Marie"
        assert name.PreferredName == "Ali"


class TestContactInfo:
    """Tests for the ContactInfo model."""

    def test_all_fields_optional(self) -> None:
        contact = ContactInfo()
        assert contact.Email is None
        assert contact.Phone is None
        assert contact.Website is None
        assert contact.LinkedIn is None
        assert contact.GitHub is None
        assert contact.OtherUrls == []

    def test_valid_email(self) -> None:
        contact = ContactInfo(Email="alice@example.com")
        assert contact.Email == "alice@example.com"

    def test_invalid_email_rejected(self) -> None:
        with pytest.raises(ValidationError):
            ContactInfo(Email="not-an-email")

    def test_valid_phone(self) -> None:
        contact = ContactInfo(Phone="+442071234567")
        assert contact.Phone is not None

    def test_invalid_phone_rejected(self) -> None:
        with pytest.raises(ValidationError):
            ContactInfo(Phone="not-a-phone")

    def test_valid_urls(self) -> None:
        contact = ContactInfo(
            Website="https://alice.dev",
            LinkedIn="https://linkedin.com/in/alice",
            GitHub="https://github.com/alice",
            OtherUrls=["https://example.com"],
        )
        assert contact.GitHub is not None
        assert len(contact.OtherUrls) == 1
```

- [ ] **Step 3: Run the tests to verify they fail**

```bash
uv run pytest tests/test_cv.py::TestName tests/test_cv.py::TestContactInfo -v
```
Expected: `ImportError` — module not yet created.

- [ ] **Step 4: Create `src/pydanticcv/cv/personal_info.py`**

```python
"""Personal information models for a CV.

Contents:
    Name: Structured name with title, given names, family name, and preferred name.
    ContactInfo: Contact details including email, phone, URLs, and social profiles.
    PersonalInfo: Top-level personal information section of a CV.
"""

__all__ = ["Name", "ContactInfo", "PersonalInfo"]

from typing import Optional
from pydantic import AnyUrl, BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

from pydanticcv.utils.locations import CVAddress


class Name(BaseModel):
    """A structured personal name.

    Attributes:
        Title: Honorific or title (e.g. ``"Dr."``, ``"Prof."``).
        FamilyName: Family name / surname. Required.
        GivenNames: Ordered list of given (first) names.
        MiddleName: Middle name, if any.
        PreferredName: Preferred or chosen name used in everyday contexts.
    """

    Title: Optional[str] = None
    FamilyName: str
    GivenNames: Optional[list[str]] = None
    MiddleName: Optional[str] = None
    PreferredName: Optional[str] = None


class ContactInfo(BaseModel):
    """Contact details for a CV.

    Attributes:
        Email: Primary email address.
        Phone: Phone number in E.164 format (e.g. ``"+442071234567"``).
        Website: Personal website or portfolio URL.
        LinkedIn: LinkedIn profile URL.
        GitHub: GitHub profile URL.
        OtherUrls: Additional URLs (e.g. personal blog, portfolio).
    """

    Email: Optional[EmailStr] = None
    Phone: Optional[PhoneNumber] = None
    Website: Optional[AnyUrl] = None
    LinkedIn: Optional[AnyUrl] = None
    GitHub: Optional[AnyUrl] = None
    OtherUrls: list[AnyUrl] = []


class PersonalInfo(BaseModel):
    """Personal information section of a CV.

    Attributes:
        Name: Structured name. Required.
        Contact: Contact details.
        Address: Home or mailing address.
        Photo: URL to a profile photo or headshot.
    """

    Name: Name
    Contact: Optional[ContactInfo] = None
    Address: Optional[CVAddress] = None
    Photo: Optional[AnyUrl] = None
```

- [ ] **Step 5: Run the tests to verify they pass**

```bash
uv run pytest tests/test_cv.py::TestName tests/test_cv.py::TestContactInfo -v
```
Expected: all passed.

- [ ] **Step 6: Commit**

```bash
git add src/pydanticcv/cv/__init__.py src/pydanticcv/cv/personal_info.py tests/test_cv.py
git commit -m "feat: add Name, ContactInfo, PersonalInfo models"
```

---

## Task 4: Implement `PersonalInfo` tests and `CV` model

**Files:**
- Create: `src/pydanticcv/cv/cv.py`
- Modify: `tests/test_cv.py`

- [ ] **Step 1: Add failing tests for `PersonalInfo` and `CV`**

Append to `tests/test_cv.py`:

```python
from pydanticcv.cv.personal_info import PersonalInfo
from pydanticcv.cv.cv import CV


class TestPersonalInfo:
    """Tests for the PersonalInfo model."""

    def test_requires_name(self) -> None:
        with pytest.raises(ValidationError):
            PersonalInfo()

    def test_name_only(self) -> None:
        pi = PersonalInfo(Name=Name(FamilyName="Smith"))
        assert pi.Name.FamilyName == "Smith"
        assert pi.Contact is None
        assert pi.Address is None
        assert pi.Photo is None

    def test_all_fields(self) -> None:
        pi = PersonalInfo(
            Name=Name(FamilyName="Smith", GivenNames=["Alice"]),
            Contact=ContactInfo(Email="alice@example.com"),
            Address=CVAddress(City="London"),
            Photo="https://example.com/photo.jpg",
        )
        assert pi.Name.GivenNames == ["Alice"]
        assert pi.Contact.Email == "alice@example.com"
        assert pi.Address.City == "London"
        assert pi.Photo is not None


class TestCV:
    """Tests for the top-level CV model."""

    def test_requires_personal_info(self) -> None:
        with pytest.raises(ValidationError):
            CV()

    def test_minimal_cv(self) -> None:
        cv = CV(PersonalInfo=PersonalInfo(Name=Name(FamilyName="Smith")))
        assert cv.PersonalInfo.Name.FamilyName == "Smith"

    def test_round_trip_json(self) -> None:
        cv = CV(
            PersonalInfo=PersonalInfo(
                Name=Name(
                    Title="Dr.",
                    FamilyName="Smith",
                    GivenNames=["Alice"],
                ),
                Contact=ContactInfo(Email="alice@example.com"),
                Address=CVAddress(City="London"),
            )
        )
        json_str = cv.model_dump_json()
        cv2 = CV.model_validate_json(json_str)
        assert cv2.PersonalInfo.Name.FamilyName == "Smith"
        assert cv2.PersonalInfo.Contact.Email == "alice@example.com"
```

- [ ] **Step 2: Run to verify they fail**

```bash
uv run pytest tests/test_cv.py::TestPersonalInfo tests/test_cv.py::TestCV -v
```
Expected: `ImportError` — `cv.py` not yet created.

- [ ] **Step 3: Create `src/pydanticcv/cv/cv.py`**

```python
"""Top-level CV model.

Contents:
    CV: Root Pydantic model representing a complete CV/resume.
"""

__all__ = ["CV"]

from pydantic import BaseModel
from pydanticcv.cv.personal_info import PersonalInfo


class CV(BaseModel):
    """A complete CV/resume.

    Attributes:
        PersonalInfo: Personal information section. Required.
    """

    PersonalInfo: PersonalInfo
```

- [ ] **Step 4: Run to verify they pass**

```bash
uv run pytest tests/test_cv.py::TestPersonalInfo tests/test_cv.py::TestCV -v
```
Expected: all passed.

- [ ] **Step 5: Commit**

```bash
git add src/pydanticcv/cv/cv.py tests/test_cv.py
git commit -m "feat: add CV top-level model"
```

---

## Task 5: Wire up public API in `cv/__init__.py`

**Files:**
- Modify: `src/pydanticcv/cv/__init__.py`
- Modify: `tests/test_cv.py`

- [ ] **Step 1: Add failing import test**

Append to `tests/test_cv.py`:

```python
class TestPublicAPI:
    """Tests that the public API re-exports are correct."""

    def test_imports_from_cv_package(self) -> None:
        from pydanticcv.cv import CV, PersonalInfo, Name, ContactInfo  # noqa: F401
        assert CV is not None
        assert PersonalInfo is not None
        assert Name is not None
        assert ContactInfo is not None
```

- [ ] **Step 2: Run to verify it fails**

```bash
uv run pytest tests/test_cv.py::TestPublicAPI -v
```
Expected: `ImportError` — `__init__.py` doesn't re-export yet.

- [ ] **Step 3: Update `src/pydanticcv/cv/__init__.py`**

```python
"""CV schema subpackage.

Provides the top-level CV model and all supporting personal information models.

Contents:
    CV: Root model for a complete CV/resume.
    PersonalInfo: Personal information section.
    Name: Structured name model.
    ContactInfo: Contact details model.
"""

__all__ = ["CV", "PersonalInfo", "Name", "ContactInfo"]

from pydanticcv.cv.cv import CV
from pydanticcv.cv.personal_info import PersonalInfo, Name, ContactInfo
```

- [ ] **Step 4: Run the full test suite**

```bash
uv run pytest -v
```
Expected: all tests pass, including the full existing suite.

- [ ] **Step 5: Commit**

```bash
git add src/pydanticcv/cv/__init__.py tests/test_cv.py
git commit -m "feat: wire up pydanticcv.cv public API"
```
