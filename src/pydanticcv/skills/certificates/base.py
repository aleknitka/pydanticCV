"""Shared base types for skill proficiency certificates.

Provides the base model that all skill certificate records inherit from.

Contents:
    SkillCertificate: Base Pydantic model for any skill certification record.
"""

__all__ = ["SkillCertificate"]

from datetime import date

from pydantic import AnyUrl, BaseModel

from pydanticcv.utils.date import PastDate


class SkillCertificate(BaseModel):
    """Base model for a professional skill certification record.

    Attributes:
        CertificateName: Full name of the certification (e.g. "AWS Certified Solutions Architect").
        IssuingOrganisation: Body that issued the certificate (e.g. "Amazon Web Services").
        DateObtained: Date the certificate was awarded; must not be in the future.
        ExpiryDate: Optional expiry date; unconstrained — may be past or future.
        Link: Optional URL to the official certificate or verification page.
    """

    CertificateName: str
    IssuingOrganisation: str
    DateObtained: PastDate
    ExpiryDate: date | None = None
    Link: AnyUrl | None = None
