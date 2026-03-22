"""Base for English language Certificates"""

__all__ = ["EnglishLanguageProficiencyCertificate"]

from typing import ClassVar

from pydanticcv.languages.certificates.base import LanguageProficiencyCertificate
from pydanticcv.languages.languages import Language
from pydantic_extra_types.language_code import ISO639_3


class EnglishLanguageProficiencyCertificate(LanguageProficiencyCertificate):
    """Base model for all English language proficiency certificates."""

    CertifiedLanguage: ClassVar[Language] = Language(
        name="English", iso=ISO639_3("eng")
    )
