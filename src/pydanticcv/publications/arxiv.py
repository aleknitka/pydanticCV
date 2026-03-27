"""arXiv preprint publication model.

Contents:
    ArxivIDStr: Annotated str constrained to valid arXiv identifier formats.
    ArxivCategory: Annotated str constrained to the arXiv category tag format.
    ArxivPreprint: Publication record for an arXiv preprint.
"""

__all__ = ["ArxivIDStr", "ArxivCategory", "ArxivPreprint"]

from typing import Annotated

from pydantic import StringConstraints, model_validator
from pydantic.functional_validators import AfterValidator

from pydanticcv.publications.base import Publication
from pydanticcv.utils.date import PastDate


def _validate_version(v: int) -> int:
    """Reject version numbers less than 1.

    Args:
        v: The candidate version integer.

    Returns:
        The validated version number.

    Raises:
        ValueError: If ``v`` is less than 1.
    """
    if v < 1:
        raise ValueError(f"Version must be at least 1, got {v}")
    return v


# New format (April 2007+): YYMM.NNNNN[vN] or YYMM.NNNNNN[vN]
# Old format (pre-2007):    archive[.sub]/YYMMNNN[vN]
_ARXIV_ID_PATTERN = (
    r"^("
    r"\d{4}\.\d{4,5}(v\d+)?"  # new: 1706.03762, 2301.00234v2
    r"|"
    r"[a-z][a-z\-]*(\.[A-Za-z][A-Za-z\-]*)?/\d{7}(v\d+)?"  # old: hep-th/9711200
    r")$"
)

ArxivIDStr = Annotated[str, StringConstraints(pattern=_ARXIV_ID_PATTERN)]
"""str constrained to a valid arXiv identifier.

Accepts both identifier formats:

* **New** (April 2007+): ``YYMM.NNNNN[vN]`` — e.g. ``1706.03762``, ``2301.00234v2``.
* **Old** (pre-2007): ``archive[.sub]/YYMMNNN[vN]`` — e.g. ``hep-th/9711200``.
"""

ArxivCategory = Annotated[
    str,
    StringConstraints(pattern=r"^[a-z][a-z\-]*(\.[A-Za-z][A-Za-z\-]*)?$"),
]
"""str constrained to an arXiv category tag.

Examples: ``cs.LG``, ``math.CO``, ``cond-mat.mes-hall``, ``hep-th``.
"""


class ArxivPreprint(Publication):
    """Publication record for an arXiv preprint.

    Inherits all fields from :class:`~pydanticcv.publications.base.Publication`.

    Attributes:
        ArxivID: arXiv identifier in new (``YYMM.NNNNN``) or old
            (``archive/YYMMNNN``) format, with an optional version suffix.
        Categories: Ordered list of arXiv subject-area tags; must contain at
            least one entry. The first entry is the primary category.
        Version: Submission version number, starting at 1.
        Submitted: Date the initial version was submitted to arXiv.
    """

    ArxivID: ArxivIDStr
    Categories: list[ArxivCategory]
    Version: Annotated[int, AfterValidator(_validate_version)] = 1
    Submitted: PastDate

    @model_validator(mode="after")
    def check_categories_non_empty(self) -> "ArxivPreprint":
        """Ensure at least one category is provided.

        Returns:
            The validated model instance.

        Raises:
            ValueError: If ``Categories`` is an empty list.
        """
        if not self.Categories:
            raise ValueError("Categories must contain at least one entry")
        return self
