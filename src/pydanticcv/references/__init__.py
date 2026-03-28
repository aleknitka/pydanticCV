"""Professional reference Pydantic models.

Exposes the public reference types used throughout pydanticCV.  Import from
this package rather than from the individual sub-modules.

Contents:
    RelationshipType: Enum of how a reference knows the CV owner.
    Reference: Model representing a single professional reference contact.
"""

__all__ = ["RelationshipType", "Reference"]

from pydanticcv.references.reference import RelationshipType, Reference
