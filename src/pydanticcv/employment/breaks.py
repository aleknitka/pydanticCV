"""Models for deliberate gaps and date intervals in the employment timeline.

Contents:
    DateRange: A closed date interval [Start, End].
    EmploymentBreak: A recorded break between employment records.
"""

__all__ = ["DateRange", "EmploymentBreak"]

from datetime import date
from pydantic import BaseModel, model_validator
from pydanticcv.utils.date import PastDate
from pydanticcv.employment.types import BreakReason


class DateRange(BaseModel):
    """A closed date interval from Start to End (inclusive).

    Used to represent uncovered gaps in an employment timeline.

    Attributes:
        Start: First day of the interval.
        End: Last day of the interval.
    """

    Start: date
    End: date


class EmploymentBreak(BaseModel):
    """A deliberate, recorded gap between employment records.

    Neither Reason nor Description is required — the break may be noted
    without explaining why it occurred.  EndDate of None means the break
    is ongoing (rare but valid, e.g. an open-ended sabbatical).

    Attributes:
        StartDate: First day of the break. Must not be in the future.
        EndDate: Last day of the break, or None if the break is ongoing.
        Reason: Category describing the nature of the break. Optional.
        Description: Free-text elaboration on the break. Optional.
    """

    StartDate: PastDate
    EndDate: PastDate | None = None
    Reason: BreakReason | None = None
    Description: str | None = None

    @model_validator(mode="after")
    def _check_date_order(self) -> "EmploymentBreak":
        """Validate that EndDate is strictly after StartDate when set.

        Returns:
            The validated model instance.

        Raises:
            ValueError: If EndDate is set and is not after StartDate.
        """
        if self.EndDate is not None and self.EndDate <= self.StartDate:
            raise ValueError(
                f"EndDate ({self.EndDate}) must be after StartDate ({self.StartDate})"
            )
        return self
