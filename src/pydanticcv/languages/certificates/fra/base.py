"""Base for French language Certificates"""

__all__ = ["FrenchLanguageProficiencyCertificate"]

from typing import ClassVar

from pydanticcv.languages.certificates.base import LanguageProficiencyCertificate
from pydanticcv.languages.languages import Language
from pydantic_extra_types.language_code import ISO639_3


class FrenchLanguageProficiencyCertificate(LanguageProficiencyCertificate):
    """Base model for all French language proficiency certificates."""

    CertifiedLanguage: ClassVar[Language] = Language(name="French", iso=ISO639_3("fra"))
