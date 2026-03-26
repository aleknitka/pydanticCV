"""DELF and DALF French language certificate Pydantic models.

DELF (Diplôme d'Études en Langue Française) and DALF (Diplôme Approfondi de
Langue Française) are lifetime diplomas issued by the French Ministry of
Education.  Both exams share the same four-skill structure (25 pts each,
100 pts total).  DELF covers CEFR levels A1–B2; DALF covers C1–C2.

A minimum total of 50/100 and at least 5/25 per skill are required to pass.
The diploma itself certifies the CEFR level at which the exam was sat.

Contents:
    DELFDALFSectionScore: Annotated float constrained to 0-25.
    DELFDALFScores: Per-skill scores with a computed total.
    DELF: Full DELF exam record with computed CEFR level (A1-B2).
    DALF: Full DALF exam record with computed CEFR level (C1-C2).
"""

__all__ = [
    "DELFDALFSectionScore",
    "DELFDALFScores",
    "DELF",
    "DALF",
]

from typing import Annotated, Literal

from pydantic import BaseModel, computed_field
from pydantic.functional_validators import AfterValidator

from pydanticcv.languages.certificates.fra.base import FrenchLanguageProficiencyCertificate
from pydanticcv.utils.date import PastDate


def _validate_section_score(v: float) -> float:
    if not 0 <= v <= 25:
        raise ValueError(f"Section score must be between 0 and 25, got {v}")
    return v


DELFDALFSectionScore = Annotated[float, AfterValidator(_validate_section_score)]
"""DELF/DALF section score: a float in the range 0–25."""


class DELFDALFScores(BaseModel):
    """Per-skill DELF/DALF scores with a computed total.

    Attributes:
        Listening: Score for the Listening (Compréhension Orale) section (0–25).
        Reading: Score for the Reading (Compréhension Écrite) section (0–25).
        Writing: Score for the Writing (Expression Écrite) section (0–25).
        Speaking: Score for the Speaking (Expression Orale) section (0–25).
        Total: Sum of the four section scores (computed, 0–100).
    """

    Listening: DELFDALFSectionScore
    Reading: DELFDALFSectionScore
    Writing: DELFDALFSectionScore
    Speaking: DELFDALFSectionScore

    @computed_field
    @property
    def Total(self) -> float:
        """Compute the total score as the sum of the four sections.

        Returns:
            Total score in the range 0–100.
        """
        return self.Listening + self.Reading + self.Writing + self.Speaking


class DELF(FrenchLanguageProficiencyCertificate):
    """DELF exam record with scores and derived CEFR level.

    DELF (Diplôme d'Études en Langue Française) is a lifetime diploma covering
    CEFR levels A1 through B2.  The exam is taken at a specific level chosen
    at registration; passing the exam certifies that level.

    Attributes:
        Level: CEFR level at which the exam was sat (A1–B2).
        Scores: Per-skill scores and computed total.
        DateTaken: Date the exam was sat (inherited; must not be in the future).
        Link: Optional URL to the official diploma (inherited).
        CEFRLevel: CEFR level certified by the diploma (computed; equals Level).
    """

    Level: Literal["A1", "A2", "B1", "B2"]
    Scores: DELFDALFScores
    DateTaken: PastDate

    @computed_field
    @property
    def CEFRLevel(self) -> Literal["A1", "A2", "B1", "B2"]:
        """Return the CEFR level certified by this diploma.

        Returns:
            The CEFR level at which the exam was sat and passed.
        """
        return self.Level


class DALF(FrenchLanguageProficiencyCertificate):
    """DALF exam record with scores and derived CEFR level.

    DALF (Diplôme Approfondi de Langue Française) is a lifetime diploma
    covering CEFR levels C1 and C2.  The exam is taken at a specific level
    chosen at registration; passing certifies that level.

    Attributes:
        Level: CEFR level at which the exam was sat (C1 or C2).
        Scores: Per-skill scores and computed total.
        DateTaken: Date the exam was sat (inherited; must not be in the future).
        Link: Optional URL to the official diploma (inherited).
        CEFRLevel: CEFR level certified by the diploma (computed; equals Level).
    """

    Level: Literal["C1", "C2"]
    Scores: DELFDALFScores
    DateTaken: PastDate

    @computed_field
    @property
    def CEFRLevel(self) -> Literal["C1", "C2"]:
        """Return the CEFR level certified by this diploma.

        Returns:
            The CEFR level at which the exam was sat and passed.
        """
        return self.Level
