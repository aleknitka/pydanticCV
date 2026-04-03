"""Personal information models for a CV.

Contents:
    Name: Structured name with title, given names, family name, and preferred name.
    ContactInfo: Contact details including email, phone, URLs, and social profiles.
    PersonalInfo: Top-level personal information section of a CV.
    SocialPlatform: Enum for social/professional platform types.
    ProfileLink: Model for profile URLs with automatic platform detection.
"""

__all__ = ["Name", "ContactInfo", "PersonalInfo", "SocialPlatform", "ProfileLink"]

import re
from enum import StrEnum
from typing import Annotated, Optional

from pydantic import AnyUrl, BaseModel, BeforeValidator, EmailStr, computed_field
from pydantic_extra_types.phone_numbers import PhoneNumber

from pydanticcv.utils.locations import CVAddress


class SocialPlatform(StrEnum):
    """Social and professional platform types for profile links.

    Platforms:
        LinkedIn: LinkedIn professional network.
        GitHub: GitHub code hosting.
        Twitter: Twitter/X microblogging.
        Website: Personal website or portfolio.
        ORCID: Open Researcher and Contributor ID.
        GoogleScholar: Google Scholar academic profile.
        ResearchGate: ResearchGate research network.
        Behance: Behance creative portfolio.
        Dribbble: Dribbble design portfolio.
        Custom: Other or unspecified platform.
    """

    LinkedIn = "LinkedIn"
    GitHub = "GitHub"
    Twitter = "Twitter"
    Website = "Website"
    ORCID = "ORCID"
    GoogleScholar = "GoogleScholar"
    ResearchGate = "ResearchGate"
    Behance = "Behance"
    Dribbble = "Dribbble"
    Custom = "Custom"


# URL pattern regexes for platform detection
_PLATFORM_PATTERNS: list[tuple[re.Pattern[str], SocialPlatform]] = [
    (re.compile(r"linkedin\.com/(in|pub)/", re.IGNORECASE), SocialPlatform.LinkedIn),
    (re.compile(r"github\.com/", re.IGNORECASE), SocialPlatform.GitHub),
    (re.compile(r"(twitter\.com|x\.com)/", re.IGNORECASE), SocialPlatform.Twitter),
    (re.compile(r"orcid\.org/", re.IGNORECASE), SocialPlatform.ORCID),
    (re.compile(r"scholar\.google\.com/", re.IGNORECASE), SocialPlatform.GoogleScholar),
    (re.compile(r"researchgate\.net/", re.IGNORECASE), SocialPlatform.ResearchGate),
    (re.compile(r"behance\.net/", re.IGNORECASE), SocialPlatform.Behance),
    (re.compile(r"dribbble\.com/", re.IGNORECASE), SocialPlatform.Dribbble),
]


def _detect_platform(url: str) -> SocialPlatform:
    """Detect the social platform from a URL.

    Args:
        url: The URL to analyze.

    Returns:
        The detected SocialPlatform, or Custom if no match.
    """
    for pattern, platform in _PLATFORM_PATTERNS:
        if pattern.search(url):
            return platform
    return SocialPlatform.Custom


def _validate_https(url: AnyUrl | str) -> AnyUrl:
    """Validate that the URL uses HTTPS scheme.

    Args:
        url: The URL to validate (string or AnyUrl).

    Returns:
        The validated AnyUrl.

    Raises:
        ValueError: If the URL scheme is not https.
    """
    # Convert string to AnyUrl if needed
    if isinstance(url, str):
        url = AnyUrl(url)
    if url.scheme != "https":
        msg = "URL must use HTTPS scheme"
        raise ValueError(msg)
    return url


class ProfileLink(BaseModel):
    """A social or professional profile link with automatic platform detection.

    Attributes:
        url: The profile URL (must use HTTPS).
        platform: Automatically detected platform based on URL pattern.
        label: Optional user-provided label for the link.
    """

    url: Annotated[AnyUrl, BeforeValidator(_validate_https)]
    label: Optional[str] = None

    @computed_field
    @property
    def platform(self) -> SocialPlatform:
        """Detect the platform from the URL."""
        return _detect_platform(str(self.url))


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
        Twitter: Twitter/X profile URL.
        ORCID: ORCID researcher profile URL.
        GoogleScholar: Google Scholar profile URL.
        ResearchGate: ResearchGate profile URL.
        Behance: Behance portfolio URL.
        Dribbble: Dribbble portfolio URL.
        ProfileLinks: Additional profile links with auto-detected platforms.
        OtherUrls: Additional URLs (e.g. personal blog, portfolio).
    """

    Email: Optional[EmailStr] = None
    Phone: Optional[PhoneNumber] = None
    Website: Optional[AnyUrl] = None
    LinkedIn: Optional[AnyUrl] = None
    GitHub: Optional[AnyUrl] = None
    Twitter: Optional[AnyUrl] = None
    ORCID: Optional[AnyUrl] = None
    GoogleScholar: Optional[AnyUrl] = None
    ResearchGate: Optional[AnyUrl] = None
    Behance: Optional[AnyUrl] = None
    Dribbble: Optional[AnyUrl] = None
    ProfileLinks: list[ProfileLink] = []
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
