"""TEF (Test d'Évaluation de Français) Pydantic models.

The TEF is a French proficiency test issued by the Paris Île-de-France Chamber
of Commerce and Industry.  It evaluates six skills: listening comprehension,
spoken expression, reading comprehension, written expression, structure, and
vocabulary.  Scores are reported as levels A, B, or C (each with sub-levels).

The TEF is used for French immigration (e.g., Quebec's Arrima) and citizenship
applications.  Scores map onto the CEFR A1–C2 scale.

Score-to-CEFR mapping:
    Level C (score 14-20) → C1 or C2
    Level B (score 10-13) → B1 or B2
    Level A (score 4-9)   → A1 or A2

Contents:
    TEFSectionScore: Annotated int constrained to TEF section scores (0-20).
    TEFScores: Six-section TEF scores with validation.
    TEF: Full TEF exam record with computed CEFR level.
"""

__all__ = ["TEFSectionScore", "TEFScores", "TEF"]

from typing import Annotated, Literal

from pydantic import BaseModel, computed_field
from pydantic.functional_validators import AfterValidator

from pydanticcv.languages.certificates.base import CEFRLiteral
from pydanticcv.languages.certificates.fra.base import (
    FrenchLanguageProficiencyCertificate,
)
from pydanticcv.utils.date import PastDate


def _validate_section_score(v: int) -> int:
    if not 0 <= v <= 20:
        raise ValueError(f"TEF section score must be between 0 and 20, got {v}")
    return v


TEFSectionScore = Annotated[int, AfterValidator(_validate_section_score)]
"""TEF section score: an int in the range 0-20."""


class TEFScores(BaseModel):
    """Six-section TEF scores.

    The TEF evaluates six components:
        - Compréhension orale (Listening comprehension)
        - Expression orale (Spoken expression)
        - Compréhension écrite (Reading comprehension)
        - Expression écrite (Written expression)
        - Structure du français (French structure/grammar)
        - Vocabulaire (Vocabulary)

    Attributes:
        Listening: Listening comprehension score (0-20).
        Speaking: Spoken expression score (0-20).
        Reading: Reading comprehension score (0-20).
        Writing: Written expression score (0-20).
        Structure: French structure/grammar score (0-20).
        Vocabulary: Vocabulary score (0-20).
    """

    Listening: TEFSectionScore
    Speaking: TEFSectionScore
    Reading: TEFSectionScore
    Writing: TEFSectionScore
    Structure: TEFSectionScore
    Vocabulary: TEFSectionScore


class TEF(FrenchLanguageProficiencyCertificate):
    """TEF exam record with scores and derived CEFR level.

    The TEF evaluates six language skills.  The CEFR level is derived from
    the average of all six section scores, rounded to the nearest integer.

    Attributes:
        Scores: Six-section TEF scores.
        DateTaken: Date the exam was sat (inherited; must not be in the future).
        ExamLevel: High-level exam level (A, B, or C).
        CEFRLevel: CEFR level derived from the average score (computed).
    """

    Scores: TEFScores
    DateTaken: PastDate
    ExamLevel: Literal["A", "B", "C"]

    @computed_field
    @property
    def CEFRLevel(self) -> CEFRLiteral:
        """Derive the CEFR level from the average TEF section score.

        The CEFR level is computed from the average of all six section scores,
        rounded to the nearest integer.

        Returns:
            CEFR level string corresponding to the average score.
        """
        avg_score = round(
            (
                self.Scores.Listening
                + self.Scores.Speaking
                + self.Scores.Reading
                + self.Scores.Writing
                + self.Scores.Structure
                + self.Scores.Vocabulary
            )
            / 6
        )
        if avg_score >= 14:
            return "C2"
        elif avg_score >= 10:
            return "C1"
        elif avg_score >= 8:
            return "B2"
        elif avg_score >= 6:
            return "B1"
        elif avg_score >= 4:
            return "A2"
        else:
            return "A1"
