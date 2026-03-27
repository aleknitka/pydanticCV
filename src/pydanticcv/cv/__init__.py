"""CV schema subpackage.

Provides the top-level CV model and all supporting personal information models.

Contents:
    CV: Root model for a complete CV/resume.
    PersonalInfo: Personal information section.
    Name: Structured name model.
    ContactInfo: Contact details model.
"""

__all__ = ["CV", "PersonalInfo", "Name", "ContactInfo"]

from pydanticcv.cv.cv import CV
from pydanticcv.cv.personal_info import PersonalInfo, Name, ContactInfo
