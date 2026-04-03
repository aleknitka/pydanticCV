"""CELPIP (Canadian English Language Proficiency Index Program) Pydantic models.

The CELPIP is a Canadian English proficiency test evaluating listening, speaking,
reading, and writing skills.  Scores are reported as CLB (Canadian Language
Benchmark) levels from 4 to 12, which map directly onto the CEFR A2–C2 scale.

CLB-to-CEFR mapping:
    CLB 12   → C2
    CLB 10-11 → C1
    CLB 8-9  → B2
    CLB 7    → B1
    CLB 4-6  → A2

Contents:
    CELPIPCLBScore: Annotated int constrained to valid CLB levels (4-12).
    CELPIPScores: Per-skill CLB scores with validation.
    CELPIP: Full CELPIP exam record with computed CEFR level.
"""

__all__ = ["CELPIPCLBScore", "CELPIPScores", "CELPIP"]

from typing import Annotated, Literal

from pydantic import BaseModel, computed_field
from pydantic.functional_validators import AfterValidator

from pydanticcv.languages.certificates.base import CEFRLiteral
from pydanticcv.languages.certificates.eng.base import (
    EnglishLanguageProficiencyCertificate,
)
from pydanticcv.utils.date import PastDate


def _validate_clb_score(v: int) -> int:
    if not 4 <= v <= 12:
        raise ValueError(f"CELPIP CLB score must be between 4 and 12, got {v}")
    return v


CELPIPCLBScore = Annotated[int, AfterValidator(_validate_clb_score)]
"""CELPIP CLB (Canadian Language Benchmark) score: an int in the range 4-12."""


class CELPIPScores(BaseModel):
    """Per-skill CELPIP CLB scores.

    Attributes:
        Listening: Listening score (CLB 4-12).
        Speaking: Speaking score (CLB 4-12).
        Reading: Reading score (CLB 4-12).
        Writing: Writing score (CLB 4-12).
    """

    Listening: CELPIPCLBScore
    Speaking: CELPIPCLBScore
    Reading: CELPIPCLBScore
    Writing: CELPIPCLBScore


class CELPIP(EnglishLanguageProficiencyCertificate):
    """CELPIP exam record with scores and derived CEFR level.

    The CELPIP tests listening, speaking, reading, and writing.  Scores are
    reported as CLB (Canadian Language Benchmark) levels from 4 to 12.
    The overall CEFR level is derived from the average of the four section
    scores, rounded to the nearest integer.

    Attributes:
        Scores: Per-skill CLB scores (Listening, Speaking, Reading, Writing).
        DateTaken: Date the exam was sat (inherited; must not be in the future).
        ExamType: General or Academic test variant.
        CEFRLevel: CEFR level derived from the average CLB score (computed).
    """

    Scores: CELPIPScores
    DateTaken: PastDate
    ExamType: Literal["General", "Academic"]

    @computed_field
    @property
    def CEFRLevel(self) -> CEFRLiteral:
        """Derive the CEFR level from the average CLB score.

        The CEFR level is computed from the average of the four CLB section
        scores, rounded to the nearest integer.

        Returns:
            CEFR level string corresponding to the average CLB score.
        """
        avg_clb = round(
            (
                self.Scores.Listening
                + self.Scores.Speaking
                + self.Scores.Reading
                + self.Scores.Writing
            )
            / 4
        )
        if avg_clb >= 12:
            return "C2"
        elif avg_clb >= 10:
            return "C1"
        elif avg_clb >= 8:
            return "B2"
        elif avg_clb >= 7:
            return "B1"
        else:
            return "A2"
