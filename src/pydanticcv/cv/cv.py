"""Top-level CV model.

Contents:
    CV: Root Pydantic model representing a complete CV/resume.
"""

__all__ = ["CV"]

from pydantic import BaseModel, Field

from pydanticcv.cv.personal_info import PersonalInfo
from pydanticcv.education import EducationRecord
from pydanticcv.employment import EmploymentHistory
from pydanticcv.languages import NativeLanguage, SelfReportedCEFR
from pydanticcv.languages.certificates import LanguageProficiencyCertificate
from pydanticcv.projects import Project
from pydanticcv.publications import Publication
from pydanticcv.skills import Skill
from pydanticcv.activities import VolunteeringActivity
from pydanticcv.references import Reference

_PersonalInfo = PersonalInfo
_EducationRecord = EducationRecord
_EmploymentHistory = EmploymentHistory
_Skill = Skill
_Project = Project
_Publication = Publication
_VolunteeringActivity = VolunteeringActivity
_Reference = Reference


class CV(BaseModel):
    """A complete CV/resume.

    Attributes:
        PersonalInfo: Personal information section. Required.
        EmploymentHistory: Full employment timeline with gap detection. Optional.
        Education: List of education entries. Defaults to empty list.
        Skills: List of professional skills. Optional.
        NativeLanguages: List of native/mother-tongue languages. Optional.
        SelfReportedLanguages: List of self-assessed CEFR proficiency levels.
            Optional.
        LanguageCertificates: List of validated exam certificates (IELTS, TOEFL,
            DELF, etc.). Optional.
        Publications: List of academic publications. Optional.
        Projects: List of portfolio projects. Optional.
        Volunteering: List of volunteering activities. Optional.
        References: List of professional references. Optional.
    """

    PersonalInfo: _PersonalInfo
    EmploymentHistory: _EmploymentHistory | None = None
    Education: list[_EducationRecord] = Field(default_factory=list)
    Skills: list[_Skill] | None = None
    NativeLanguages: list[NativeLanguage] | None = None
    SelfReportedLanguages: list[SelfReportedCEFR] | None = None
    LanguageCertificates: list[LanguageProficiencyCertificate] | None = None
    Publications: list[_Publication] | None = None
    Projects: list[_Project] | None = None
    Volunteering: list[_VolunteeringActivity] | None = None
    References: list[_Reference] | None = None
