"""Structures for the most common language proficiency exams"""

from pydantic import BaseModel, Field
from typing import Optional
from pydanticcv.utils.date import PastDate
from pydanticcv.languages._exams_types.ielts import IELTS_Scores


class IELTS(BaseModel):
    "International English Language Testing System"

    Scores: IELTS_Scores = Field(..., default_factory=IELTS_Scores)
    DateTaken: PastDate
    TestCentre: Optional[str]
