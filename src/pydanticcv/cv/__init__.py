"""CV schema subpackage.
 
Provides the top-level CV model and all supporting personal information models.

Contents:
    CV: Root model for a complete CV/resume.
    PersonalInfo: Personal information section.
    Name: Structured name model.
    ContactInfo: Contact details model.
    EmploymentHistory: Full employment timeline with gap detection.
    Skill: A single professional skill entry.
    Project: A portfolio project entry.
    Publication: Base model for academic publications.
    VolunteeringActivity: A single volunteering activity.
    Reference: A professional reference.
    RelationshipType: How a reference knows the CV owner.
"""
 
__all__ = [
    "CV",
    "PersonalInfo",
    "Name",
    "ContactInfo",
    "EmploymentHistory",
    "Skill",
    "Project",
    "Publication",
    "VolunteeringActivity",
    "Reference",
    "RelationshipType",
]
 
from pydanticcv.cv.cv import CV
from pydanticcv.cv.personal_info import PersonalInfo, Name, ContactInfo
from pydanticcv.employment import EmploymentHistory
from pydanticcv.projects import Project
from pydanticcv.publications import Publication
from pydanticcv.skills import Skill
from pydanticcv.activities import VolunteeringActivity
from pydanticcv.references import Reference, RelationshipType
