"""HSK (汉语水平考试) Chinese proficiency exam Pydantic models.

Models the HSK 3.0 exam record including section scores, level validation,
and automatic CEFR level derivation. HSK 3.0 launched in 2021 with 6 levels
(HSK 1-6), each testing listening, reading, and writing skills.

Note: The CEFR mapping for HSK is preliminary as no official mapping has
been published by Hanban/Chinese Testing International.

Contents:
    HSKLevel: Literal type for HSK levels 1-6.
    HSKSectionScores: Section scores with validation per level.
    HSK: Full exam record with CEFR computation.
"""

__all__ = ["HSK", "HSKLevel", "HSKSectionScores"]

from typing import Literal

from pydantic import BaseModel, computed_field, model_validator, field_validator
from pydanticcv.languages.certificates.base import CEFRLiteral
from pydanticcv.languages.certificates.zho.base import (
    ChineseLanguageProficiencyCertificate,
)
from pydanticcv.utils.date import PastDate


# HSK 3.0 score ranges per level
# Levels 1-2: Listening + Reading only (100 points each, total 200)
# Levels 3-6: Listening + Reading + Writing (100 points each, total 300)
_HSK_SCORE_RANGES = {
    1: {"Listening": (0, 100), "Reading": (0, 100)},
    2: {"Listening": (0, 100), "Reading": (0, 100)},
    3: {"Listening": (0, 100), "Reading": (0, 100), "Writing": (0, 100)},
    4: {"Listening": (0, 100), "Reading": (0, 100), "Writing": (0, 100)},
    5: {"Listening": (0, 100), "Reading": (0, 100), "Writing": (0, 100)},
    6: {"Listening": (0, 100), "Reading": (0, 100), "Writing": (0, 100)},
}

_HSK_PASS_SCORES = {
    1: 120,
    2: 120,
    3: 180,
    4: 180,
    5: 180,
    6: 180,
}

# CEFR mapping from HSK level (preliminary - not officially published)
_HSK_TO_CEFR = {
    1: "A2",
    2: "A2",
    3: "B1",
    4: "B2",
    5: "C1",
    6: "C1",
}

HSKLevel = Literal[1, 2, 3, 4, 5, 6]
"""HSK exam level: integers 1-6, where 1 is beginner and 6 is advanced."""


class HSKSectionScores(BaseModel):
    """HSK section scores with validation per level.

    Validates that the provided scores are within the acceptable range
    for the specified HSK level. HSK 1-2 have only listening and reading
    sections, while HSK 3-6 include writing.

    Attributes:
        Listening: Listening section score (0-100).
        Reading: Reading section score (0-100).
        Writing: Writing section score (0-100). Required for HSK 3-6, not
            allowed for HSK 1-2.
    """

    Listening: int
    Reading: int
    Writing: int | None = None

    @field_validator("Listening", "Reading", "Writing")
    @classmethod
    def check_score_range(cls, v: int | None, info) -> int | None:
        """Validate that scores are within 0-100 range."""
        if v is not None and not 0 <= v <= 100:
            raise ValueError(f"{info.field_name} must be between 0 and 100, got {v}")
        return v


class HSK(ChineseLanguageProficiencyCertificate):
    """HSK exam record with scores, date, and derived CEFR level.

    Validates section scores based on the HSK level and computes the
    CEFR level using the preliminary mapping: HSK1-2→A2, HSK3→B1,
    HSK4→B2, HSK5-6→C1.

    Attributes:
        Level: HSK exam level (1-6).
        Scores: Section scores (Listening, Reading, optional Writing).
        DateTaken: Date the exam was taken (must not be in the future).
        Link: URL to the official score report.
        CEFRLevel: CEFR level derived from HSK level (computed).
    """

    Level: HSKLevel
    Scores: HSKSectionScores
    DateTaken: PastDate

    @model_validator(mode="after")
    def check_level_scores_consistency(self) -> "HSK":
        """Validate that section scores match the HSK level requirements.

        HSK levels 1-2 should not have a Writing section, while levels 3-6
        must have a Writing section.

        Returns:
            The validated model instance.

        Raises:
            ValueError: If Writing section is present for HSK 1-2 or
                missing for HSK 3-6.
        """
        level = self.Level
        scores = self.Scores

        # Check Writing section consistency
        if level in (1, 2):
            if scores.Writing is not None:
                raise ValueError(f"HSK level {level} does not have a Writing section")
        elif scores.Writing is None:
            raise ValueError(f"HSK level {level} requires a Writing section score")

        # Validate total score meets pass threshold
        total = scores.Listening + scores.Reading
        if scores.Writing is not None:
            total += scores.Writing

        pass_score = _HSK_PASS_SCORES[level]
        if total < pass_score:
            raise ValueError(
                f"Total score {total} is below passing score {pass_score} "
                f"for HSK level {level}"
            )

        return self

    @computed_field
    @property
    def CEFRLevel(self) -> CEFRLiteral:
        """Derive the CEFR level from the HSK level.

        Note: This mapping is preliminary as no official CEFR mapping
        has been published by Hanban/Chinese Testing International.

        Returns:
            CEFR level string corresponding to the HSK level.
        """
        return _HSK_TO_CEFR[self.Level]
