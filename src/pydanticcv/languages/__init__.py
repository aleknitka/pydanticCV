"""Language proficiency models for structured CV data.

Provides models for recording language abilities including self-declared CEFR
levels, native languages, and validated exam certificates.

Contents:
    IELTS: International English Language Testing System exam record.
    SelfReportedCEFR: Self-assessed CEFR proficiency level.
    NativeLanguage: A language declared as native or mother tongue.
"""

__all__ = [
    "IELTS",
    "SelfReportedCEFR",
    "NativeLanguage",
]

from pydanticcv.languages.certificates.eng.ielts import IELTS
from pydanticcv.languages.self_reported import SelfReportedCEFR, NativeLanguage
