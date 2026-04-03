"""Chinese language proficiency certificates."""

__all__ = ["ChineseLanguageProficiencyCertificate", "HSK", "HSKLevel"]

from pydanticcv.languages.certificates.zho.base import (
    ChineseLanguageProficiencyCertificate,
)
from pydanticcv.languages.certificates.zho.hsk import HSK, HSKLevel
