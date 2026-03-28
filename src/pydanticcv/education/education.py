"""Placeholder education record model.

Contents:
    EducationRecord: Stub model for academic background.
"""

__all__ = ["EducationRecord"]

from pydantic import BaseModel


class EducationRecord(BaseModel):
    """Placeholder for a single education entry.

    TODO: Implement fully with:
        - Institution: str
        - Degree: str
        - FieldOfStudy: str
        - StartDate: PastDate
        - EndDate: PastDate | None = None
        - Grade: str | None = None
        - Description: str | None = None
    """

    pass
