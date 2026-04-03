"""Tests for pydanticcv.languages.certificates.zho.hsk models.

Covers HSK level validation, section scores, pass score thresholds, and
CEFR level derivation (preliminary mapping: HSK1-2→A2, HSK3→B1,
HSK4→B2, HSK5-6→C1).
"""

from datetime import date

import pytest
from pydantic import ValidationError

from pydanticcv.languages.certificates.zho.hsk import (
    HSK,
    HSKLevel,
    HSKSectionScores,
)


class TestHSKLevelValidation:
    """Tests for HSKLevel literal type validation."""

    def test_accepts_valid_hsk_levels(self) -> None:
        """Tests that HSKLevel accepts all valid levels 1-6.

        Args:
            None

        Returns:
            None
        """
        for level in [1, 2, 3, 4, 5, 6]:
            hsk = HSK(
                Level=level,
                Scores={"Listening": 80, "Reading": 80}
                if level <= 2
                else {"Listening": 80, "Reading": 80, "Writing": 80},
                DateTaken=date(2024, 3, 15),
                Link="https://chinesetest.cn/hsk",
            )
            assert hsk.Level == level

    def test_rejects_invalid_hsk_level(self) -> None:
        """Tests that HSKLevel rejects invalid level values.

        Args:
            None

        Returns:
            None
        """
        with pytest.raises(ValidationError, match="Input should be 1"):
            HSK(
                Level=0,
                Scores={"Listening": 80, "Reading": 80},
                DateTaken=date(2024, 3, 15),
                Link="https://chinesetest.cn/hsk",
            )

        with pytest.raises(ValidationError, match="Input should be 1"):
            HSK(
                Level=7,
                Scores={"Listening": 80, "Reading": 80, "Writing": 80},
                DateTaken=date(2024, 3, 15),
                Link="https://chinesetest.cn/hsk",
            )


class TestHSKSectionScoresValidation:
    """Tests for HSKSectionScores model validation."""

    def test_accepts_valid_section_scores(self) -> None:
        """Tests that HSKSectionScores accepts valid scores.

        Args:
            None

        Returns:
            None
        """
        scores = HSKSectionScores(Listening=85, Reading=90, Writing=80)

        assert scores.Listening == 85
        assert scores.Reading == 90
        assert scores.Writing == 80

    def test_accepts_scores_without_writing(self) -> None:
        """Tests that HSKSectionScores accepts scores without Writing.

        Args:
            None

        Returns:
            None
        """
        scores = HSKSectionScores(Listening=85, Reading=90)

        assert scores.Listening == 85
        assert scores.Reading == 90
        assert scores.Writing is None

    def test_rejects_score_below_zero(self) -> None:
        """Tests that HSKSectionScores rejects scores below 0.

        Args:
            None

        Returns:
            None
        """
        with pytest.raises(ValidationError, match="must be between 0 and 100"):
            HSKSectionScores(Listening=-5, Reading=50)

    def test_rejects_score_above_100(self) -> None:
        """Tests that HSKSectionScores rejects scores above 100.

        Args:
            None

        Returns:
            None
        """
        with pytest.raises(ValidationError, match="must be between 0 and 100"):
            HSKSectionScores(Listening=150, Reading=50)


class TestHSKLevelScoreConsistency:
    """Tests for HSK level and score consistency validation."""

    def test_rejects_writing_for_hsk_1(self) -> None:
        """Tests that HSK 1 rejects Writing section.

        Args:
            None

        Returns:
            None
        """
        with pytest.raises(
            ValidationError, match="HSK level 1 does not have a Writing section"
        ):
            HSK(
                Level=1,
                Scores={"Listening": 90, "Reading": 85, "Writing": 80},
                DateTaken=date(2024, 3, 15),
                Link="https://chinesetest.cn/hsk",
            )

    def test_rejects_writing_for_hsk_2(self) -> None:
        """Tests that HSK 2 rejects Writing section.

        Args:
            None

        Returns:
            None
        """
        with pytest.raises(
            ValidationError, match="HSK level 2 does not have a Writing section"
        ):
            HSK(
                Level=2,
                Scores={"Listening": 90, "Reading": 85, "Writing": 80},
                DateTaken=date(2024, 3, 15),
                Link="https://chinesetest.cn/hsk",
            )

    def test_requires_writing_for_hsk_3(self) -> None:
        """Tests that HSK 3 requires Writing section.

        Args:
            None

        Returns:
            None
        """
        with pytest.raises(
            ValidationError, match="HSK level 3 requires a Writing section score"
        ):
            HSK(
                Level=3,
                Scores={"Listening": 90, "Reading": 85},
                DateTaken=date(2024, 3, 15),
                Link="https://chinesetest.cn/hsk",
            )

    def test_requires_writing_for_hsk_4(self) -> None:
        """Tests that HSK 4 requires Writing section.

        Args:
            None

        Returns:
            None
        """
        with pytest.raises(
            ValidationError, match="HSK level 4 requires a Writing section score"
        ):
            HSK(
                Level=4,
                Scores={"Listening": 90, "Reading": 85},
                DateTaken=date(2024, 3, 15),
                Link="https://chinesetest.cn/hsk",
            )

    def test_requires_writing_for_hsk_5(self) -> None:
        """Tests that HSK 5 requires Writing section.

        Args:
            None

        Returns:
            None
        """
        with pytest.raises(
            ValidationError, match="HSK level 5 requires a Writing section score"
        ):
            HSK(
                Level=5,
                Scores={"Listening": 90, "Reading": 85},
                DateTaken=date(2024, 3, 15),
                Link="https://chinesetest.cn/hsk",
            )

    def test_requires_writing_for_hsk_6(self) -> None:
        """Tests that HSK 6 requires Writing section.

        Args:
            None

        Returns:
            None
        """
        with pytest.raises(
            ValidationError, match="HSK level 6 requires a Writing section score"
        ):
            HSK(
                Level=6,
                Scores={"Listening": 90, "Reading": 85},
                DateTaken=date(2024, 3, 15),
                Link="https://chinesetest.cn/hsk",
            )


class TestHSKPassScoreValidation:
    """Tests for HSK pass score threshold validation."""

    @pytest.mark.parametrize(
        "level,pass_score",
        [
            (1, 120),
            (2, 120),
            (3, 180),
            (4, 180),
            (5, 180),
            (6, 180),
        ],
    )
    def test_rejects_total_below_passing(self, level: int, pass_score: int) -> None:
        """Tests that total scores below passing threshold are rejected.

        Args:
            level: HSK level.
            pass_score: Pass score threshold for the level.

        Returns:
            None
        """
        with pytest.raises(ValidationError, match="below passing score"):
            if level <= 2:
                HSK(
                    Level=level,
                    Scores={"Listening": 50, "Reading": 50},
                    DateTaken=date(2024, 3, 15),
                    Link="https://chinesetest.cn/hsk",
                )
            else:
                HSK(
                    Level=level,
                    Scores={"Listening": 50, "Reading": 50, "Writing": 50},
                    DateTaken=date(2024, 3, 15),
                    Link="https://chinesetest.cn/hsk",
                )


class TestHSKCEFRLevelComputation:
    """Tests for HSK CEFRLevel computed field."""

    @pytest.mark.parametrize(
        "level,expected_cefr",
        [
            (1, "A2"),
            (2, "A2"),
            (3, "B1"),
            (4, "B2"),
            (5, "C1"),
            (6, "C1"),
        ],
    )
    def test_cefr_level_mapping(self, level: int, expected_cefr: str) -> None:
        """Tests that CEFRLevel correctly maps from HSK level.

        Note: This mapping is preliminary as no official CEFR mapping
        has been published by Hanban/Chinese Testing International.

        Args:
            level: HSK exam level.
            expected_cefr: Expected CEFR level.

        Returns:
            None
        """
        if level <= 2:
            hsk = HSK(
                Level=level,
                Scores={"Listening": 80, "Reading": 80},
                DateTaken=date(2024, 3, 15),
                Link="https://chinesetest.cn/hsk",
            )
        else:
            hsk = HSK(
                Level=level,
                Scores={"Listening": 80, "Reading": 80, "Writing": 80},
                DateTaken=date(2024, 3, 15),
                Link="https://chinesetest.cn/hsk",
            )

        assert hsk.CEFRLevel == expected_cefr


class TestHSKModelValidation:
    """Tests for complete HSK model validation."""

    def test_accepts_valid_hsk_1_exam_record(self) -> None:
        """Tests that HSK accepts a valid HSK 1 exam record.

        Args:
            None

        Returns:
            None
        """
        hsk = HSK(
            Level=1,
            Scores={"Listening": 90, "Reading": 85},
            DateTaken=date(2024, 3, 15),
            Link="https://chinesetest.cn/hsk",
        )

        assert hsk.Level == 1
        assert hsk.Scores.Listening == 90
        assert hsk.Scores.Reading == 85
        assert hsk.Scores.Writing is None

    def test_accepts_valid_hsk_6_exam_record(self) -> None:
        """Tests that HSK accepts a valid HSK 6 exam record.

        Args:
            None

        Returns:
            None
        """
        hsk = HSK(
            Level=6,
            Scores={"Listening": 95, "Reading": 98, "Writing": 90},
            DateTaken=date(2024, 3, 15),
            Link="https://chinesetest.cn/hsk",
        )

        assert hsk.Level == 6
        assert hsk.Scores.Writing == 90

    def test_hsk_rejects_future_date(self) -> None:
        """Tests that HSK rejects future exam dates.

        Args:
            None

        Returns:
            None
        """
        future = date(2099, 1, 1)

        with pytest.raises(ValidationError, match="cannot be in the future"):
            HSK(
                Level=3,
                Scores={"Listening": 80, "Reading": 80, "Writing": 80},
                DateTaken=future,
                Link="https://chinesetest.cn/hsk",
            )


class TestPublicAPIIntegration:
    """Tests for HSK integration with public certificates API."""

    def test_hsk_importable_from_public_api(self) -> None:
        """Tests that HSK can be imported from pydanticcv.languages.certificates.

        Args:
            None

        Returns:
            None
        """
        from pydanticcv.languages.certificates import HSK

        hsk = HSK(
            Level=4,
            Scores={"Listening": 85, "Reading": 90, "Writing": 80},
            DateTaken=date(2024, 3, 15),
            Link="https://chinesetest.cn/hsk",
        )

        assert hsk.Level == 4
        assert hsk.CEFRLevel == "B2"
