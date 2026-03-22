"""Base for French language Certificates"""

__all__ = ["FrenchLanguageProficiencyCertificate"]

from pydanticcv.languages.certificates.base import LanguageProficiencyCertificate
from pydanticcv.languages.languages import Language
from pydantic_extra_types.language_code import ISO639_3


class FrenchLanguageProficiencyCertificate(LanguageProficiencyCertificate):
    CertifiedLanguage = Language(name="French", iso=ISO639_3("fra"))