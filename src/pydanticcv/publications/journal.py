"""Journal article publication model.

Contents:
    ISSNStr: Annotated str constrained to the ISSN format (NNNN-NNNX).
    JournalArticle: Publication record for a peer-reviewed journal article.
"""

__all__ = ["ISSNStr", "JournalArticle"]

from typing import Annotated

from pydantic import StringConstraints

from pydanticcv.publications.base import Publication


ISSNStr = Annotated[str, StringConstraints(pattern=r"^\d{4}-\d{3}[\dX]$")]
"""str constrained to the standard ISSN format ``NNNN-NNNX``.

The final character may be a digit or the check digit ``X``.

Examples: ``0028-0836`` (Nature print), ``1476-4687`` (Nature online).
"""


class JournalArticle(Publication):
    """Publication record for a peer-reviewed journal article.

    Inherits all fields from :class:`~pydanticcv.publications.base.Publication`.

    Attributes:
        Journal: Full name of the journal.
        Volume: Volume number of the journal issue, if applicable.
        Issue: Issue (number) within the volume, if applicable.
        Pages: Page range or article identifier, e.g. ``"123-145"`` or ``"e12345"``.
        ISSN: Print ISSN of the journal in ``NNNN-NNNX`` format.
        EISSN: Electronic ISSN of the journal in ``NNNN-NNNX`` format.
        Publisher: Name of the publishing organisation.
    """

    Journal: str
    Volume: int | None = None
    Issue: int | None = None
    Pages: str | None = None
    ISSN: ISSNStr | None = None
    EISSN: ISSNStr | None = None
    Publisher: str | None = None
