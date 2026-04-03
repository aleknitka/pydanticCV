"""Tests for pydanticcv.languages.certificates.fra.tef models.

Covers TEF section score validation (0-20 range), six-section scores, exam
levels, and CEFR level derivation (average 0-3→A1, 4-5→A2, 6-7→B1, 8-9→B2,
10-13→C1, 14-20→C2).
"""

from datetime import date

import pytest
from pydantic import ValidationError, TypeAdapter

from pydanticcv.languages.certificates.fra.tef import (
    TEFSectionScore,
    TEFScores,
    TEF,
)


class TestTEFSectionScoreValidation:
    """Tests for TEFSectionScore type validation."""

    def test_accepts_valid_section_scores(self) -> None:
        """Tests that TEFSectionScore accepts valid scores 0-20.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(TEFSectionScore)
        valid_scores = [0, 5, 10, 15, 20]

        for score in valid_scores:
            result = validator.validate_python(score)
            assert result == score

    def test_rejects_section_score_below_zero(self) -> None:
        """Tests that TEFSectionScore rejects scores below 0.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(TEFSectionScore)

        with pytest.raises(ValidationError, match="must be between 0 and 20"):
            validator.validate_python(-1)

    def test_rejects_section_score_above_20(self) -> None:
        """Tests that TEFSectionScore rejects scores above 20.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(TEFSectionScore)

        with pytest.raises(ValidationError, match="must be between 0 and 20"):
            validator.validate_python(21)

    def test_accepts_exact_boundaries(self) -> None:
        """Tests that TEFSectionScore accepts boundary values 0 and 20.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(TEFSectionScore)

        assert validator.validate_python(0) == 0
        assert validator.validate_python(20) == 20


class TestTEFScoresValidation:
    """Tests for TEFScores model validation."""

    def test_accepts_valid_section_scores(self) -> None:
        """Tests that TEFScores accepts all six valid section scores.

        Args:
            None

        Returns:
            None
        """
        scores = TEFScores(
            Listening=15,
            Speaking=14,
            Reading=15,
            Writing=14,
            Structure=15,
            Vocabulary=15,
        )

        assert scores.Listening == 15
        assert scores.Speaking == 14
        assert scores.Reading == 15
        assert scores.Writing == 14
        assert scores.Structure == 15
        assert scores.Vocabulary == 15

    def test_rejects_invalid_section_score(self) -> None:
        """Tests that TEFScores rejects invalid section scores.

        Args:
            None

        Returns:
            None
        """
        with pytest.raises(ValidationError, match="must be between 0 and 20"):
            TEFScores(
                Listening=25,
                Speaking=14,
                Reading=15,
                Writing=14,
                Structure=15,
                Vocabulary=15,
            )

    def test_rejects_negative_section_score(self) -> None:
        """Tests that TEFScores rejects negative section scores.

        Args:
            None

        Returns:
            None
        """
        with pytest.raises(ValidationError, match="must be between 0 and 20"):
            TEFScores(
                Listening=-5,
                Speaking=14,
                Reading=15,
                Writing=14,
                Structure=15,
                Vocabulary=15,
            )


class TestTEFCEFRLevelComputation:
    """Tests for TEF CEFRLevel computed field."""

    @pytest.mark.parametrize(
        "avg_score,expected_cefr",
        [
            (20, "C2"),
            (19, "C2"),
            (15, "C2"),
            (14, "C2"),
            (13, "C1"),
            (12, "C1"),
            (10, "C1"),
            (9, "B2"),
            (8, "B2"),
            (7, "B1"),
            (6, "B1"),
            (5, "A2"),
            (4, "A2"),
            (3, "A1"),
            (2, "A1"),
            (1, "A1"),
            (0, "A1"),
        ],
        ids=[
            "20_C2",
            "19_C2",
            "15_C2",
            "14_C2",
            "13_C1",
            "12_C1",
            "10_C1",
            "9_B2",
            "8_B2",
            "7_B1",
            "6_B1",
            "5_A2",
            "4_A2",
            "3_A1",
            "2_A1",
            "1_A1",
            "0_A1",
        ],
    )
    def test_cefr_level_thresholds(self, avg_score: int, expected_cefr: str) -> None:
        """Tests that CEFRLevel maps average score correctly.

        Args:
            avg_score: The average section score (all sections equal).
            expected_cefr: The expected CEFR level.

        Returns:
            None
        """
        tef = TEF(
            Scores=TEFScores(
                Listening=avg_score,
                Speaking=avg_score,
                Reading=avg_score,
                Writing=avg_score,
                Structure=avg_score,
                Vocabulary=avg_score,
            ),
            DateTaken=date(2020, 5, 15),
            Link="https://example.com",
            ExamLevel="C",
        )

        assert tef.CEFRLevel == expected_cefr

    def test_cefr_level_with_mixed_scores(self) -> None:
        """Tests CEFRLevel with mixed section scores.

        Scores: 15, 15, 14, 14, 15, 15 → sum = 88 → avg = 14.67 → rounded to 15 → C2

        Args:
            None

        Returns:
            None
        """
        tef = TEF(
            Scores=TEFScores(
                Listening=15,
                Speaking=15,
                Reading=14,
                Writing=14,
                Structure=15,
                Vocabulary=15,
            ),
            DateTaken=date(2020, 5, 15),
            Link="https://example.com",
            ExamLevel="C",
        )

        assert tef.CEFRLevel == "C2"

    def test_cefr_level_rounds_correctly(self) -> None:
        """Tests that CEFRLevel rounds average correctly.

        Scores: 10, 10, 10, 10, 10, 10 → average = 10 → C1

        Args:
            None

        Returns:
            None
        """
        tef = TEF(
            Scores=TEFScores(
                Listening=10,
                Speaking=10,
                Reading=10,
                Writing=10,
                Structure=10,
                Vocabulary=10,
            ),
            DateTaken=date(2020, 5, 15),
            Link="https://example.com",
            ExamLevel="B",
        )

        assert tef.CEFRLevel == "C1"


class TestTEFModelValidation:
    """Tests for complete TEF model validation."""

    def test_accepts_valid_tef_exam_record(self) -> None:
        """Tests that TEF accepts a valid complete exam record.

        Args:
            None

        Returns:
            None
        """
        tef = TEF(
            Scores=TEFScores(
                Listening=15,
                Speaking=14,
                Reading=15,
                Writing=14,
                Structure=15,
                Vocabulary=15,
            ),
            DateTaken=date(2020, 5, 15),
            Link="https://example.com",
            ExamLevel="C",
        )

        assert tef.Scores.Listening == 15
        assert tef.ExamLevel == "C"
        assert tef.CEFRLevel == "C2"

    def test_accepts_all_exam_levels(self) -> None:
        """Tests that TEF accepts all valid exam levels.

        Args:
            None

        Returns:
            None
        """
        for level in ["A", "B", "C"]:
            tef = TEF(
                Scores=TEFScores(
                    Listening=10,
                    Speaking=10,
                    Reading=10,
                    Writing=10,
                    Structure=10,
                    Vocabulary=10,
                ),
                DateTaken=date(2020, 5, 15),
                Link="https://example.com",
                ExamLevel=level,
            )

            assert tef.ExamLevel == level

    def test_tef_rejects_future_date(self) -> None:
        """Tests that TEF rejects future exam dates.

        Args:
            None

        Returns:
            None
        """
        future = date(2099, 1, 1)

        with pytest.raises(ValidationError, match="cannot be in the future"):
            TEF(
                Scores=TEFScores(
                    Listening=10,
                    Speaking=10,
                    Reading=10,
                    Writing=10,
                    Structure=10,
                    Vocabulary=10,
                ),
                DateTaken=future,
                Link="https://example.com",
                ExamLevel="B",
            )

    def test_tef_requires_link(self) -> None:
        """Tests that TEF requires a Link field.

        Args:
            None

        Returns:
            None
        """
        with pytest.raises(ValidationError, match="Link"):
            TEF(
                Scores=TEFScores(
                    Listening=10,
                    Speaking=10,
                    Reading=10,
                    Writing=10,
                    Structure=10,
                    Vocabulary=10,
                ),
                DateTaken=date(2020, 5, 15),
                ExamLevel="B",
            )

    def test_tef_rejects_invalid_exam_level(self) -> None:
        """Tests that TEF rejects invalid exam level values.

        Args:
            None

        Returns:
            None
        """
        with pytest.raises(ValidationError, match="Input should be 'A'"):
            TEF(
                Scores=TEFScores(
                    Listening=10,
                    Speaking=10,
                    Reading=10,
                    Writing=10,
                    Structure=10,
                    Vocabulary=10,
                ),
                DateTaken=date(2020, 5, 15),
                Link="https://example.com",
                ExamLevel="D",
            )


class TestPublicAPIIntegration:
    """Tests for TEF integration with public certificates API."""

    def test_tef_importable_from_public_api(self) -> None:
        """Tests that TEF can be imported from pydanticcv.languages.certificates.

        Args:
            None

        Returns:
            None
        """
        from pydanticcv.languages.certificates import TEF

        tef = TEF(
            Scores=TEFScores(
                Listening=12,
                Speaking=11,
                Reading=12,
                Writing=11,
                Structure=12,
                Vocabulary=11,
            ),
            DateTaken=date(2024, 3, 15),
            Link="https://example.com",
            ExamLevel="B",
        )

        assert tef.CEFRLevel == "C1"
