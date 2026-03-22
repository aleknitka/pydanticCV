"""Shared base types for language proficiency certificates.

Provides the abstract base model that all exam-specific models inherit from,
as well as shared type aliases used across exam modules.

Contents:
    LanguageProficiencyCertificate: Base Pydantic model for any exam record.
    CEFRLiteral: Type alias for the six CEFR proficiency level strings.
"""

__all__ = ["LanguageProficiencyCertificate", "CEFRLiteral"]

from typing import Literal
from pydantic import BaseModel, AnyUrl, Field
from pydanticcv.utils.date import PastDate
from pydantic_extra_types.language_code import ISO639_3


CEFRLiteral = Literal["A1", "A2", "B1", "B2", "C1", "C2"]
"""CEFR proficiency level labels, from beginner (A1) to mastery (C2)."""


class LanguageProficiencyCertificate(BaseModel):
    """Abstract base for a language proficiency exam record.

    Attributes:
        DateTaken: Date the exam was sat. Accepts multiple string formats;
            must not be in the future.
        Link: URL to the official score report or certificate.
    """

    DateTaken: PastDate
    Link: AnyUrl
    LanguageCertified: ISO639_3 = Field(..., default_factory=ISO639_3)
