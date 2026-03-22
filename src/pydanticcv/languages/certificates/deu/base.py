"""Base for German language Certificates"""

__all__ = ["GermanLanguageProficiencyCertificate"]

from pydanticcv.languages.certificates.base import LanguageProficiencyCertificate
from pydanticcv.languages.languages import Language
from pydantic_extra_types.language_code import ISO639_3


class GermanLanguageProficiencyCertificate(LanguageProficiencyCertificate):
    CertifiedLanguage = Language(name="German", iso=ISO639_3("deu"))