"""
Objects related to language proficiency, self declared and/or validated with certifaicates
"""

__all__ = ["IELTS", "SelfReportedCEFR"]

from pydanticcv.languages.certificates.eng.ielts import IELTS
from pydanticcv.languages.self_reported import SelfReportedCEFR
