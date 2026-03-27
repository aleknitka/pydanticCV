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


from pydanticcv.cv.personal_info import Name, ContactInfo, PersonalInfo
from pydanticcv.cv.cv import CV


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


class TestPublicAPI:
    """Tests that the public API re-exports are correct."""

    def test_imports_from_cv_package(self) -> None:
        from pydanticcv.cv import CV, PersonalInfo, Name, ContactInfo  # noqa: F401
        assert CV is not None
        assert PersonalInfo is not None
        assert Name is not None
        assert ContactInfo is not None
