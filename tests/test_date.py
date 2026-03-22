"""Tests for pydanticcv.utils.date.PastDate validator.

PastDate is an Annotated[date, BeforeValidator] that accepts date objects
and multiple string formats, enforcing that dates must not be in the future.
"""

from datetime import date, timedelta

import pytest
from pydantic import ValidationError, TypeAdapter

from pydanticcv.utils.date import PastDate


class TestPastDateAcceptsDateObjects:
    """Tests for accepting date object inputs."""

    def test_past_date_accepts_date_object_from_past(self) -> None:
        """Tests that PastDate accepts a date object from the past.

        Args:
            None

        Returns:
            None
        """
        past = date(2020, 5, 15)
        validator = TypeAdapter(PastDate)
        result = validator.validate_python(past)

        assert result == past

    def test_past_date_accepts_date_object_from_today(self) -> None:
        """Tests that PastDate accepts today's date.

        Args:
            None

        Returns:
            None
        """
        today = date.today()
        validator = TypeAdapter(PastDate)
        result = validator.validate_python(today)

        assert result == today

    def test_past_date_rejects_date_object_from_future(self) -> None:
        """Tests that PastDate rejects a date object from the future.

        Args:
            None

        Returns:
            None
        """
        tomorrow = date.today() + timedelta(days=1)
        validator = TypeAdapter(PastDate)

        with pytest.raises(ValidationError, match="cannot be in the future"):
            validator.validate_python(tomorrow)


class TestPastDateISOFormat:
    """Tests for accepting ISO format strings (%Y-%m-%d)."""

    def test_parses_iso_format_past_date(self) -> None:
        """Tests that PastDate parses ISO format strings.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(PastDate)
        result = validator.validate_python("2020-05-15")

        assert result == date(2020, 5, 15)

    def test_parses_iso_format_today(self) -> None:
        """Tests that PastDate parses today's date in ISO format.

        Args:
            None

        Returns:
            None
        """
        today = date.today()
        validator = TypeAdapter(PastDate)
        result = validator.validate_python(today.isoformat())

        assert result == today

    def test_rejects_iso_format_future_date(self) -> None:
        """Tests that PastDate rejects future dates in ISO format.

        Args:
            None

        Returns:
            None
        """
        tomorrow = date.today() + timedelta(days=1)
        validator = TypeAdapter(PastDate)

        with pytest.raises(ValidationError, match="cannot be in the future"):
            validator.validate_python(tomorrow.strftime("%Y-%m-%d"))


class TestPastDateNumericFormat:
    """Tests for accepting numeric format strings (%Y/%m/%d)."""

    def test_parses_numeric_format(self) -> None:
        """Tests that PastDate parses numeric format with slashes.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(PastDate)
        result = validator.validate_python("2020/05/15")

        assert result == date(2020, 5, 15)

    def test_rejects_numeric_format_future_date(self) -> None:
        """Tests that PastDate rejects future dates in numeric format.

        Args:
            None

        Returns:
            None
        """
        tomorrow = date.today() + timedelta(days=1)
        validator = TypeAdapter(PastDate)

        with pytest.raises(ValidationError, match="cannot be in the future"):
            validator.validate_python(tomorrow.strftime("%Y/%m/%d"))


class TestPastDateDottedFormat:
    """Tests for accepting dotted format strings (%Y.%m.%d)."""

    def test_parses_dotted_format(self) -> None:
        """Tests that PastDate parses dotted format.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(PastDate)
        result = validator.validate_python("2023.04.23")

        assert result == date(2023, 4, 23)

    def test_rejects_dotted_format_future_date(self) -> None:
        """Tests that PastDate rejects future dates in dotted format.

        Args:
            None

        Returns:
            None
        """
        tomorrow = date.today() + timedelta(days=1)
        validator = TypeAdapter(PastDate)

        with pytest.raises(ValidationError, match="cannot be in the future"):
            validator.validate_python(tomorrow.strftime("%Y.%m.%d"))


class TestPastDateEuropeanFormat:
    """Tests for accepting European format strings (DD/MM/YYYY and DD-MM-YYYY).

    European format is prioritized over US format for slash-separated dates.
    """

    def test_parses_european_slash_format(self) -> None:
        """Tests that PastDate parses European slash format.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(PastDate)
        result = validator.validate_python("23/04/2012")

        assert result == date(2012, 4, 23)

    def test_parses_european_dash_format(self) -> None:
        """Tests that PastDate parses European dash format.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(PastDate)
        result = validator.validate_python("23-04-2012")

        assert result == date(2012, 4, 23)

    def test_parses_european_dot_format(self) -> None:
        """Tests that PastDate parses European dot format.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(PastDate)
        result = validator.validate_python("23.04.2012")

        assert result == date(2012, 4, 23)

    def test_european_format_takes_priority_over_us_for_slash(self) -> None:
        """Tests that European format (DD/MM/YYYY) is tried before US.

        For the ambiguous date string "04/05/2012", which could be
        April 5 (US) or May 4 (European), European format takes priority
        and the result should be May 4, 2012.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(PastDate)
        result = validator.validate_python("04/05/2012")

        assert result == date(2012, 5, 4)

    def test_rejects_european_format_future_date(self) -> None:
        """Tests that PastDate rejects future dates in European format.

        Args:
            None

        Returns:
            None
        """
        tomorrow = date.today() + timedelta(days=1)
        validator = TypeAdapter(PastDate)

        with pytest.raises(ValidationError, match="cannot be in the future"):
            validator.validate_python(tomorrow.strftime("%d/%m/%Y"))


class TestPastDateUSFormat:
    """Tests for accepting US format strings (MM/DD/YYYY and MM-DD-YYYY).

    US format is only tried when European format fails for slash-separated dates.
    """

    def test_parses_us_slash_format_unambiguous(self) -> None:
        """Tests that PastDate parses unambiguous US slash format.

        For the date "12/05/2012", which is unambiguous (no month 13 exists),
        European format (DD/MM/YYYY) fails, so US format is tried.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(PastDate)
        result = validator.validate_python("12/05/2012")

        assert result == date(2012, 5, 12)

    def test_parses_us_dash_format(self) -> None:
        """Tests that PastDate parses US dash format.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(PastDate)
        result = validator.validate_python("04-23-2012")

        assert result == date(2012, 4, 23)

    def test_rejects_us_format_future_date(self) -> None:
        """Tests that PastDate rejects future dates in US format.

        Args:
            None

        Returns:
            None
        """
        tomorrow = date.today() + timedelta(days=1)
        validator = TypeAdapter(PastDate)

        with pytest.raises(ValidationError, match="cannot be in the future"):
            validator.validate_python(tomorrow.strftime("%m-%d-%Y"))


class TestPastDateErrorHandling:
    """Tests for error handling and invalid inputs."""

    def test_rejects_invalid_string_format(self) -> None:
        """Tests that PastDate rejects strings in unrecognized formats.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(PastDate)

        with pytest.raises(ValidationError, match="Unrecognised date format"):
            validator.validate_python("15/04/2012-invalid")

    def test_rejects_non_date_non_string_type(self) -> None:
        """Tests that PastDate rejects non-date, non-string inputs.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(PastDate)

        with pytest.raises(ValidationError, match="Expected a date or string"):
            validator.validate_python(12345)

    def test_rejects_invalid_date_values(self) -> None:
        """Tests that PastDate rejects strings with invalid date values.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(PastDate)

        with pytest.raises(ValidationError):
            validator.validate_python("2020-13-45")

    def test_rejects_empty_string(self) -> None:
        """Tests that PastDate rejects empty strings.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(PastDate)

        with pytest.raises(ValidationError):
            validator.validate_python("")
