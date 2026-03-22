"""Different frameworks for language proficiency"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import StrEnum

from pydanticcv.languages._exams_types import IELTS


class CEFRLevel(StrEnum):
    "Common European Framework of Reference for Languages"

    a1 = "A1"
    a2 = "A2"
    b1 = "B1"
    b2 = "B2"
    c1 = "C1"
    c2 = "C2"


class CEFR(BaseModel):
    "Common European Framework of Reference for Languages proficiency record"

    level: CEFRLevel = Field(...)
    evidence: Optional[IELTS] = None
