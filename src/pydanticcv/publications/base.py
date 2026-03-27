"""Base model and shared types for academic publications.

Contents:
    PublicationYear: Annotated int constrained to non-future years.
    DOIStr: Annotated str constrained to the standard DOI prefix format.
    Publication: Base model for all publication records.
"""

__all__ = ["PublicationYear", "DOIStr", "Publication"]

from datetime import date
from typing import Annotated

from pydantic import AnyUrl, BaseModel, StringConstraints, model_validator
from pydantic.functional_validators import AfterValidator


def _validate_publication_year(v: int) -> int:
    """Reject years in the future.

    Args:
        v: The candidate year integer.

    Returns:
        The validated year.

    Raises:
        ValueError: If ``v`` exceeds the current calendar year.
    """
    current_year = date.today().year
    if v > current_year:
        raise ValueError(
            f"Publication year {v} cannot be in the future (current year: {current_year})"
        )
    return v


PublicationYear = Annotated[int, AfterValidator(_validate_publication_year)]
"""int constrained to years not exceeding the current calendar year."""

DOIStr = Annotated[str, StringConstraints(pattern=r"^10\.\d{4,}/.+$")]
"""str constrained to the standard DOI format (prefix ``10.NNNN/...``).

Examples: ``10.1038/nature12345``, ``10.48550/arXiv.1706.03762``.
"""


class Publication(BaseModel):
    """Base record for an academic publication.

    All concrete publication types (journal articles, preprints, etc.)
    inherit from this model.

    Attributes:
        Title: Full title of the work.
        Authors: Ordered list of author names; must contain at least one entry.
        Year: Calendar year of publication; must not be in the future.
        Abstract: Optional abstract or summary text.
        DOI: Optional Digital Object Identifier in ``10.NNNN/...`` format.
        Link: Optional URL pointing to the publication.
    """

    Title: str
    Authors: list[str]
    Year: PublicationYear
    Abstract: str | None = None
    DOI: DOIStr | None = None
    Link: AnyUrl | None = None

    @model_validator(mode="after")
    def check_authors_non_empty(self) -> "Publication":
        """Ensure at least one author is provided.

        Returns:
            The validated model instance.

        Raises:
            ValueError: If ``Authors`` is an empty list.
        """
        if not self.Authors:
            raise ValueError("Authors must contain at least one entry")
        return self
