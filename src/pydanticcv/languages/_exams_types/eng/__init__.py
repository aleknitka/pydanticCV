"""English language proficiency exam Pydantic models.

Re-exports all English exam types so consumers can import from this package
rather than from the individual sub-modules.

Contents:
    IELTS: International English Language Testing System model.
    TOEFLiBT: TOEFL iBT model (2026+ 1-6 scale).
    TOEFLiBTLegacy: TOEFL iBT model (pre-2026, 0-120 scale).
    TOEFLITР: TOEFL ITP (Institutional Testing Program) model.
"""

__all__ = ["IELTS", "TOEFLiBT", "TOEFLiBTLegacy", "TOEFLITP"]

from pydanticcv.languages._exams_types.eng.ielts import IELTS
from pydanticcv.languages._exams_types.eng.toefl_ibt import TOEFLiBT, TOEFLiBTLegacy
from pydanticcv.languages._exams_types.eng.toefl_itp import TOEFLITP
