"""Utilities for anything to do with locations"""

from pydantic import BaseModel
from pydantic_extra_types.country import CountryAlpha3
from pydantic_extra_types.coordinate import (
    Latitude as _Latitude,
    Longitude as _Longitude,
)


class Country(BaseModel):
    name: str
    iso: CountryAlpha3


class Location(BaseModel):
    Latitude: _Latitude
    Longitude: _Longitude
