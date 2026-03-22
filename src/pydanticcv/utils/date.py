"""Utilities for date and time"""

__all__ = ["PastDate"]
from typing import Annotated
from datetime import date
from pydantic.functional_validators import BeforeValidator

# Tried in order; European (DD/MM/YYYY) takes priority over US (MM/DD/YYYY)
# for ambiguous slash-separated dates.
_DATE_FORMATS = [
    "%Y-%m-%d",  # ISO:      2012-04-23
    "%Y/%m/%d",  # numeric:  2012/04/23
    "%Y.%m.%d",  # dotted:   2023.04.23
    "%d/%m/%Y",  # European: 23/04/2012
    "%m/%d/%Y",  # US:       04/23/2012
    "%d-%m-%Y",  # European: 23-04-2012
    "%m-%d-%Y",  # US:       04-23-2012
    "%d.%m.%Y",  # European: 23.04.2012
]


def _parse_and_validate_date(v: object) -> date:
    if isinstance(v, date):
        parsed = v
    elif isinstance(v, str):
        for fmt in _DATE_FORMATS:
            try:
                parsed = (
                    date.fromisoformat(v)
                    if fmt == "%Y-%m-%d"
                    else __import__("datetime").datetime.strptime(v, fmt).date()
                )
                break
            except ValueError:
                continue
        else:
            raise ValueError(f"Unrecognised date format: {v!r}")
    else:
        raise ValueError(f"Expected a date or string, got {type(v).__name__}")

    if parsed > date.today():
        raise ValueError(f"DateTaken cannot be in the future: {parsed}")
    return parsed


PastDate = Annotated[date, BeforeValidator(_parse_and_validate_date)]
