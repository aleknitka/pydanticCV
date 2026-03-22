"""Goethe-Zertifikat German language certificate Pydantic models.

The Goethe-Zertifikat is issued by the Goethe-Institut and covers all six
CEFR levels (A1-C2).  Each exam consists of four skills (Listening, Reading,
Writing, Speaking), each worth 25 points, for a maximum total of 100 points.

A result of ≥ 60 points is required to pass.  Grades are awarded as follows:

    90-100  mit Auszeichnung  (with distinction)
    80-89.5 sehr gut          (very good)
    70-79.5 gut               (good)
    60-69.5 befriedigend      (satisfactory)
    <60     nicht bestanden   (failed)

Contents:
    GoetheZertifikatSectionScore: Annotated float constrained to 0-25.
    GoetheZertifikatGrade: Literal type for the five possible grades.
    GoetheZertifikatScores: Per-skill scores with a computed total.
    GoetheZertifikat: Full Goethe-Zertifikat exam record with computed grade.
"""

__all__ = [
    "GoetheZertifikatSectionScore",
    "GoetheZertifikatGrade",
    "GoetheZertifikatScores",
    "GoetheZertifikat",
]

from typing import Annotated, Literal
from pydantic import BaseModel, computed_field
from pydantic.functional_validators import AfterValidator
from pydanticcv.languages.certificates.base import CEFRLiteral
from pydanticcv.languages.certificates.deu.base import (
    GermanLanguageProficiencyCertificate,
)
from pydanticcv.utils.date import PastDate


def _validate_section_score(v: float) -> float:
    if not 0 <= v <= 25:
        raise ValueError(f"Section score must be between 0 and 25, got {v}")
    return v


GoetheZertifikatSectionScore = Annotated[float, AfterValidator(_validate_section_score)]
"""Goethe-Zertifikat section score: a float in the range 0-25."""

GoetheZertifikatGrade = Literal[
    "mit Auszeichnung", "sehr gut", "gut", "befriedigend", "nicht bestanden"
]
"""Goethe-Zertifikat grade, derived from the total score."""


class GoetheZertifikatScores(BaseModel):
    """Per-skill Goethe-Zertifikat scores with a computed total.

    Attributes:
        Listening: Score for the Listening (Hören) section (0-25).
        Reading: Score for the Reading (Lesen) section (0-25).
        Writing: Score for the Writing (Schreiben) section (0-25).
        Speaking: Score for the Speaking (Sprechen) section (0-25).
        Total: Sum of the four section scores (computed, 0-100).
    """

    Listening: GoetheZertifikatSectionScore
    Reading: GoetheZertifikatSectionScore
    Writing: GoetheZertifikatSectionScore
    Speaking: GoetheZertifikatSectionScore

    @computed_field
    @property
    def Total(self) -> float:
        """Compute the total score as the sum of the four sections.

        Returns:
            Total score in the range 0-100.
        """
        return self.Listening + self.Reading + self.Writing + self.Speaking


class GoetheZertifikat(GermanLanguageProficiencyCertificate):
    """Goethe-Zertifikat exam record with scores, metadata, and derived grade.

    Attributes:
        Level: CEFR level for which the exam was taken (A1-C2).
        Scores: Per-skill scores and computed total.
        DateTaken: Date the exam was sat (inherited; must not be in the future).
        Link: Optional URL to the official certificate (inherited).
        Grade: Grade string derived from the total score (computed).
    """

    Level: CEFRLiteral
    Scores: GoetheZertifikatScores
    DateTaken: PastDate

    @computed_field
    @property
    def Grade(self) -> GoetheZertifikatGrade:
        """Derive the grade from the total score.

        Returns:
            Grade string corresponding to the total score.
        """
        total = self.Scores.Total
        if total >= 90:
            return "mit Auszeichnung"
        elif total >= 80:
            return "sehr gut"
        elif total >= 70:
            return "gut"
        elif total >= 60:
            return "befriedigend"
        else:
            return "nicht bestanden"
