"""Skill models for CV/resume data.

Provides structured types for representing professional and technical skills.
Skill certifications are exposed separately via `pydanticcv.skills.certificates`.

Contents:
    SkillProficiencyLevel: Ordered proficiency levels (Beginner → Expert).
    SkillType: High-level skill categories (Technical, Soft, Tool, etc.).
    Skill: Pydantic model for a single skill entry.
"""

__all__ = ["SkillProficiencyLevel", "SkillType", "Skill"]

from pydanticcv.skills.levels import SkillProficiencyLevel
from pydanticcv.skills.skill import Skill, SkillType
