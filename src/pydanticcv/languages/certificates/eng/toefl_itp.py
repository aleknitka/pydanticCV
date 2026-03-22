"""TOEFL ITP (Institutional Testing Program) Pydantic models.

The TOEFL ITP is a paper-based test used by institutions for placement,
progress monitoring, and programme exit decisions.  It differs from the
iBT in three key ways:

- Three sections only (no Speaking): Listening Comprehension, Structure
  and Written Expression, Reading Comprehension.
- Scores are reported on a 677-point scale (Level 1) or 500-point scale
  (Level 2), not as a simple sum or average of raw scores.
- It is not subject to the 2026 ETS iBT scale change.

Score ranges:
    Level 1: total 310-677 (advanced to proficient).
    Level 2: total 200-500 (intermediate).

Contents:
    TOEFLITPLevel: Literal type for Level 1 or Level 2 variants.
    TOEFLITPSectionScore: Annotated int constrained to the valid scaled-score range.
    TOEFLITPScores: Section scaled scores with computed total.
    TOEFLITPCEFR: Approximate CEFR level for Level 1 total scores.
    TOEFLITP: Full TOEFL ITP exam record.
"""

__all__ = ["TOEFLITPLevel", "TOEFLITPSectionScore", "TOEFLITPScores", "TOEFLITP"]

from typing import Annotated, Literal
from pydantic import BaseModel, computed_field, model_validator
from pydantic.functional_validators import AfterValidator
from pydanticcv.languages.certificates.base import CEFRLiteral
from pydanticcv.languages.certificates.eng.base import (
    EnglishLanguageProficiencyCertificate,
)

TOEFLITPLevel = Literal["Level 1", "Level 2"]
"""TOEFL ITP test level.

Level 1 targets upper-intermediate to advanced learners (score range 310-677).
Level 2 targets lower to intermediate learners (score range 200-500).
"""

# ---------------------------------------------------------------------------
# Section score ranges per level (scaled scores as reported by ETS)
# Level 1: Listening 31-68, Structure 31-68, Reading 31-67
# Level 2: Listening 20-50, Structure 16-46, Reading 18-52
# ---------------------------------------------------------------------------
_LEVEL_TOTAL_RANGE: dict[str, tuple[int, int]] = {
    "Level 1": (310, 677),
    "Level 2": (200, 500),
}

# CEFR equivalences for Level 1 total scores (ETS approximate mapping).
# Level 2 does not have an official CEFR mapping.
_ITP_LEVEL1_CEFR_THRESHOLDS: list[tuple[int, CEFRLiteral]] = [
    (543, "C1"),
    (460, "B2"),
    (337, "B1"),
    (310, "A2"),
]


def _validate_itp_section(v: int) -> int:
    if not 16 <= v <= 68:
        raise ValueError(f"ITP section scaled score must be 16-68, got {v}")
    return v


TOEFLITPSectionScore = Annotated[int, AfterValidator(_validate_itp_section)]
"""TOEFL ITP section scaled score: integer in the range 16-68.

The upper bound of 68 covers the maximum across all sections and both levels.
Individual section ceilings are lower (68 for Listening/Structure Level 1,
67 for Reading Level 1, 52/50/46 for Level 2 sections).
"""


class TOEFLITPScores(BaseModel):
    """TOEFL ITP section scaled scores.

    Attributes:
        ListeningComprehension: Listening Comprehension scaled score.
        StructureWrittenExpression: Structure and Written Expression scaled score.
        ReadingComprehension: Reading Comprehension scaled score.
        Total: Sum of the three section scores multiplied by 10/3, rounded to
            the nearest whole number (computed).  This produces the
            677-point or 500-point total reported on the score report.
    """

    ListeningComprehension: TOEFLITPSectionScore
    StructureWrittenExpression: TOEFLITPSectionScore
    ReadingComprehension: TOEFLITPSectionScore

    @computed_field
    @property
    def Total(self) -> int:
        """Compute the ITP total score from the three section scaled scores.

        Formula: round((L + S + R) * 10 / 3)

        Returns:
            Total score on the 677- or 500-point scale.
        """
        return round(
            (
                self.ListeningComprehension
                + self.StructureWrittenExpression
                + self.ReadingComprehension
            )
            * 10
            / 3
        )


class TOEFLITP(EnglishLanguageProficiencyCertificate):
    """TOEFL ITP exam record.

    Attributes:
        Level: Test level — ``"Level 1"`` (310-677) or ``"Level 2"`` (200-500).
        AwardingInstitution: Issuing institution; defaults to ``"ETS"``.
        Scores: Section scaled scores and computed total.
        CEFRLevel: Approximate CEFR level derived from the Level 1 total score
            (computed).  ``None`` for Level 2 records as ETS does not publish
            an official Level 2 CEFR mapping.
    """

    Level: TOEFLITPLevel
    AwardingInstitution: str = "ETS"
    Scores: TOEFLITPScores

    @model_validator(mode="after")
    def check_total_in_range(self) -> "TOEFLITP":
        """Validate that the computed total falls within the expected range for the level.

        Returns:
            The validated model instance.

        Raises:
            ValueError: If the total score is outside the valid range for the chosen level.
        """
        lo, hi = _LEVEL_TOTAL_RANGE[self.Level]
        total = self.Scores.Total
        if not lo <= total <= hi:
            raise ValueError(
                f"TOEFL ITP {self.Level} total score must be {lo}-{hi}, got {total}"
            )
        return self

    @computed_field
    @property
    def CEFRLevel(self) -> CEFRLiteral | None:
        """Derive the approximate CEFR level from the Level 1 total score.

        Returns:
            CEFR level string for Level 1 records, or ``None`` for Level 2.
        """
        if self.Level != "Level 1":
            return None
        total = self.Scores.Total
        for threshold, cefr in _ITP_LEVEL1_CEFR_THRESHOLDS:
            if total >= threshold:
                return cefr
        return None
