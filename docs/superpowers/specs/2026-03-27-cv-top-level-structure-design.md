# CV Top-Level Structure — Design Spec

**Date:** 2026-03-27
**Scope:** First iteration — personal info section only. Other CV sections (work experience, education, skills, etc.) are out of scope and will be added incrementally.

---

## Goals

Add a top-level `CV` Pydantic v2 model as a general-purpose schema for CV/resume data: storage/serialisation, validation of submitted CVs, and programmatic generation.

---

## File Layout

```
src/pydanticcv/
├── utils/
│   ├── date.py               # unchanged
│   └── locations.py          # existing Country + Location; add CVAddress
├── cv/
│   ├── __init__.py           # re-exports: CV, PersonalInfo, Name, ContactInfo
│   ├── cv.py                 # CV top-level model
│   └── personal_info.py      # Name, ContactInfo, PersonalInfo
└── languages/                # unchanged
```

---

## Models

### `CVAddress` — `utils/locations.py`

New model appended to the existing file. Reuses the existing `Country` model.

```python
class CVAddress(BaseModel):
    City: Optional[str] = None
    Country: Optional[Country] = None
```

### `Name` — `cv/personal_info.py`

```python
class Name(BaseModel):
    Title: Optional[str] = None          # e.g. "Dr.", "Prof.", "Mr."
    FamilyName: str                      # only required field in the whole CV
    GivenNames: Optional[list[str]] = None
    MiddleName: Optional[str] = None
    PreferredName: Optional[str] = None
```

### `ContactInfo` — `cv/personal_info.py`

Uses `EmailStr` from Pydantic and `PhoneNumber` from `pydantic_extra_types.phone_numbers`. The `phone` extra of `pydantic-extra-types` must be added to `pyproject.toml` (it pulls in `phonenumbers`): `pydantic-extra-types[phone]>=2.11.1`.

```python
class ContactInfo(BaseModel):
    Email: Optional[EmailStr] = None
    Phone: Optional[PhoneNumber] = None
    Website: Optional[AnyUrl] = None
    LinkedIn: Optional[AnyUrl] = None
    GitHub: Optional[AnyUrl] = None
    OtherUrls: list[AnyUrl] = []
```

### `PersonalInfo` — `cv/personal_info.py`

```python
class PersonalInfo(BaseModel):
    Name: Name                           # required (carries the only required field)
    Contact: Optional[ContactInfo] = None
    Address: Optional[CVAddress] = None
    Photo: Optional[AnyUrl] = None
```

### `CV` — `cv/cv.py`

```python
class CV(BaseModel):
    PersonalInfo: PersonalInfo           # required
```

---

## Public API

`from pydanticcv.cv import CV, PersonalInfo, Name, ContactInfo`

`cv/__init__.py` re-exports all four models. `pydanticcv/__init__.py` remains empty (unchanged).

---

## Conventions followed

- Google-style docstrings with `Attributes:` sections on all models.
- Every module declares `__all__`.
- Every file starts with a module-level docstring listing its contents.
- PascalCase for model names and fields.
- `Optional[X]` always paired with `= None`.
- No `default_factory` on required fields.

---

## Out of scope (future iterations)

Work experience, education, skills, projects, publications, certifications, awards, volunteer experience, references.
