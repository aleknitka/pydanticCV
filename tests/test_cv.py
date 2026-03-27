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
