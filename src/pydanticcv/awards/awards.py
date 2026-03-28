"""Award model for CV/resume data.

Contents:
    Award: Pydantic model representing a single award or honor.
"""

__all__ = ["Award"]


from pydantic import BaseModel, Field
from pydanticcv.utils.date import PastDate


class Award(BaseModel):
    """A single award or honor on a CV.

    Attributes:
        Title: Name of the award (e.g. ``"Nobel Prize in Physics"``).
        DateReceived: Date the award was received; must not be in the future.
        IssuingOrganization: Organization that granted the award.
        Description: Optional free-text description of the award.
    """

    Title: str = Field(..., min_length=1)
    DateReceived: PastDate
    IssuingOrganization: str = Field(..., min_length=1)
    Description: str | None = None
