"""Utilities for anything to do with locations"""

from pydantic import BaseModel, Field
from pydantic_extra_types.country import CountryAlpha3
from pydantic_extra_types.coordinate import Latitude, Longitude


class Country(BaseModel):
    name: str
    iso: CountryAlpha3


class Location(BaseModel):
    Latitude: Latitude = Field(..., decimal_places=2, default_factory=Latitude)
    Longitude: Longitude = Field(..., decimal_places=2, default_factory=Longitude)