"""Utilities for anything to do with locations.

Contents:
    Country: Pydantic model for a named country with ISO 3166-1 alpha-3 code.
    Location: Pydantic model for a geographic coordinate pair.
    CVAddress: Pydantic model for a human-readable CV address (city + country).
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
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

    model_config = ConfigDict(arbitrary_types_allowed=True)

    City: Optional[str] = Field(default=None)
    Country: Optional[Country] = Field(default=None)
