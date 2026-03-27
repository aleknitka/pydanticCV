"""Tests for the employment history models.

Covers EmploymentType, BreakReason, EmploymentRecord, EmploymentBreak,
DateRange, and EmploymentHistory including the gap-detection algorithm.
"""

from datetime import date, timedelta

import pytest
from pydantic import ValidationError

from pydanticcv.employment import (
    BreakReason,
    DateRange,
    EmploymentBreak,
    EmploymentHistory,
    EmploymentRecord,
    EmploymentType,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_TODAY = date.today()
_PAST = _TODAY - timedelta(days=365 * 3)  # 3 years ago
_FUTURE = _TODAY + timedelta(days=1)


def _record(
    start: date,
    end: date | None,
    emp_type: EmploymentType = EmploymentType.EMPLOYEE,
) -> EmploymentRecord:
    return EmploymentRecord(
        EmployerName="Acme",
        Role="Developer",
        EmploymentType=emp_type,
        StartDate=start,
        EndDate=end,
    )


def _break(start: date, end: date | None) -> EmploymentBreak:
    return EmploymentBreak(StartDate=start, EndDate=end)


# ---------------------------------------------------------------------------
# TestEmploymentType
# ---------------------------------------------------------------------------


class TestEmploymentType:
    def test_values_are_stable_strings(self):
        assert EmploymentType.EMPLOYEE == "Employee"
        assert EmploymentType.B2B == "B2B"
        assert EmploymentType.SELF_EMPLOYED == "Self-employed"
        assert EmploymentType.FREELANCE == "Freelance"
        assert EmploymentType.INTERNSHIP == "Internship"
        assert EmploymentType.APPRENTICESHIP == "Apprenticeship"
        assert EmploymentType.VOLUNTEER == "Volunteer"
        assert EmploymentType.OTHER == "Other"

    def test_all_members_present(self):
        assert len(EmploymentType) == 8


# ---------------------------------------------------------------------------
# TestBreakReason
# ---------------------------------------------------------------------------


class TestBreakReason:
    def test_values_are_stable_strings(self):
        assert BreakReason.PARENTAL_LEAVE == "Parental leave"
        assert BreakReason.SABBATICAL == "Sabbatical"
        assert BreakReason.EDUCATION == "Education"
        assert BreakReason.TRAVEL == "Travel"
        assert BreakReason.ILLNESS == "Illness"
        assert BreakReason.CAREGIVING == "Caregiving"
        assert BreakReason.JOB_SEARCH == "Job search"
        assert BreakReason.PERSONAL == "Personal"
        assert BreakReason.OTHER == "Other"

    def test_all_members_present(self):
        assert len(BreakReason) == 9


# ---------------------------------------------------------------------------
# TestEmploymentRecord
# ---------------------------------------------------------------------------


class TestEmploymentRecord:
    def _base(self, **kwargs) -> dict:
        return {
            "EmployerName": "Acme Corp",
            "Role": "Engineer",
            "EmploymentType": EmploymentType.EMPLOYEE,
            "StartDate": date(2020, 1, 1),
            **kwargs,
        }

    def test_minimal_valid_record(self):
        rec = EmploymentRecord(**self._base())
        assert rec.EmployerName == "Acme Corp"
        assert rec.IsCurrent is True
        assert rec.EndDate is None

    def test_closed_record(self):
        rec = EmploymentRecord(**self._base(EndDate=date(2022, 6, 30)))
        assert rec.IsCurrent is False
        assert rec.EndDate == date(2022, 6, 30)

    def test_future_start_date_rejected(self):
        with pytest.raises(ValidationError):
            EmploymentRecord(**self._base(StartDate=_FUTURE))

    def test_future_end_date_rejected(self):
        with pytest.raises(ValidationError):
            EmploymentRecord(**self._base(EndDate=_FUTURE))

    def test_end_before_start_rejected(self):
        with pytest.raises(ValidationError, match="EndDate"):
            EmploymentRecord(**self._base(EndDate=date(2019, 12, 31)))

    def test_end_equal_to_start_rejected(self):
        with pytest.raises(ValidationError, match="EndDate"):
            EmploymentRecord(**self._base(EndDate=date(2020, 1, 1)))

    def test_description_optional(self):
        rec = EmploymentRecord(**self._base(Description="Led backend team."))
        assert rec.Description == "Led backend team."

        rec2 = EmploymentRecord(**self._base())
        assert rec2.Description is None

    def test_responsibilities_optional(self):
        duties = ["Design APIs", "Code review"]
        rec = EmploymentRecord(**self._base(Responsibilities=duties))
        assert rec.Responsibilities == duties

        rec2 = EmploymentRecord(**self._base())
        assert rec2.Responsibilities is None

    def test_achievements_optional(self):
        wins = ["Reduced latency by 30%"]
        rec = EmploymentRecord(**self._base(Achievements=wins))
        assert rec.Achievements == wins

        rec2 = EmploymentRecord(**self._base())
        assert rec2.Achievements is None

    def test_clients_optional(self):
        rec = EmploymentRecord(
            **self._base(EmploymentType=EmploymentType.B2B, Clients=["ClientA", "ClientB"])
        )
        assert rec.Clients == ["ClientA", "ClientB"]

        rec2 = EmploymentRecord(**self._base())
        assert rec2.Clients is None

    @pytest.mark.parametrize("emp_type", list(EmploymentType))
    def test_all_employment_types_accepted(self, emp_type):
        rec = EmploymentRecord(**self._base(EmploymentType=emp_type))
        assert rec.EmploymentType == emp_type

    def test_string_date_accepted(self):
        rec = EmploymentRecord(**self._base(StartDate="2020-01-01"))
        assert rec.StartDate == date(2020, 1, 1)


# ---------------------------------------------------------------------------
# TestEmploymentBreak
# ---------------------------------------------------------------------------


class TestEmploymentBreak:
    def test_minimal_break_no_reason(self):
        brk = EmploymentBreak(StartDate=date(2021, 1, 1), EndDate=date(2021, 6, 30))
        assert brk.Reason is None
        assert brk.Description is None

    def test_ongoing_break(self):
        brk = EmploymentBreak(StartDate=date(2023, 1, 1))
        assert brk.EndDate is None

    def test_reason_accepted(self):
        brk = EmploymentBreak(
            StartDate=date(2021, 1, 1),
            EndDate=date(2021, 6, 30),
            Reason=BreakReason.PARENTAL_LEAVE,
        )
        assert brk.Reason == BreakReason.PARENTAL_LEAVE

    def test_description_accepted(self):
        brk = EmploymentBreak(
            StartDate=date(2021, 1, 1),
            EndDate=date(2021, 6, 30),
            Description="Stayed home with newborn.",
        )
        assert brk.Description == "Stayed home with newborn."

    def test_future_start_rejected(self):
        with pytest.raises(ValidationError):
            EmploymentBreak(StartDate=_FUTURE)

    def test_future_end_rejected(self):
        with pytest.raises(ValidationError):
            EmploymentBreak(StartDate=date(2020, 1, 1), EndDate=_FUTURE)

    def test_end_before_start_rejected(self):
        with pytest.raises(ValidationError, match="EndDate"):
            EmploymentBreak(StartDate=date(2021, 6, 1), EndDate=date(2021, 1, 1))

    def test_end_equal_to_start_rejected(self):
        with pytest.raises(ValidationError, match="EndDate"):
            EmploymentBreak(StartDate=date(2021, 1, 1), EndDate=date(2021, 1, 1))

    @pytest.mark.parametrize("reason", list(BreakReason))
    def test_all_break_reasons_accepted(self, reason):
        brk = EmploymentBreak(
            StartDate=date(2021, 1, 1), EndDate=date(2021, 6, 30), Reason=reason
        )
        assert brk.Reason == reason


# ---------------------------------------------------------------------------
# TestEmploymentHistory
# ---------------------------------------------------------------------------


class TestEmploymentHistory:
    def test_empty_records_no_gaps(self):
        h = EmploymentHistory(Records=[])
        assert h.Gaps == []

    def test_single_current_record_no_gaps(self):
        h = EmploymentHistory(Records=[_record(date(2020, 1, 1), None)])
        assert h.Gaps == []

    def test_single_closed_record_no_gaps(self):
        # A single record — nothing to compare against, so no gaps.
        h = EmploymentHistory(Records=[_record(date(2020, 1, 1), date(2022, 12, 31))])
        assert h.Gaps == []

    def test_two_adjacent_records_no_gaps(self):
        # End of first == start of second → no gap.
        h = EmploymentHistory(
            Records=[
                _record(date(2020, 1, 1), date(2021, 6, 30)),
                _record(date(2021, 6, 30), date(2023, 1, 1)),
            ]
        )
        assert h.Gaps == []

    def test_gap_between_two_records(self):
        h = EmploymentHistory(
            Records=[
                _record(date(2020, 1, 1), date(2021, 6, 30)),
                _record(date(2021, 10, 1), None),
            ]
        )
        assert len(h.Gaps) == 1
        gap = h.Gaps[0]
        assert gap.Start == date(2021, 6, 30)
        assert gap.End == date(2021, 10, 1)

    def test_break_fills_gap(self):
        h = EmploymentHistory(
            Records=[
                _record(date(2020, 1, 1), date(2021, 6, 30)),
                _break(date(2021, 6, 30), date(2021, 10, 1)),
                _record(date(2021, 10, 1), None),
            ]
        )
        assert h.Gaps == []

    def test_partial_break_still_leaves_gap(self):
        # Break only covers part of the gap.
        h = EmploymentHistory(
            Records=[
                _record(date(2020, 1, 1), date(2021, 6, 30)),
                _break(date(2021, 6, 30), date(2021, 8, 1)),   # gap 2021-08-01 to 2021-10-01
                _record(date(2021, 10, 1), None),
            ]
        )
        assert len(h.Gaps) == 1
        assert h.Gaps[0].Start == date(2021, 8, 1)
        assert h.Gaps[0].End == date(2021, 10, 1)

    def test_overlapping_records_no_false_gap(self):
        # Two simultaneous part-time jobs.
        h = EmploymentHistory(
            Records=[
                _record(date(2020, 1, 1), date(2022, 12, 31)),
                _record(date(2021, 6, 1), date(2023, 6, 30)),
            ]
        )
        assert h.Gaps == []

    def test_multiple_gaps_all_reported(self):
        h = EmploymentHistory(
            Records=[
                _record(date(2018, 1, 1), date(2019, 1, 1)),
                _record(date(2020, 1, 1), date(2021, 1, 1)),
                _record(date(2022, 1, 1), None),
            ]
        )
        assert len(h.Gaps) == 2
        assert h.Gaps[0].Start == date(2019, 1, 1)
        assert h.Gaps[0].End == date(2020, 1, 1)
        assert h.Gaps[1].Start == date(2021, 1, 1)
        assert h.Gaps[1].End == date(2022, 1, 1)

    def test_current_position_no_trailing_gap(self):
        # The current role extends to today, so there is no gap after it.
        h = EmploymentHistory(
            Records=[
                _record(date(2020, 1, 1), date(2021, 6, 30)),
                _record(date(2021, 6, 30), None),
            ]
        )
        assert h.Gaps == []

    def test_records_order_independent(self):
        # Records given in reverse chronological order should produce same gaps.
        r1 = _record(date(2020, 1, 1), date(2021, 1, 1))
        r2 = _record(date(2022, 1, 1), date(2023, 1, 1))
        h_fwd = EmploymentHistory(Records=[r1, r2])
        h_rev = EmploymentHistory(Records=[r2, r1])
        assert h_fwd.Gaps == h_rev.Gaps
        assert len(h_fwd.Gaps) == 1

    def test_mixed_record_and_break_types(self):
        h = EmploymentHistory(
            Records=[
                _record(date(2019, 1, 1), date(2020, 6, 30)),
                _break(date(2020, 6, 30), date(2020, 12, 31)),
                _record(date(2020, 12, 31), None),
            ]
        )
        assert h.Gaps == []
