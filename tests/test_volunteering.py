"""Tests for pydanticcv.activities.volunteering.

Tests cover VolunteeringArea enum and VolunteeringActivity model validation,
including date range checks, ongoing detection, and area acceptance.
"""

from datetime import date, timedelta

import pytest
from pydantic import ValidationError

from pydanticcv.activities import VolunteeringActivity, VolunteeringArea


_BASE = dict(
    Organisation="Green Earth",
    Role="Coordinator",
    Area=VolunteeringArea.Environment,
    StartDate=date(2022, 3, 1),
    Description="Organised beach clean-up events.",
)


class TestVolunteeringAreaEnum:
    """Tests for the VolunteeringArea enum."""

    def test_all_members_are_accessible(self) -> None:
        """Tests that every VolunteeringArea member can be referenced.

        Args:
            None

        Returns:
            None
        """
        expected = {
            "Education", "Environment", "Health", "Policy", "Community",
            "Humanitarian", "Arts", "AnimalWelfare", "Technology", "Sports",
        }
        assert {m.value for m in VolunteeringArea} == expected

    def test_invalid_area_raises_validation_error(self) -> None:
        """Tests that an invalid area string raises a ValidationError.

        Args:
            None

        Returns:
            None
        """
        with pytest.raises(ValidationError):
            VolunteeringActivity(**{**_BASE, "Area": "Cooking"})


class TestVolunteeringActivityValid:
    """Happy-path tests for VolunteeringActivity."""

    def test_ongoing_activity_has_no_end_date(self) -> None:
        """Tests that an activity without EndDate is created and IsOngoing is True.

        Args:
            None

        Returns:
            None
        """
        activity = VolunteeringActivity(**_BASE)

        assert activity.EndDate is None
        assert activity.IsOngoing is True

    def test_completed_activity_has_end_date(self) -> None:
        """Tests that an activity with EndDate is created and IsOngoing is False.

        Args:
            None

        Returns:
            None
        """
        activity = VolunteeringActivity(**{**_BASE, "EndDate": date(2023, 6, 30)})

        assert activity.EndDate == date(2023, 6, 30)
        assert activity.IsOngoing is False

    def test_all_volunteering_areas_accepted(self) -> None:
        """Tests that every VolunteeringArea value is accepted by the model.

        Args:
            None

        Returns:
            None
        """
        for area in VolunteeringArea:
            activity = VolunteeringActivity(**{**_BASE, "Area": area})
            assert activity.Area == area

    def test_start_date_equals_end_date_is_valid(self) -> None:
        """Tests that StartDate equal to EndDate is accepted.

        Args:
            None

        Returns:
            None
        """
        activity = VolunteeringActivity(**{**_BASE, "EndDate": _BASE["StartDate"]})

        assert activity.StartDate == activity.EndDate

    def test_string_dates_are_parsed(self) -> None:
        """Tests that ISO string dates are parsed by PastDate.

        Args:
            None

        Returns:
            None
        """
        activity = VolunteeringActivity(
            **{**_BASE, "StartDate": "2021-01-15", "EndDate": "2021-12-31"}
        )

        assert activity.StartDate == date(2021, 1, 15)
        assert activity.EndDate == date(2021, 12, 31)


class TestVolunteeringActivityDates:
    """Date validation tests for VolunteeringActivity."""

    def test_end_date_before_start_date_raises_validation_error(self) -> None:
        """Tests that EndDate before StartDate raises a ValidationError.

        Args:
            None

        Returns:
            None
        """
        with pytest.raises(ValidationError, match="EndDate.*cannot be before StartDate"):
            VolunteeringActivity(
                **{**_BASE, "EndDate": date(2021, 1, 1)}
            )

    def test_future_start_date_raises_validation_error(self) -> None:
        """Tests that a future StartDate raises a ValidationError.

        Args:
            None

        Returns:
            None
        """
        future = date.today() + timedelta(days=10)
        with pytest.raises(ValidationError):
            VolunteeringActivity(**{**_BASE, "StartDate": future})

    def test_future_end_date_raises_validation_error(self) -> None:
        """Tests that a future EndDate raises a ValidationError.

        Args:
            None

        Returns:
            None
        """
        future = date.today() + timedelta(days=10)
        with pytest.raises(ValidationError):
            VolunteeringActivity(**{**_BASE, "EndDate": future})
