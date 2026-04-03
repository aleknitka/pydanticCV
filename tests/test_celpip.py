"""Tests for pydanticcv.languages.certificates.eng.celpip models.

Covers CELPIP CLB score validation (4-12 range), section scores, exam types,
and CEFR level derivation (CLB 4-6→A2, CLB 7→B1, CLB 8-9→B2, CLB 10-11→C1,
CLB 12→C2).
"""

from datetime import date

import pytest
from pydantic import ValidationError, TypeAdapter

from pydanticcv.languages.certificates.eng.celpip import (
    CELPIPCLBScore,
    CELPIPScores,
    CELPIP,
)


class TestCELPIPCLBScoreValidation:
    """Tests for CELPIPCLBScore type validation."""

    def test_accepts_valid_clb_scores(self) -> None:
        """Tests that CELPIPCLBScore accepts all valid CLB levels 4-12.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(CELPIPCLBScore)
        valid_scores = [4, 5, 6, 7, 8, 9, 10, 11, 12]

        for score in valid_scores:
            result = validator.validate_python(score)
            assert result == score

    def test_rejects_clb_score_below_4(self) -> None:
        """Tests that CELPIPCLBScore rejects scores below 4.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(CELPIPCLBScore)

        with pytest.raises(ValidationError, match="must be between 4 and 12"):
            validator.validate_python(3)

    def test_rejects_clb_score_above_12(self) -> None:
        """Tests that CELPIPCLBScore rejects scores above 12.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(CELPIPCLBScore)

        with pytest.raises(ValidationError, match="must be between 4 and 12"):
            validator.validate_python(13)

    def test_rejects_clb_score_zero(self) -> None:
        """Tests that CELPIPCLBScore rejects score of 0.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(CELPIPCLBScore)

        with pytest.raises(ValidationError, match="must be between 4 and 12"):
            validator.validate_python(0)

    def test_rejects_negative_clb_score(self) -> None:
        """Tests that CELPIPCLBScore rejects negative scores.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(CELPIPCLBScore)

        with pytest.raises(ValidationError, match="must be between 4 and 12"):
            validator.validate_python(-1)


class TestCELPIPScoresValidation:
    """Tests for CELPIPScores model validation."""

    def test_accepts_valid_section_scores(self) -> None:
        """Tests that CELPIPScores accepts all valid CLB section scores.

        Args:
            None

        Returns:
            None
        """
        scores = CELPIPScores(
            Listening=8,
            Speaking=9,
            Reading=10,
            Writing=7,
        )

        assert scores.Listening == 8
        assert scores.Speaking == 9
        assert scores.Reading == 10
        assert scores.Writing == 7

    def test_rejects_invalid_section_score(self) -> None:
        """Tests that CELPIPScores rejects invalid section scores.

        Args:
            None

        Returns:
            None
        """
        with pytest.raises(ValidationError, match="must be between 4 and 12"):
            CELPIPScores(
                Listening=3,
                Speaking=10,
                Reading=10,
                Writing=10,
            )

    def test_rejects_section_score_above_12(self) -> None:
        """Tests that CELPIPScores rejects scores above 12.

        Args:
            None

        Returns:
            None
        """
        with pytest.raises(ValidationError, match="must be between 4 and 12"):
            CELPIPScores(
                Listening=15,
                Speaking=10,
                Reading=10,
                Writing=10,
            )


class TestCELPIPCEFRLevelComputation:
    """Tests for CELPIP CEFRLevel computed field."""

    @pytest.mark.parametrize(
        "avg_clb,expected_cefr",
        [
            (12, "C2"),
            (11, "C1"),
            (10, "C1"),
            (9, "B2"),
            (8, "B2"),
            (7, "B1"),
            (6, "A2"),
            (5, "A2"),
            (4, "A2"),
        ],
        ids=[
            "12_C2",
            "11_C1",
            "10_C1",
            "9_B2",
            "8_B2",
            "7_B1",
            "6_A2",
            "5_A2",
            "4_A2",
        ],
    )
    def test_cefr_level_thresholds(self, avg_clb: int, expected_cefr: str) -> None:
        """Tests that CEFRLevel maps average CLB score correctly.

        Args:
            avg_clb: The average CLB score (all sections equal).
            expected_cefr: The expected CEFR level.

        Returns:
            None
        """
        celpip = CELPIP(
            Scores=CELPIPScores(
                Listening=avg_clb,
                Speaking=avg_clb,
                Reading=avg_clb,
                Writing=avg_clb,
            ),
            DateTaken=date(2020, 5, 15),
            Link="https://example.com",
            ExamType="General",
        )

        assert celpip.CEFRLevel == expected_cefr

    def test_cefr_level_with_mixed_scores(self) -> None:
        """Tests CEFRLevel with mixed section scores.

        CLB scores: 10, 10, 9, 9 → average = 9.5 → rounded to 10 → C1

        Args:
            None

        Returns:
            None
        """
        celpip = CELPIP(
            Scores=CELPIPScores(
                Listening=10,
                Speaking=10,
                Reading=9,
                Writing=9,
            ),
            DateTaken=date(2020, 5, 15),
            Link="https://example.com",
            ExamType="Academic",
        )

        assert celpip.CEFRLevel == "C1"

    def test_cefr_level_rounds_correctly(self) -> None:
        """Tests that CEFRLevel rounds average correctly.

        CLB scores: 8, 8, 8, 9 → average = 8.25 → rounded to 8 → B2

        Args:
            None

        Returns:
            None
        """
        celpip = CELPIP(
            Scores=CELPIPScores(
                Listening=8,
                Speaking=8,
                Reading=8,
                Writing=9,
            ),
            DateTaken=date(2020, 5, 15),
            Link="https://example.com",
            ExamType="General",
        )

        assert celpip.CEFRLevel == "B2"


class TestCELPIPModelValidation:
    """Tests for complete CELPIP model validation."""

    def test_accepts_valid_celpip_exam_record(self) -> None:
        """Tests that CELPIP accepts a valid complete exam record.

        Args:
            None

        Returns:
            None
        """
        celpip = CELPIP(
            Scores=CELPIPScores(
                Listening=10,
                Speaking=10,
                Reading=10,
                Writing=10,
            ),
            DateTaken=date(2020, 5, 15),
            Link="https://example.com",
            ExamType="General",
        )

        assert celpip.Scores.Listening == 10
        assert celpip.ExamType == "General"
        assert celpip.CEFRLevel == "C1"

    def test_accepts_academic_exam_type(self) -> None:
        """Tests that CELPIP accepts the Academic exam type.

        Args:
            None

        Returns:
            None
        """
        celpip = CELPIP(
            Scores=CELPIPScores(
                Listening=12,
                Speaking=12,
                Reading=12,
                Writing=12,
            ),
            DateTaken=date(2020, 5, 15),
            Link="https://example.com",
            ExamType="Academic",
        )

        assert celpip.ExamType == "Academic"
        assert celpip.CEFRLevel == "C2"

    def test_celpip_rejects_future_date(self) -> None:
        """Tests that CELPIP rejects future exam dates.

        Args:
            None

        Returns:
            None
        """
        future = date(2099, 1, 1)

        with pytest.raises(ValidationError, match="cannot be in the future"):
            CELPIP(
                Scores=CELPIPScores(
                    Listening=8,
                    Speaking=8,
                    Reading=8,
                    Writing=8,
                ),
                DateTaken=future,
                Link="https://example.com",
                ExamType="General",
            )

    def test_celpip_requires_link(self) -> None:
        """Tests that CELPIP requires a Link field.

        Args:
            None

        Returns:
            None
        """
        with pytest.raises(ValidationError, match="Link"):
            CELPIP(
                Scores=CELPIPScores(
                    Listening=8,
                    Speaking=8,
                    Reading=8,
                    Writing=8,
                ),
                DateTaken=date(2020, 5, 15),
                ExamType="General",
            )


class TestPublicAPIIntegration:
    """Tests for CELPIP integration with public certificates API."""

    def test_celpip_importable_from_public_api(self) -> None:
        """Tests that CELPIP can be imported from pydanticcv.languages.certificates.

        Args:
            None

        Returns:
            None
        """
        from pydanticcv.languages.certificates import CELPIP

        celpip = CELPIP(
            Scores=CELPIPScores(
                Listening=8,
                Speaking=9,
                Reading=8,
                Writing=9,
            ),
            DateTaken=date(2024, 3, 15),
            Link="https://example.com",
            ExamType="General",
        )

        assert celpip.CEFRLevel == "B2"
