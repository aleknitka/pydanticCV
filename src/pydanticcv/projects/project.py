"""Project showcase model for CV/portfolio entries.

Models a single project entry suitable for a GitHub project page, portfolio
site, or structured CV.  Supports optional repository and live URLs,
date ranges, lifecycle status, free-form tags, and a technology stack list.

Contents:
    ProjectStatus: StrEnum of lifecycle states (Active, Completed, Archived, Paused).
    Project: Full project record with optional dates, URLs, tags, and tech stack.
"""

__all__ = ["ProjectStatus", "Project"]

from datetime import date
from enum import StrEnum
from typing import Optional

from pydantic import AnyUrl, BaseModel, Field, model_validator
from pydanticcv.utils.date import PastDate


class ProjectStatus(StrEnum):
    """Lifecycle state of a project.

    Attributes:
        Active: Project is currently being developed.
        Completed: Project has reached its intended goal and is no longer actively developed.
        Archived: Project is no longer maintained and has been archived.
        Paused: Development is temporarily on hold.
    """

    Active = "Active"
    Completed = "Completed"
    Archived = "Archived"
    Paused = "Paused"


class Project(BaseModel):
    """A single showcased project for a CV or portfolio.

    Attributes:
        Name: Human-readable project name.
        Description: Short summary of what the project does and why it exists.
        RepoURL: URL to the source code repository (e.g. GitHub, GitLab). Optional.
        LiveURL: URL to a live demo, hosted app, or project homepage. Optional.
        StartDate: Date the project was started; must not be in the future.
        EndDate: Date the project ended or was archived. Must not be in the future
            and must not be earlier than StartDate. Optional — omit for ongoing work.
        Status: Current lifecycle state of the project.
        Tags: Arbitrary labels for filtering or grouping (e.g. "open-source", "ml").
        Technologies: Ordered list of languages, frameworks, or tools used.
    """

    Name: str = Field(..., min_length=1)
    Description: str = Field(..., min_length=1)
    RepoURL: Optional[AnyUrl] = None
    LiveURL: Optional[AnyUrl] = None
    StartDate: PastDate
    EndDate: Optional[PastDate] = None
    Status: ProjectStatus = ProjectStatus.Active
    Tags: list[str] = Field(default_factory=list)
    Technologies: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def check_end_date_after_start(self) -> "Project":
        """Validate that EndDate is not earlier than StartDate.

        Returns:
            The validated model instance.

        Raises:
            ValueError: If EndDate precedes StartDate.
        """
        if self.EndDate is not None and self.EndDate < self.StartDate:
            raise ValueError(
                f"EndDate ({self.EndDate}) must not be earlier than "
                f"StartDate ({self.StartDate})"
            )
        return self
