"""TOEFL iBT (Internet-Based Test) Pydantic models.

Models both the legacy (pre-2026, 0-120 scale) and current (2026+, 1-6 scale)
TOEFL iBT scoring systems, and provides conversion methods between them using
the official ETS lookup tables from ``toefl_ibt_conversion``.

Score ranges:
    Legacy: each section 0-30 (int), total = sum of four sections (0-120).
    New:    each section 1-6 (float, 0.5 steps), overall = avg rounded to 0.5.

Contents:
    TOEFLiBTLegacySectionScore: Annotated int for legacy section scores (0-30).
    TOEFLiBTSectionScore: Annotated float for new section scores (1-6, 0.5 steps).
    TOEFLiBTLegacyScores: Legacy section scores with computed total.
    TOEFLiBTScores: New section scores with computed overall average.
    TOEFLiBTLegacy: Full legacy exam record with CEFR level and conversion to new scale.
    TOEFLiBT: Full new-scale exam record with CEFR level and conversion to legacy scale.
"""

from __future__ import annotations

__all__ = [
    "TOEFLiBTLegacySectionScore",
    "TOEFLiBTSectionScore",
    "TOEFLiBTLegacyScores",
    "TOEFLiBTScores",
    "TOEFLiBTLegacy",
    "TOEFLiBT",
]
from typing import Annotated
from pydantic import BaseModel, computed_field
from pydantic.functional_validators import AfterValidator
from pydanticcv.languages.certificates.base import CEFRLiteral
from pydanticcv.languages.certificates.eng.base import (
    EnglishLanguageProficiencyCertificate,
)

from pydanticcv.languages.certificates.eng.toefl_ibt_conversion import (
    READING_TO_NEW,
    LISTENING_TO_NEW,
    WRITING_TO_NEW,
    SPEAKING_TO_NEW,
    READING_TO_LEGACY,
    LISTENING_TO_LEGACY,
    WRITING_TO_LEGACY,
    SPEAKING_TO_LEGACY,
    total_legacy_to_new,
)


def _cefr_from_new_score(score: float) -> CEFRLiteral:
    """Map a TOEFL iBT new-scale score (1-6) to a CEFR level.

    Args:
        score: Overall or section score on the 1-6 scale.

    Returns:
        Corresponding CEFR level string.
    """
    if score >= 6.0:
        return "C2"
    elif score >= 5.0:
        return "C1"
    elif score >= 4.0:
        return "B2"
    elif score >= 3.0:
        return "B1"
    elif score >= 2.0:
        return "A2"
    else:
        return "A1"


def _validate_legacy_section(v: int) -> int:
    if not 0 <= v <= 30:
        raise ValueError(f"Legacy section score must be 0-30, got {v}")
    return v


def _validate_new_section(v: float) -> float:
    if not 1.0 <= v <= 6.0:
        raise ValueError(f"Section score must be 1-6, got {v}")
    if (v * 2) % 1 != 0:
        raise ValueError(f"Section score must be in 0.5 steps, got {v}")
    return v


TOEFLiBTLegacySectionScore = Annotated[int, AfterValidator(_validate_legacy_section)]
"""Legacy TOEFL iBT section score: integer in the range 0-30."""

TOEFLiBTSectionScore = Annotated[float, AfterValidator(_validate_new_section)]
"""New TOEFL iBT section score: float in the range 1-6 in 0.5 increments."""


class TOEFLiBTLegacyScores(BaseModel):
    """Legacy TOEFL iBT section scores (0-30 per section).

    Attributes:
        Reading: Reading section score (0-30).
        Listening: Listening section score (0-30).
        Speaking: Speaking section score (0-30).
        Writing: Writing section score (0-30).
        Overall: Sum of all four section scores (0-120, computed).
    """

    Reading: TOEFLiBTLegacySectionScore
    Listening: TOEFLiBTLegacySectionScore
    Speaking: TOEFLiBTLegacySectionScore
    Writing: TOEFLiBTLegacySectionScore

    @computed_field
    @property
    def Overall(self) -> int:
        """Compute the total score as the sum of all four sections.

        Returns:
            Total score in the range 0-120.
        """
        return self.Reading + self.Listening + self.Speaking + self.Writing


class TOEFLiBTScores(BaseModel):
    """New TOEFL iBT section scores (1-6 per section, 0.5 steps).

    Attributes:
        Reading: Reading section score (1-6).
        Listening: Listening section score (1-6).
        Speaking: Speaking section score (1-6).
        Writing: Writing section score (1-6).
        Overall: Average of all four section scores rounded to nearest 0.5 (computed).
    """

    Reading: TOEFLiBTSectionScore
    Listening: TOEFLiBTSectionScore
    Speaking: TOEFLiBTSectionScore
    Writing: TOEFLiBTSectionScore

    @computed_field
    @property
    def Overall(self) -> float:
        """Compute the overall score as the average of the four sections rounded to 0.5.

        Returns:
            Overall score in the range 1-6 in 0.5 steps.
        """
        return (
            round(
                (self.Reading + self.Listening + self.Speaking + self.Writing) / 4 * 2
            )
            / 2
        )


class TOEFLiBTLegacy(EnglishLanguageProficiencyCertificate):
    """TOEFL iBT exam record using the pre-2026 0-120 scoring scale.

    Attributes:
        AwardingInstitution: Issuing body; defaults to ``"ETS"``.
        Scores: Section scores on the legacy 0-30 scale.
        CEFRLevel: CEFR level derived via the ETS total-score conversion table (computed).
    """

    AwardingInstitution: str = "ETS"
    Scores: TOEFLiBTLegacyScores

    @computed_field
    @property
    def CEFRLevel(self) -> CEFRLiteral:
        """Derive the CEFR level from the legacy total score.

        Converts the total (0-120) to the new 1-6 scale via the ETS threshold
        table, then maps that to a CEFR level.

        Returns:
            CEFR level string.
        """
        return _cefr_from_new_score(total_legacy_to_new(self.Scores.Overall))

    def to_new(self) -> TOEFLiBT:
        """Convert this record to the new 1-6 scoring scale.

        Each section is converted independently using the official ETS
        per-section lookup tables.

        Returns:
            A new :class:`TOEFLiBT` instance with equivalent scores on the 1-6 scale.
        """
        return TOEFLiBT(
            DateTaken=self.DateTaken,
            Link=self.Link,
            AwardingInstitution=self.AwardingInstitution,
            Scores=TOEFLiBTScores(
                Reading=READING_TO_NEW[self.Scores.Reading],
                Listening=LISTENING_TO_NEW[self.Scores.Listening],
                Speaking=SPEAKING_TO_NEW[self.Scores.Speaking],
                Writing=WRITING_TO_NEW[self.Scores.Writing],
            ),
        )


class TOEFLiBT(EnglishLanguageProficiencyCertificate):
    """TOEFL iBT exam record using the 2026+ 1-6 scoring scale.

    Attributes:
        AwardingInstitution: Issuing body; defaults to ``"ETS"``.
        Scores: Section scores on the new 1-6 scale.
        CEFRLevel: CEFR level derived directly from the overall score (computed).
    """

    AwardingInstitution: str = "ETS"
    Scores: TOEFLiBTScores

    @computed_field
    @property
    def CEFRLevel(self) -> CEFRLiteral:
        """Derive the CEFR level from the new-scale overall score.

        Returns:
            CEFR level string.
        """
        return _cefr_from_new_score(self.Scores.Overall)

    def to_legacy(self) -> TOEFLiBTLegacy:
        """Convert this record to the legacy 0-30 scoring scale.

        Each section is converted independently using the reverse of the ETS
        per-section lookup tables.  Because multiple legacy values map to the
        same new value, the returned section scores are the **highest** legacy
        value that maps to each new score — not necessarily the original values.

        Returns:
            A new :class:`TOEFLiBTLegacy` instance with approximate legacy scores.
        """
        return TOEFLiBTLegacy(
            DateTaken=self.DateTaken,
            Link=self.Link,
            AwardingInstitution=self.AwardingInstitution,
            Scores=TOEFLiBTLegacyScores(
                Reading=READING_TO_LEGACY[self.Scores.Reading],
                Listening=LISTENING_TO_LEGACY[self.Scores.Listening],
                Speaking=SPEAKING_TO_LEGACY[self.Scores.Speaking],
                Writing=WRITING_TO_LEGACY[self.Scores.Writing],
            ),
        )
