"""Base for Chinese language certificates."""

__all__ = ["ChineseLanguageProficiencyCertificate"]

from typing import ClassVar

from pydanticcv.languages.certificates.base import LanguageProficiencyCertificate
from pydanticcv.languages.languages import Language
from pydantic_extra_types.language_code import ISO639_3


class ChineseLanguageProficiencyCertificate(LanguageProficiencyCertificate):
    """Base model for all Chinese language proficiency certificates."""

    CertifiedLanguage: ClassVar[Language] = Language(
        name="Chinese", iso=ISO639_3("zho")
    )
