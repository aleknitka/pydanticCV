"""Top-level CV model.

Contents:
    CV: Root Pydantic model representing a complete CV/resume.
"""

__all__ = ["CV"]

from pydantic import BaseModel

from pydanticcv.cv.personal_info import PersonalInfo

_PersonalInfo = PersonalInfo  # alias avoids field-name shadowing the class in annotations


class CV(BaseModel):
    """A complete CV/resume.

    Attributes:
        PersonalInfo: Personal information section. Required.
    """

    PersonalInfo: _PersonalInfo
