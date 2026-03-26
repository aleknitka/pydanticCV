"""Core skill models for CV/resume data.

Contents:
    SkillType: StrEnum of high-level skill categories.
    Skill: Pydantic model representing a single skill entry.
"""

__all__ = ["SkillType", "Skill"]

from enum import StrEnum

from pydantic import BaseModel

from pydanticcv.skills.levels import SkillProficiencyLevel


class SkillType(StrEnum):
    """High-level categories for classifying a skill.

    Attributes:
        Technical: Hard technical skills (e.g. programming languages, protocols).
        Soft: Interpersonal or organisational skills (e.g. leadership, communication).
        Tool: Specific software tools or platforms (e.g. Git, Docker).
        Framework: Libraries or frameworks (e.g. Django, React).
        Domain: Industry or domain knowledge (e.g. finance, healthcare).
        Other: Skills that do not fit the above categories.
    """

    Technical = "Technical"
    Soft = "Soft"
    Tool = "Tool"
    Framework = "Framework"
    Domain = "Domain"
    Other = "Other"


class Skill(BaseModel):
    """A single skill entry on a CV.

    Attributes:
        Name: Human-readable skill name (e.g. "Python", "Public Speaking").
        Type: High-level category of the skill.
        Level: Self-assessed or verified proficiency level.
        YearsExperience: Optional years of active experience with this skill.
    """

    Name: str
    Type: SkillType
    Level: SkillProficiencyLevel
    YearsExperience: float | None = None
