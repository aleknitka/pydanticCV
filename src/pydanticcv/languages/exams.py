"""Structures for the most common language proficiency exams"""

from pydantic import BaseModel, Field
from typing import Optional
from pydanticcv.utils.date import PastDate
from pydanticcv.languages.certificates.eng.ielts import IELTSScores


class IELTS(BaseModel):
    "International English Language Testing System"

    Scores: IELTSScores = Field(..., default_factory=IELTSScores)
    DateTaken: PastDate
    TestCentre: Optional[str]
