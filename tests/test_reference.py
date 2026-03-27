"""Tests for pydanticcv.references.Reference model.

Covers RelationshipType enum values, required/optional field validation,
phone number pattern acceptance and rejection, and a factory smoke test.
"""

from typing import Any

import pytest
from faker import Faker
from polyfactory.factories.pydantic_factory import ModelFactory
from pydantic import ValidationError

from pydanticcv.references import Reference, RelationshipType
from pydanticcv.references.reference import PhoneNumber, EmailAddress


fake = Faker()


class ReferenceFactory(ModelFactory[Reference]):
    """Factory for generating valid Reference instances."""

    __model__ = Reference

    @classmethod
    def create(cls, **kwargs: Any) -> Reference:
        """Create a valid Reference with sensible defaults.

        Args:
            **kwargs: Field overrides applied on top of defaults.

        Returns:
            A fully-validated Reference instance.
        """
        defaults: dict[str, Any] = {
            "Name": fake.name(),
            "Title": fake.job(),
            "Organization": fake.company(),
            "Relationship": fake.random_element(list(RelationshipType)),
        }
        defaults.update(kwargs)
        return Reference(**defaults)


class TestRelationshipType:
    """Tests for RelationshipType enum values."""

    @pytest.mark.parametrize(
        "value",
        ["Manager", "Colleague", "Professor", "Mentor", "Client", "Other"],
    )
    def test_all_values_are_valid(self, value: str) -> None:
        """Tests that every RelationshipType string value round-trips correctly.

        Args:
            value: String representation of the enum member.

        Returns:
            None
        """
        member = RelationshipType(value)
        assert member.value == value

    def test_invalid_value_raises(self) -> None:
        """Tests that an unrecognised string raises ValueError.

        Returns:
            None
        """
        with pytest.raises(ValueError):
            RelationshipType("Boss")


class TestReferenceValidation:
    """Tests for Reference field validation."""

    def test_required_fields_only(self) -> None:
        """Tests that a Reference with only required fields is valid.

        Returns:
            None
        """
        ref = Reference(
            Name="Jane Doe",
            Title="Engineering Manager",
            Organization="Acme Corp",
            Relationship=RelationshipType.Manager,
        )
        assert ref.Name == "Jane Doe"
        assert ref.Email is None
        assert ref.Phone is None
        assert ref.LinkedInURL is None

    def test_all_fields(self) -> None:
        """Tests that a Reference with all fields set is valid.

        Returns:
            None
        """
        ref = Reference(
            Name="John Smith",
            Title="Professor",
            Organization="State University",
            Relationship=RelationshipType.Professor,
            Email="j.smith@university.edu",
            Phone="+1 555-123-4567",
            LinkedInURL="https://linkedin.com/in/jsmith",
        )
        assert ref.Email == "j.smith@university.edu"
        assert ref.Phone == "+1 555-123-4567"
        assert ref.LinkedInURL is not None

    @pytest.mark.parametrize("field", ["Name", "Title", "Organization"])
    def test_empty_string_rejected(self, field: str) -> None:
        """Tests that empty strings are rejected for required string fields.

        Args:
            field: Name of the field to set to an empty string.

        Returns:
            None
        """
        kwargs: dict[str, Any] = {
            "Name": "Jane Doe",
            "Title": "Manager",
            "Organization": "Corp",
            "Relationship": RelationshipType.Colleague,
            field: "",
        }
        with pytest.raises(ValidationError):
            Reference(**kwargs)

    def test_missing_required_field_raises(self) -> None:
        """Tests that omitting a required field raises ValidationError.

        Returns:
            None
        """
        with pytest.raises(ValidationError):
            Reference(Name="Jane Doe", Title="Manager", Organization="Corp")  # type: ignore[call-arg]


class TestReferencePhoneValidation:
    """Tests for PhoneNumber pattern validation."""

    @pytest.mark.parametrize(
        "phone",
        [
            "+1 555-123-4567",
            "+44 20 7946 0958",
            "555-123-4567",
            "(555) 123-4567",
            "+49.30.12345678",
            "0031201234567",
        ],
    )
    def test_valid_phone_formats(self, phone: str) -> None:
        """Tests that common phone number formats are accepted.

        Args:
            phone: A phone number string to validate.

        Returns:
            None
        """
        ref = Reference(
            Name="A",
            Title="B",
            Organization="C",
            Relationship=RelationshipType.Other,
            Phone=phone,
        )
        assert ref.Phone == phone

    @pytest.mark.parametrize(
        "phone",
        [
            "abc",          # non-numeric
            "123",          # too short
            "+1" + "2" * 20,  # too long
        ],
    )
    def test_invalid_phone_formats(self, phone: str) -> None:
        """Tests that malformed phone numbers are rejected.

        Args:
            phone: An invalid phone number string.

        Returns:
            None
        """
        with pytest.raises(ValidationError):
            Reference(
                Name="A",
                Title="B",
                Organization="C",
                Relationship=RelationshipType.Other,
                Phone=phone,
            )


class TestReferenceFactory:
    """Smoke tests for ReferenceFactory."""

    def test_factory_creates_valid_instance(self) -> None:
        """Tests that the factory produces a valid Reference.

        Returns:
            None
        """
        ref = ReferenceFactory.create()
        assert isinstance(ref, Reference)
        assert ref.Name
        assert ref.Title
        assert ref.Organization
        assert isinstance(ref.Relationship, RelationshipType)

    def test_factory_accepts_overrides(self) -> None:
        """Tests that field overrides are applied correctly.

        Returns:
            None
        """
        ref = ReferenceFactory.create(Relationship=RelationshipType.Client)
        assert ref.Relationship == RelationshipType.Client
