"""Employment classification enumerations.

Contents:
    EmploymentType: Classification of the contractual/work arrangement.
    BreakReason: Common reasons for a voluntary gap in employment.
"""

__all__ = ["EmploymentType", "BreakReason"]

from enum import StrEnum


class EmploymentType(StrEnum):
    """Classification of the contractual or work arrangement for a position.

    Members:
        EMPLOYEE: Standard employment contract (full-time or part-time).
        B2B: Business-to-business contract; the person operates through their
            own legal entity and invoices the client. Common in PL, CZ, etc.
        SELF_EMPLOYED: Sole trader or freelancer without a separate legal entity.
        FREELANCE: Project-based work delivered to multiple clients with no
            fixed employer relationship.
        INTERNSHIP: Fixed-term placement, typically for students or graduates.
        APPRENTICESHIP: Formal training contract combining work and study.
        VOLUNTEER: Unpaid voluntary work.
        OTHER: Any arrangement not covered by the above categories.
    """

    EMPLOYEE = "Employee"
    B2B = "B2B"
    SELF_EMPLOYED = "Self-employed"
    FREELANCE = "Freelance"
    INTERNSHIP = "Internship"
    APPRENTICESHIP = "Apprenticeship"
    VOLUNTEER = "Volunteer"
    OTHER = "Other"


class BreakReason(StrEnum):
    """Common reasons for a deliberate gap between employment records.

    All values are optional — a break may be recorded without specifying
    a reason.

    Members:
        PARENTAL_LEAVE: Maternity, paternity, or adoption leave.
        SABBATICAL: Extended planned leave for personal development or rest.
        EDUCATION: Full-time study, course, or retraining.
        TRAVEL: Extended personal travel.
        ILLNESS: Medical leave or recovery.
        CAREGIVING: Caring for a family member or dependent.
        JOB_SEARCH: Period of active job hunting between roles.
        PERSONAL: Personal circumstances not listed elsewhere.
        OTHER: Any reason not covered by the above categories.
    """

    PARENTAL_LEAVE = "Parental leave"
    SABBATICAL = "Sabbatical"
    EDUCATION = "Education"
    TRAVEL = "Travel"
    ILLNESS = "Illness"
    CAREGIVING = "Caregiving"
    JOB_SEARCH = "Job search"
    PERSONAL = "Personal"
    OTHER = "Other"
