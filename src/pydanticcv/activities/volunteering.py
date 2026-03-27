"""Volunteering activity model for CV/resume data.

Contents:
    VolunteeringArea: StrEnum of volunteering domain categories.
    VolunteeringActivity: Pydantic model for a single volunteering activity.
"""

__all__ = ["VolunteeringArea", "VolunteeringActivity"]

from datetime import date
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, computed_field, model_validator

from pydanticcv.utils.date import PastDate


class VolunteeringArea(StrEnum):
    """Domain categories for volunteering activities.

    Attributes:
        Education: Teaching, tutoring, literacy programmes.
        Environment: Conservation, sustainability, climate action.
        Health: Medical outreach, mental health, wellbeing.
        Policy: Advocacy, civic engagement, public affairs.
        Community: Local support, neighbourhood, social cohesion.
        Humanitarian: Disaster relief, refugees, international aid.
        Arts: Culture, music, theatre, creative projects.
        AnimalWelfare: Rescue, shelter support, wildlife protection.
        Technology: Open-source, digital inclusion, STEM outreach.
        Sports: Coaching, events, physical activity programmes.
    """

    Education = "Education"
    Environment = "Environment"
    Health = "Health"
    Policy = "Policy"
    Community = "Community"
    Humanitarian = "Humanitarian"
    Arts = "Arts"
    AnimalWelfare = "AnimalWelfare"
    Technology = "Technology"
    Sports = "Sports"


class VolunteeringActivity(BaseModel):
    """A single volunteering activity on a CV.

    Attributes:
        Organisation: Name of the organisation or cause.
        Role: The volunteer's title or position.
        Area: Domain category of the activity.
        StartDate: Date the activity began.
        EndDate: Date the activity ended; ``None`` if still ongoing.
        Description: Free-text description of duties or impact.
        IsOngoing: Computed — ``True`` when ``EndDate`` is ``None``.
    """

    Organisation: str
    Role: str
    Area: VolunteeringArea
    StartDate: PastDate
    EndDate: Optional[PastDate] = None
    Description: str

    @computed_field  # type: ignore[prop-decorator]
    @property
    def IsOngoing(self) -> bool:
        """Whether the activity is still ongoing.

        Returns:
            True if EndDate is None, False otherwise.
        """
        return self.EndDate is None

    @model_validator(mode="after")
    def _validate_date_range(self) -> "VolunteeringActivity":
        """Ensure EndDate is not before StartDate.

        Returns:
            Self if valid.

        Raises:
            ValueError: If EndDate precedes StartDate.
        """
        if self.EndDate is not None and self.EndDate < self.StartDate:
            raise ValueError(
                f"EndDate ({self.EndDate}) cannot be before StartDate ({self.StartDate})."
            )
        return self
