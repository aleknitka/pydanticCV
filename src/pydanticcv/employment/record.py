"""Employment record model for a single role at a single employer.

Multiple roles held at the same employer are represented as separate
EmploymentRecord instances sharing the same EmployerName.

Contents:
    EmploymentRecord: A single continuous period of work in one role.
"""

__all__ = ["EmploymentRecord"]

from pydantic import BaseModel, computed_field, model_validator
from pydanticcv.utils.date import PastDate
from pydanticcv.employment.types import EmploymentType


class EmploymentRecord(BaseModel):
    """A single continuous period of employment in one role.

    Dates are validated with PastDate, which accepts multiple string formats
    and rejects future dates. EndDate of None means the position is current.

    For B2B and Freelance arrangements the Clients field records the names
    of client organisations engaged during this period.

    Attributes:
        EmployerName: Name of the employer, or the person's own legal entity
            for B2B and Self-employed arrangements.
        Role: Job title or position held.
        EmploymentType: Contractual or work arrangement classification.
        StartDate: Date the role began. Must not be in the future.
        EndDate: Date the role ended, or None if still current.
        Location: City, country, or descriptive location string. Optional.
        Remote: True if fully remote, False if fully on-site, None if hybrid
            or unspecified. Optional.
        Description: Free-prose summary of the role and its context. Optional.
        Responsibilities: Recurring duties and tasks performed in the role,
            suitable for a bullet-point list. Optional.
        Achievements: Notable accomplishments and delivered results,
            suitable for a bullet-point list. Optional.
        Clients: Names of client organisations, relevant for B2B and
            Freelance arrangements. Optional.
        IsCurrent: True when EndDate is None (computed).
    """

    EmployerName: str
    Role: str
    EmploymentType: EmploymentType
    StartDate: PastDate
    EndDate: PastDate | None = None
    Location: str | None = None
    Remote: bool | None = None
    Description: str | None = None
    Responsibilities: list[str] | None = None
    Achievements: list[str] | None = None
    Clients: list[str] | None = None

    @model_validator(mode="after")
    def _check_date_order(self) -> "EmploymentRecord":
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

    @computed_field
    @property
    def IsCurrent(self) -> bool:
        """True when this is an ongoing position (EndDate is None).

        Returns:
            True if EndDate is None, False otherwise.
        """
        return self.EndDate is None
