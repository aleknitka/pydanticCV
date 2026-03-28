"""Language proficiency exam Pydantic models.

Exposes the public exam types used throughout pydanticCV.  Import from this
package rather than from the individual sub-modules so that the internal
structure can change without affecting consumers.

Contents:
    IELTS: International English Language Testing System model.
    TOEFLiBT: TOEFL iBT model (2026+ 1-6 scale).
    TOEFLiBTLegacy: TOEFL iBT model (pre-2026, 0-120 scale).
    TOEFLITP: TOEFL ITP (Institutional Testing Program) model.
    DELF: Diplôme d'Études en Langue Française model (A1–B2).
    DALF: Diplôme Approfondi de Langue Française model (C1–C2).
    TCF: Test de Connaissance du Français model (A1–C2).
"""

__all__ = [
    "IELTS",
    "TOEFLiBT",
    "TOEFLiBTLegacy",
    "TOEFLITP",
    "DELF",
    "DALF",
    "TCF",
    "LanguageProficiencyCertificate",
]

from pydanticcv.languages.certificates.base import LanguageProficiencyCertificate
from pydanticcv.languages.certificates.eng.ielts import IELTS
from pydanticcv.languages.certificates.eng.toefl_ibt import TOEFLiBT, TOEFLiBTLegacy
from pydanticcv.languages.certificates.eng.toefl_itp import TOEFLITP
from pydanticcv.languages.certificates.fra.delf_dalf import DALF, DELF
from pydanticcv.languages.certificates.fra.tcf import TCF
