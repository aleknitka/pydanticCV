"""Shared base types for skill proficiency certificates.

Provides the base model that all skill certificate records inherit from.

Contents:
    IssuerAllowlist: Literal type with curated list of approved certification issuers.
    SkillCertificate: Base Pydantic model for any skill certification record.
"""

__all__ = ["SkillCertificate", "IssuerAllowlist"]

from datetime import date
from typing import Literal

from pydantic import AnyUrl, BaseModel

from pydanticcv.utils.date import PastDate

# Curated allowlist of recognized certification issuers
IssuerAllowlist = Literal["AWS", "Azure", "GCP", "PMI", "ISC2", "CompTIA"]


class SkillCertificate(BaseModel):
    """Base model for a professional skill certification record.

    Attributes:
        CertificateName: Full name of the certification (e.g. "AWS Certified Solutions Architect").
        Issuer: Body that issued the certificate; must be from the allowlist
            (AWS, Azure, GCP, PMI, ISC2, CompTIA).
        DateObtained: Date the certificate was awarded; must not be in the future.
        ExpiryDate: Optional expiry date; unconstrained — may be past or future.
        Link: Optional URL to the official certificate or verification page.
    """

    CertificateName: str
    Issuer: IssuerAllowlist
    DateObtained: PastDate
    ExpiryDate: date | None = None
    Link: AnyUrl | None = None
