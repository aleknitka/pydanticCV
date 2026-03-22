"""Tests for pydanticcv.languages.certificates.eng.ielts models.

Covers IELTS band scores, test centre codes, exam types, and CEFR level
derivation. Includes validation of the cross-field Overall constraint
and CEFRLevel thresholds.
"""

from datetime import date

import pytest
from pydantic import ValidationError, TypeAdapter

from pydanticcv.languages.certificates.eng.ielts import (
    IELTSBandScore,
    IELTSTestCentreCode,
    IELTSType,
    IELTSScores,
    IELTS,
)
from tests.conftest import IELTSScoresFactory, IELTSFactory


class TestIELTSBandScoreValidation:
    """Tests for IELTSBandScore type validation."""

    def test_accepts_valid_band_scores(self) -> None:
        """Tests that IELTSBandScore accepts all valid 0.5-step values.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(IELTSBandScore)
        valid_scores = [0.0, 0.5, 1.0, 4.5, 5.0, 8.5, 9.0]

        for score in valid_scores:
            result = validator.validate_python(score)
            assert result == score

    def test_rejects_band_score_below_zero(self) -> None:
        """Tests that IELTSBandScore rejects scores below 0.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(IELTSBandScore)

        with pytest.raises(ValidationError, match="must be between 0 and 9"):
            validator.validate_python(-0.5)

    def test_rejects_band_score_above_nine(self) -> None:
        """Tests that IELTSBandScore rejects scores above 9.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(IELTSBandScore)

        with pytest.raises(ValidationError, match="must be between 0 and 9"):
            validator.validate_python(9.5)

    def test_rejects_band_score_not_in_0_5_steps(self) -> None:
        """Tests that IELTSBandScore rejects non-0.5-step values.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(IELTSBandScore)

        with pytest.raises(ValidationError, match="must be in 0.5 steps"):
            validator.validate_python(5.3)

    @pytest.mark.parametrize(
        "invalid_score",
        [1.1, 2.3, 3.7, 7.2, 8.9],
        ids=["1.1", "2.3", "3.7", "7.2", "8.9"],
    )
    def test_rejects_various_invalid_steps(self, invalid_score: float) -> None:
        """Tests that IELTSBandScore rejects various non-0.5-step values.

        Args:
            invalid_score: A score not in 0.5 increments.

        Returns:
            None
        """
        validator = TypeAdapter(IELTSBandScore)

        with pytest.raises(ValidationError, match="must be in 0.5 steps"):
            validator.validate_python(invalid_score)


class TestIELTSTestCentreCodeValidation:
    """Tests for IELTSTestCentreCode pattern validation."""

    def test_accepts_valid_test_centre_codes(self) -> None:
        """Tests that IELTSTestCentreCode accepts valid ISO + digits codes.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(IELTSTestCentreCode)
        valid_codes = ["GB123", "US999", "AU1", "DE50"]

        for code in valid_codes:
            result = validator.validate_python(code)
            assert result == code

    def test_rejects_code_with_lowercase_letters(self) -> None:
        """Tests that IELTSTestCentreCode rejects lowercase letters.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(IELTSTestCentreCode)

        with pytest.raises(ValidationError, match="String should match pattern"):
            validator.validate_python("gb123")

    def test_rejects_code_with_wrong_letter_count(self) -> None:
        """Tests that IELTSTestCentreCode rejects non-2-letter codes.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(IELTSTestCentreCode)

        with pytest.raises(ValidationError, match="String should match pattern"):
            validator.validate_python("GBR123")

    def test_rejects_code_with_no_digits(self) -> None:
        """Tests that IELTSTestCentreCode rejects codes without digits.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(IELTSTestCentreCode)

        with pytest.raises(ValidationError, match="String should match pattern"):
            validator.validate_python("GB")

    def test_rejects_code_with_special_characters(self) -> None:
        """Tests that IELTSTestCentreCode rejects special characters.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(IELTSTestCentreCode)

        with pytest.raises(ValidationError, match="String should match pattern"):
            validator.validate_python("GB-123")


class TestIELTSTypeValidation:
    """Tests for IELTSType literal validation."""

    def test_accepts_academic_exam_type(self) -> None:
        """Tests that IELTSType accepts "Academic".

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(IELTSType)
        result = validator.validate_python("Academic")

        assert result == "Academic"

    def test_accepts_general_training_exam_type(self) -> None:
        """Tests that IELTSType accepts "General Training".

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(IELTSType)
        result = validator.validate_python("General Training")

        assert result == "General Training"

    def test_rejects_invalid_exam_type(self) -> None:
        """Tests that IELTSType rejects invalid exam type strings.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(IELTSType)

        with pytest.raises(ValidationError, match="Input should be 'Academic'"):
            validator.validate_python("Professional")


class TestIELTSScoresValidation:
    """Tests for IELTSScores model validation."""

    def test_accepts_valid_scores_with_matching_overall(self) -> None:
        """Tests that IELTSScores accepts valid scores with correct Overall.

        Args:
            None

        Returns:
            None
        """
        scores = IELTSScores(
            Listening=6.0,
            Reading=6.0,
            Writing=5.5,
            Speaking=6.0,
            Overall=6.0,
        )

        assert scores.Overall == 6.0

    def test_rejects_overall_not_matching_average(self) -> None:
        """Tests that IELTSScores rejects inconsistent Overall.

        Args:
            None

        Returns:
            None
        """
        with pytest.raises(
            ValidationError, match="Overall band score .* does not match"
        ):
            IELTSScores(
                Listening=6.0,
                Reading=6.0,
                Writing=6.0,
                Speaking=6.0,
                Overall=5.0,
            )

    def test_accepts_scores_averaging_to_6_0(self) -> None:
        """Tests that IELTSScores computes Overall correctly for 6.0 average.

        Args:
            None

        Returns:
            None
        """
        scores = IELTSScores(
            Listening=5.5,
            Reading=6.0,
            Writing=5.5,
            Speaking=6.0,
            Overall=6.0,
        )

        assert scores.Overall == 6.0

    def test_rejects_invalid_section_score(self) -> None:
        """Tests that IELTSScores rejects invalid section scores.

        Args:
            None

        Returns:
            None
        """
        with pytest.raises(ValidationError, match="must be between 0 and 9"):
            IELTSScores(
                Listening=9.5,
                Reading=6.0,
                Writing=6.0,
                Speaking=6.0,
                Overall=6.625,
            )


class TestIELTSCEFRLevelComputation:
    """Tests for IELTS CEFRLevel computed field."""

    @pytest.mark.parametrize(
        "overall,expected_cefr",
        [
            (8.5, "C2"),
            (9.0, "C2"),
            (7.0, "C1"),
            (7.5, "C1"),
            (8.0, "C1"),
            (5.5, "B2"),
            (6.0, "B2"),
            (6.5, "B2"),
            (4.5, "B1"),
            (5.0, "B1"),
            (0.0, "A1/A2"),
            (4.0, "A1/A2"),
        ],
        ids=[
            "8.5_C2", "9.0_C2",
            "7.0_C1", "7.5_C1", "8.0_C1",
            "5.5_B2", "6.0_B2", "6.5_B2",
            "4.5_B1", "5.0_B1",
            "0.0_A1/A2", "4.0_A1/A2",
        ],
    )
    def test_cefr_level_thresholds(
        self, overall: float, expected_cefr: str
    ) -> None:
        """Tests that CEFRLevel maps Overall correctly to CEFR thresholds.

        Args:
            overall: The Overall band score.
            expected_cefr: The expected CEFR level.

        Returns:
            None
        """
        ielts = IELTS(
            Scores=IELTSScores(
                Listening=overall,
                Reading=overall,
                Writing=overall,
                Speaking=overall,
                Overall=overall,
            ),
            DateTaken=date(2020, 5, 15),
            Link="https://example.com",
            ExamType="Academic",
        )

        assert ielts.CEFRLevel == expected_cefr


class TestIELTSModelValidation:
    """Tests for complete IELTS model validation."""

    def test_accepts_valid_ielts_exam_record(self) -> None:
        """Tests that IELTS accepts a valid complete exam record.

        Args:
            None

        Returns:
            None
        """
        ielts = IELTS(
            Scores=IELTSScores(
                Listening=6.0,
                Reading=6.0,
                Writing=6.0,
                Speaking=6.5,
                Overall=6.0,
            ),
            DateTaken=date(2020, 5, 15),
            Link="https://example.com",
            ExamType="Academic",
            TestCentreCode="GB123",
        )

        assert ielts.Scores.Overall == 6.0
        assert ielts.ExamType == "Academic"
        assert ielts.TestCentreCode == "GB123"

    def test_ielts_test_centre_code_optional(self) -> None:
        """Tests that IELTS accepts records without TestCentreCode.

        Args:
            None

        Returns:
            None
        """
        ielts = IELTS(
            Scores=IELTSScores(
                Listening=6.0,
                Reading=6.0,
                Writing=6.0,
                Speaking=6.0,
                Overall=6.0,
            ),
            DateTaken=date(2020, 5, 15),
            Link="https://example.com",
            ExamType="General Training",
        )

        assert ielts.TestCentreCode is None

    def test_ielts_rejects_future_date(self) -> None:
        """Tests that IELTS rejects future exam dates.

        Args:
            None

        Returns:
            None
        """
        future = date(2099, 1, 1)

        with pytest.raises(ValidationError, match="cannot be in the future"):
            IELTS(
                Scores=IELTSScores(
                    Listening=6.0,
                    Reading=6.0,
                    Writing=6.0,
                    Speaking=6.0,
                    Overall=6.0,
                ),
                DateTaken=future,
                Link="https://example.com",
                ExamType="Academic",
            )

    def test_ielts_factory_creates_valid_record(self) -> None:
        """Tests that IELTSFactory creates a valid exam record.

        Args:
            None

        Returns:
            None
        """
        ielts = IELTSFactory.create()

        assert ielts.Scores.Overall is not None
        assert ielts.DateTaken <= date.today()
        assert ielts.ExamType in ["Academic", "General Training"]
        assert ielts.CEFRLevel in ["A1/A2", "B1", "B2", "C1", "C2"]

    def test_ielts_factory_respects_overrides(self) -> None:
        """Tests that IELTSFactory respects field overrides.

        Args:
            None

        Returns:
            None
        """
        ielts = IELTSFactory.create(ExamType="Academic")

        assert ielts.ExamType == "Academic"
