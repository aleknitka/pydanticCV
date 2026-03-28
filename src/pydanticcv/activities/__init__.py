"""Activities domain — volunteering and related CV entries.

Contents:
    VolunteeringArea: StrEnum of volunteering domain categories.
    VolunteeringActivity: Pydantic model for a single volunteering activity.
"""

__all__ = ["VolunteeringArea", "VolunteeringActivity"]

from pydanticcv.activities.volunteering import VolunteeringActivity, VolunteeringArea
