"""Project showcase Pydantic models.

Exposes the public project types used throughout pydanticCV.  Import from this
package rather than from the individual sub-modules.

Contents:
    ProjectStatus: Enum of lifecycle states a project can be in.
    Project: Model representing a single showcased project.
"""

__all__ = ["ProjectStatus", "Project"]

from pydanticcv.projects.project import ProjectStatus, Project
