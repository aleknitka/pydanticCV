"""Employment history models for structured CV data.

Provides models for recording work experience including employee, B2B,
self-employed, and freelance arrangements, deliberate breaks, and automatic
gap detection across the full employment timeline.

Contents:
    EmploymentType: Contractual/work arrangement classification.
    BreakReason: Common reasons for a gap between employment records.
    EmploymentRecord: A single continuous period of work in one role.
    DateRange: A closed date interval [Start, End].
    EmploymentBreak: A deliberate recorded gap in the timeline.
    EmploymentHistory: Full timeline container with gap detection.
"""

__all__ = [
    "EmploymentType",
    "BreakReason",
    "EmploymentRecord",
    "DateRange",
    "EmploymentBreak",
    "EmploymentHistory",
]

from pydanticcv.employment.types import EmploymentType, BreakReason
from pydanticcv.employment.record import EmploymentRecord
from pydanticcv.employment.breaks import DateRange, EmploymentBreak
from pydanticcv.employment.history import EmploymentHistory
