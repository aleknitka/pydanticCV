"""Employment history container with automatic gap detection.

Contents:
    EmploymentHistory: Ordered collection of employment records and breaks,
        with a computed Gaps field listing any uncovered date intervals.
"""

__all__ = ["EmploymentHistory"]

from datetime import date
from pydantic import BaseModel, computed_field
from pydanticcv.employment.record import EmploymentRecord
from pydanticcv.employment.breaks import DateRange, EmploymentBreak


class EmploymentHistory(BaseModel):
    """A person's full employment timeline.

    Records may be a mix of EmploymentRecord and EmploymentBreak entries in
    any order; the gap-detection algorithm sorts them internally.

    Overlapping records (e.g. two simultaneous part-time jobs) are handled
    correctly — their union is treated as covered time.

    Attributes:
        Records: All employment records and deliberate breaks.
        Gaps: Uncovered date intervals in the timeline (computed).
            An empty list means the timeline is fully accounted for.
    """

    Records: list[EmploymentRecord | EmploymentBreak]

    @computed_field
    @property
    def Gaps(self) -> list[DateRange]:
        """Uncovered periods between the earliest and latest record.

        Algorithm:
            1. Build a (start, end) interval for every record, using
               date.today() for any open-ended record or break.
            2. Sort intervals by start date.
            3. Merge overlapping or adjacent intervals into a coverage set.
            4. Collect the gaps between consecutive merged intervals.

        The analysis begins at the earliest StartDate across all records.
        A gap of even a single day is reported.

        Returns:
            List of DateRange objects, each representing one uncovered period.
            Empty list if Records is empty or the timeline is fully covered.
        """
        if not self.Records:
            return []

        today = date.today()

        # Build raw intervals
        intervals: list[tuple[date, date]] = []
        for rec in self.Records:
            start = rec.StartDate
            end = rec.EndDate if rec.EndDate is not None else today
            intervals.append((start, end))

        # Sort by start date
        intervals.sort(key=lambda t: t[0])

        # Merge overlapping / adjacent intervals
        merged: list[tuple[date, date]] = [intervals[0]]
        for start, end in intervals[1:]:
            prev_start, prev_end = merged[-1]
            if start <= prev_end:
                # Overlapping or touching — extend the current merged interval
                merged[-1] = (prev_start, max(prev_end, end))
            else:
                merged.append((start, end))

        # Gaps are the spaces between consecutive merged intervals
        gaps: list[DateRange] = []
        for i in range(1, len(merged)):
            gap_start = merged[i - 1][1]
            gap_end = merged[i][0]
            # gap_start is the end of the previous block; gap_end is the start
            # of the next block.  There is a gap if at least one day is missing.
            if gap_end > gap_start:
                gaps.append(DateRange(Start=gap_start, End=gap_end))

        return gaps
