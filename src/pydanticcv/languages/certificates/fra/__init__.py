"""French language proficiency exam Pydantic models.

Re-exports all French exam types so consumers can import from this package
rather than from the individual sub-modules.

Contents:
    DELF: Diplôme d'Études en Langue Française (A1–B2).
    DALF: Diplôme Approfondi de Langue Française (C1–C2).
    TCF: Test de Connaissance du Français (A1–C2, score-based).
"""

__all__ = ["DELF", "DALF", "TCF"]

from pydanticcv.languages.certificates.fra.delf_dalf import DALF, DELF
from pydanticcv.languages.certificates.fra.tcf import TCF
