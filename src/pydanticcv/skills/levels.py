"""Proficiency level definitions for skills.

Contents:
    SkillProficiencyLevel: StrEnum of ordered skill proficiency levels.
"""

__all__ = ["SkillProficiencyLevel"]

from enum import StrEnum


class SkillProficiencyLevel(StrEnum):
    """Ordered skill proficiency levels from least to most experienced.

    Attributes:
        Beginner: Awareness of the skill; little to no practical use.
        Elementary: Basic practical use with guidance.
        Intermediate: Independent use in common scenarios.
        Advanced: Confident, nuanced use across a wide range of situations.
        Expert: Deep mastery; able to teach others or design systems.
    """

    Beginner = "Beginner"
    Elementary = "Elementary"
    Intermediate = "Intermediate"
    Advanced = "Advanced"
    Expert = "Expert"
