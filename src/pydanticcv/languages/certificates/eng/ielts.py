"""IELTS (International English Language Testing System) Pydantic models.

Models the IELTS exam record including per-skill band scores, overall score
validation, exam type, test centre, and an automatically derived CEFR level.

Band scores range from 0 to 9 in 0.5 steps.  The overall band score must
equal the average of the four section scores rounded to the nearest 0.5.

Contents:
    IELTSBandScore: Annotated float constrained to valid IELTS band scores.
    IELTSTestCentreCode: Annotated str constrained to the ISO-country + digits format.
    IELTSType: Literal type for Academic or General Training exam variants.
    IELTSScores: Section and overall band scores with consistency validation.
    IELTS: Full IELTS exam record with computed CEFR level.
"""

__all__ = ["IELTSBandScore", "IELTSTestCentreCode", "IELTSType", "IELTSScores", "IELTS"]

from typing import Annotated, Literal
from pydantic import BaseModel, StringConstraints, computed_field, model_validator
from pydantic.functional_validators import AfterValidator
from pydanticcv.utils.date import PastDate
from pydanticcv.languages.certificates.eng.base import (
    EnglishLanguageProficiencyCertificate,
)


def _validate_band_score(v: float) -> float:
    if not 0 <= v <= 9:
        raise ValueError(f"Band score must be between 0 and 9, got {v}")
    if (v * 2) % 1 != 0:
        raise ValueError(f"Band score must be in 0.5 steps, got {v}")
    return v


IELTSBandScore = Annotated[float, AfterValidator(_validate_band_score)]
"""IELTS band score: a float in the range 0-9 in 0.5 increments."""

IELTSTestCentreCode = Annotated[str, StringConstraints(pattern=r"^[A-Z]{2}\d+$")]
"""IELTS test centre code: two uppercase ISO country letters followed by digits (e.g. GB123)."""

IELTSType = Literal["Academic", "General Training"]
"""IELTS exam variant."""


class IELTSScores(BaseModel):
    """Per-skill and overall IELTS band scores.

    Attributes:
        Listening: Band score for the Listening section (0-9, 0.5 steps).
        Reading: Band score for the Reading section (0-9, 0.5 steps).
        Writing: Band score for the Writing section (0-9, 0.5 steps).
        Speaking: Band score for the Speaking section (0-9, 0.5 steps).
        Overall: Overall band score; must equal the average of the four
            section scores rounded to the nearest 0.5.
    """

    Listening: IELTSBandScore
    Reading: IELTSBandScore
    Writing: IELTSBandScore
    Speaking: IELTSBandScore
    Overall: IELTSBandScore

    @model_validator(mode="after")
    def check_overall_is_consistent(self) -> "IELTSScores":
        """Validate that Overall equals the rounded average of the four sections.

        Returns:
            The validated model instance.

        Raises:
            ValueError: If Overall does not match the expected rounded average.
        """
        expected = (
            round(
                (self.Listening + self.Reading + self.Writing + self.Speaking) / 4 * 2
            )
            / 2
        )
        if self.Overall != expected:
            raise ValueError(
                f"Overall band score {self.Overall} does not match the average of "
                f"the four components ({expected})"
            )
        return self


class IELTS(EnglishLanguageProficiencyCertificate):
    """IELTS exam record with scores, metadata, and derived CEFR level.

    Attributes:
        Scores: Section and overall band scores.
        DateTaken: Date the exam was sat (inherited; must not be in the future).
        ExamType: Academic or General Training variant.
        TestCentreCode: Optional test centre identifier (e.g. GB123).
        CEFRLevel: CEFR level derived from the overall band score (computed).
    """

    Scores: IELTSScores
    DateTaken: PastDate
    ExamType: IELTSType
    TestCentreCode: IELTSTestCentreCode | None = None

    @computed_field
    @property
    def CEFRLevel(self) -> Literal["A1/A2", "B1", "B2", "C1", "C2"]:
        """Derive the CEFR level from the overall IELTS band score.

        Returns:
            CEFR level string corresponding to the overall band score.
        """
        score = self.Scores.Overall
        if score >= 8.5:
            return "C2"
        elif score >= 7.0:
            return "C1"
        elif score >= 5.5:
            return "B2"
        elif score >= 4.5:
            return "B1"
        else:
            return "A1/A2"
