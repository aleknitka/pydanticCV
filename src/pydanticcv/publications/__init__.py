"""Academic publication models for structured CV data.

Contents:
    Publication: Base model shared by all publication types.
    PublicationYear: Annotated int constrained to non-future years.
    DOIStr: Annotated str constrained to the standard DOI prefix format.
    JournalArticle: Publication record for a peer-reviewed journal article.
    ISSNStr: Annotated str constrained to the ISSN format.
    ArxivPreprint: Publication record for an arXiv preprint.
    ArxivIDStr: Annotated str constrained to valid arXiv identifier formats.
    ArxivCategory: Annotated str constrained to the arXiv category tag format.
"""

__all__ = [
    "Publication",
    "PublicationYear",
    "DOIStr",
    "JournalArticle",
    "ISSNStr",
    "ArxivPreprint",
    "ArxivIDStr",
    "ArxivCategory",
]

from pydanticcv.publications.arxiv import ArxivCategory, ArxivIDStr, ArxivPreprint
from pydanticcv.publications.base import DOIStr, Publication, PublicationYear
from pydanticcv.publications.journal import ISSNStr, JournalArticle
