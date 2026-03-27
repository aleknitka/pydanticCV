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


_Name = Name  # alias avoids field-name shadowing the class in annotations


class PersonalInfo(BaseModel):
    """Personal information section of a CV.

    Attributes:
        Name: Structured name. Required.
        Contact: Contact details.
        Address: Home or mailing address.
        Photo: URL to a profile photo or headshot.
    """

    Name: _Name
    Contact: Optional[ContactInfo] = None
    Address: Optional[CVAddress] = None
    Photo: Optional[AnyUrl] = None
