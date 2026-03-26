"""Self-reported language proficiency using the CEFR framework.

Contents:
    SelfReportedCEFR: Pydantic model for a self-assessed CEFR level.
"""

__all__ = ["SelfReportedCEFR"]

from pydantic import BaseModel
from pydantic_extra_types.language_code import ISO639_3
from pydanticcv.languages.certificates.base import CEFRLiteral


class SelfReportedCEFR(BaseModel):
    """A self-declared CEFR proficiency level for a language.

    Attributes:
        Language: ISO 639-3 code of the language (e.g. ``"eng"``, ``"spa"``).
        Level: Self-assessed overall CEFR level (A1–C2).
    """

    Language: ISO639_3
    Level: CEFRLiteral
