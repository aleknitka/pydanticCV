"""Language proficiency exam Pydantic models.

Exposes the public exam types used throughout pydanticCV.  Import from this
package rather than from the individual sub-modules so that the internal
structure can change without affecting consumers.

Contents:
    IELTS: International English Language Testing System model.
    TOEFLiBT: TOEFL iBT model (2026+ 1-6 scale).
    TOEFLiBTLegacy: TOEFL iBT model (pre-2026, 0-120 scale).
    TOEFLITP: TOEFL ITP (Institutional Testing Program) model.
"""

__all__ = ["IELTS", "TOEFLiBT", "TOEFLiBTLegacy", "TOEFLITP"]

from pydanticcv.languages.certificates.eng.ielts import IELTS
from pydanticcv.languages.certificates.eng.toefl_ibt import TOEFLiBT, TOEFLiBTLegacy
from pydanticcv.languages.certificates.eng.toefl_itp import TOEFLITP
