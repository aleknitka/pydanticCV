"""TCF (Test de Connaissance du Français) Pydantic models.

The TCF is a general French proficiency test issued by France Éducation
International.  It produces a scaled score from 100 to 699 based on the
compulsory components (reading comprehension, listening comprehension, and
language structures), mapping directly onto the CEFR A1–C2 scale.

Optional productive-skills components (Speaking and Writing) each yield a
separate score on a 0–20 scale and are not used for the CEFR level derivation.

Score-to-CEFR mapping:
    600–699  C2
    500–599  C1
    400–499  B2
    300–399  B1
    200–299  A2
    100–199  A1

Contents:
    TCFCompulsoryScore: Annotated int constrained to 100-699.
    TCFProductiveScore: Annotated int constrained to 0-20.
    TCF: Full TCF exam record with computed CEFR level.
"""

__all__ = [
    "TCFCompulsoryScore",
    "TCFProductiveScore",
    "TCF",
]

from typing import Annotated, Literal

from pydantic import computed_field
from pydantic.functional_validators import AfterValidator

from pydanticcv.languages.certificates.base import CEFRLiteral
from pydanticcv.languages.certificates.fra.base import FrenchLanguageProficiencyCertificate
from pydanticcv.utils.date import PastDate


def _validate_compulsory_score(v: int) -> int:
    if not 100 <= v <= 699:
        raise ValueError(f"TCF compulsory score must be between 100 and 699, got {v}")
    return v


def _validate_productive_score(v: int) -> int:
    if not 0 <= v <= 20:
        raise ValueError(f"TCF productive-skills score must be between 0 and 20, got {v}")
    return v


TCFCompulsoryScore = Annotated[int, AfterValidator(_validate_compulsory_score)]
"""TCF compulsory-component score: an int in the range 100–699."""

TCFProductiveScore = Annotated[int, AfterValidator(_validate_productive_score)]
"""TCF productive-skills score (speaking or writing): an int in the range 0–20."""


class TCF(FrenchLanguageProficiencyCertificate):
    """TCF exam record with a global score and derived CEFR level.

    The compulsory score (100–699) determines the CEFR level.  Speaking and
    Writing scores from the optional productive-skills components may be stored
    separately but do not affect the CEFR level derivation.

    Attributes:
        Score: Compulsory-component global score (100–699).
        Speaking: Optional score for the Speaking component (0–20).
        Writing: Optional score for the Writing component (0–20).
        DateTaken: Date the exam was sat (inherited; must not be in the future).
        Link: Optional URL to the official score report (inherited).
        CEFRLevel: CEFR level derived from the compulsory score (computed).
    """

    Score: TCFCompulsoryScore
    DateTaken: PastDate
    Speaking: TCFProductiveScore | None = None
    Writing: TCFProductiveScore | None = None

    @computed_field
    @property
    def CEFRLevel(self) -> CEFRLiteral:
        """Derive the CEFR level from the compulsory global score.

        Returns:
            CEFR level string corresponding to the compulsory score.
        """
        if self.Score >= 600:
            return "C2"
        elif self.Score >= 500:
            return "C1"
        elif self.Score >= 400:
            return "B2"
        elif self.Score >= 300:
            return "B1"
        elif self.Score >= 200:
            return "A2"
        else:
            return "A1"
