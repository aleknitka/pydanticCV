"""Professional reference model for CV entries.

Models a person who can vouch for the CV owner in a professional or academic
context.  Captures contact details and the nature of the relationship.

Contents:
    RelationshipType: StrEnum of how the reference knows the CV owner.
    Reference: Full reference record with optional contact details.
"""

__all__ = ["RelationshipType", "Reference"]

from enum import StrEnum
from typing import Annotated, Optional

from pydantic import AnyUrl, BaseModel, Field, StringConstraints


PhoneNumber = Annotated[str, StringConstraints(pattern=r"^\+?[\d\s\-(). ]{7,20}$")]
EmailAddress = Annotated[str, StringConstraints(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")]


class RelationshipType(StrEnum):
    """How the reference knows the CV owner.

    Attributes:
        Manager: The reference was a direct or indirect manager.
        Colleague: The reference was a peer or co-worker.
        Professor: The reference was an academic supervisor or lecturer.
        Mentor: The reference acted in a mentoring capacity.
        Client: The reference was a client or customer.
        Other: Any other professional relationship.
    """

    Manager = "Manager"
    Colleague = "Colleague"
    Professor = "Professor"
    Mentor = "Mentor"
    Client = "Client"
    Other = "Other"


class Reference(BaseModel):
    """A professional or academic reference contact.

    Attributes:
        Name: Full name of the reference person.
        Title: Their current job title or academic position.
        Organization: Employer, institution, or company they are associated with.
        Relationship: How this person knows the CV owner.
        Email: Contact e-mail address in user@domain.tld format. Optional.
        Phone: Contact phone number in any common format. Optional.
        LinkedInURL: URL to their LinkedIn profile. Optional.
    """

    Name: str = Field(..., min_length=1)
    Title: str = Field(..., min_length=1)
    Organization: str = Field(..., min_length=1)
    Relationship: RelationshipType
    Email: Optional[EmailAddress] = None
    Phone: Optional[PhoneNumber] = None
    LinkedInURL: Optional[AnyUrl] = None
