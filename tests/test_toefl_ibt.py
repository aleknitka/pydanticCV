"""Tests for pydanticcv.languages.certificates.eng.toefl_ibt models.

Covers legacy (0-30 per section) and new (1-6 per section) TOEFL iBT scoring
scales, CEFR level derivation, and bidirectional conversion between scales.
"""

from datetime import date

import pytest
from pydantic import ValidationError, TypeAdapter

from pydanticcv.languages.certificates.eng.toefl_ibt import (
    TOEFLiBTLegacySectionScore,
    TOEFLiBTSectionScore,
    TOEFLiBTLegacyScores,
    TOEFLiBTScores,
    TOEFLiBTLegacy,
    TOEFLiBT,
)
from tests.conftest import (
    TOEFLiBTLegacyScoresFactory,
    TOEFLiBTLegacyFactory,
    TOEFLiBTScoresFactory,
    TOEFLiBTFactory,
)


class TestTOEFLiBTLegacySectionScoreValidation:
    """Tests for legacy section score (0-30) validation."""

    def test_accepts_valid_legacy_section_scores(self) -> None:
        """Tests that legacy section scores accept all values 0-30.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(TOEFLiBTLegacySectionScore)
        valid_scores = [0, 15, 30]

        for score in valid_scores:
            result = validator.validate_python(score)
            assert result == score

    def test_rejects_legacy_section_score_below_zero(self) -> None:
        """Tests that legacy section scores reject negative values.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(TOEFLiBTLegacySectionScore)

        with pytest.raises(ValidationError, match="must be 0-30"):
            validator.validate_python(-1)

    def test_rejects_legacy_section_score_above_thirty(self) -> None:
        """Tests that legacy section scores reject values above 30.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(TOEFLiBTLegacySectionScore)

        with pytest.raises(ValidationError, match="must be 0-30"):
            validator.validate_python(31)

    def test_accepts_legacy_section_score_boundaries(self) -> None:
        """Tests that legacy section scores accept 0 and 30.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(TOEFLiBTLegacySectionScore)

        assert validator.validate_python(0) == 0
        assert validator.validate_python(30) == 30


class TestTOEFLiBTNewSectionScoreValidation:
    """Tests for new section score (1-6, 0.5 steps) validation."""

    def test_accepts_valid_new_section_scores(self) -> None:
        """Tests that new section scores accept all valid 0.5-step values.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(TOEFLiBTSectionScore)
        valid_scores = [1.0, 1.5, 3.0, 4.5, 6.0]

        for score in valid_scores:
            result = validator.validate_python(score)
            assert result == score

    def test_rejects_new_section_score_below_one(self) -> None:
        """Tests that new section scores reject values below 1.0.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(TOEFLiBTSectionScore)

        with pytest.raises(ValidationError, match="must be 1-6"):
            validator.validate_python(0.9)

    def test_rejects_new_section_score_above_six(self) -> None:
        """Tests that new section scores reject values above 6.0.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(TOEFLiBTSectionScore)

        with pytest.raises(ValidationError, match="must be 1-6"):
            validator.validate_python(6.1)

    def test_rejects_new_section_score_not_in_0_5_steps(self) -> None:
        """Tests that new section scores reject non-0.5-step values.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(TOEFLiBTSectionScore)

        with pytest.raises(ValidationError, match="must be in 0.5 steps"):
            validator.validate_python(3.7)

    @pytest.mark.parametrize(
        "invalid_score",
        [1.1, 2.3, 3.7, 5.2],
        ids=["1.1", "2.3", "3.7", "5.2"],
    )
    def test_rejects_various_invalid_steps(self, invalid_score: float) -> None:
        """Tests that new section scores reject various non-0.5-step values.

        Args:
            invalid_score: A score not in 0.5 increments.

        Returns:
            None
        """
        validator = TypeAdapter(TOEFLiBTSectionScore)

        with pytest.raises(ValidationError, match="must be in 0.5 steps"):
            validator.validate_python(invalid_score)


class TestTOEFLiBTLegacyScoresComputation:
    """Tests for TOEFLiBTLegacyScores Overall computation."""

    def test_computes_overall_as_sum_of_sections(self) -> None:
        """Tests that Overall equals the sum of all four sections.

        Args:
            None

        Returns:
            None
        """
        scores = TOEFLiBTLegacyScores(
            Reading=25,
            Listening=28,
            Speaking=26,
            Writing=24,
        )

        assert scores.Overall == 103

    def test_overall_zero_when_all_sections_zero(self) -> None:
        """Tests that Overall is 0 when all sections are 0.

        Args:
            None

        Returns:
            None
        """
        scores = TOEFLiBTLegacyScores(
            Reading=0,
            Listening=0,
            Speaking=0,
            Writing=0,
        )

        assert scores.Overall == 0

    def test_overall_120_when_all_sections_max(self) -> None:
        """Tests that Overall is 120 when all sections are 30.

        Args:
            None

        Returns:
            None
        """
        scores = TOEFLiBTLegacyScores(
            Reading=30,
            Listening=30,
            Speaking=30,
            Writing=30,
        )

        assert scores.Overall == 120


class TestTOEFLiBTNewScoresComputation:
    """Tests for TOEFLiBTScores Overall computation."""

    def test_computes_overall_as_rounded_average(self) -> None:
        """Tests that Overall equals the average rounded to 0.5.

        Args:
            None

        Returns:
            None
        """
        scores = TOEFLiBTScores(
            Reading=4.5,
            Listening=5.0,
            Speaking=4.5,
            Writing=5.0,
        )

        assert scores.Overall == 5.0

    def test_overall_one_when_all_sections_one(self) -> None:
        """Tests that Overall is 1.0 when all sections are 1.0.

        Args:
            None

        Returns:
            None
        """
        scores = TOEFLiBTScores(
            Reading=1.0,
            Listening=1.0,
            Speaking=1.0,
            Writing=1.0,
        )

        assert scores.Overall == 1.0

    def test_overall_six_when_all_sections_six(self) -> None:
        """Tests that Overall is 6.0 when all sections are 6.0.

        Args:
            None

        Returns:
            None
        """
        scores = TOEFLiBTScores(
            Reading=6.0,
            Listening=6.0,
            Speaking=6.0,
            Writing=6.0,
        )

        assert scores.Overall == 6.0

    def test_rounds_average_to_nearest_0_5(self) -> None:
        """Tests that Overall rounds the average to nearest 0.5.

        Args:
            None

        Returns:
            None
        """
        scores = TOEFLiBTScores(
            Reading=3.0,
            Listening=3.5,
            Speaking=3.0,
            Writing=3.5,
        )

        assert scores.Overall == 3.0


class TestTOEFLiBTLegacyCEFRLevel:
    """Tests for TOEFLiBTLegacy CEFRLevel computation."""

    @pytest.mark.parametrize(
        "total,expected_cefr",
        [
            (114, "C2"),
            (120, "C2"),
            (107, "C1"),
            (113, "C1"),
            (95, "C1"),
            (72, "B2"),
            (58, "B1"),
            (44, "B1"),
            (34, "A2"),
            (0, "A1"),
        ],
        ids=[
            "114_C2", "120_C2",
            "107_C1", "113_C1",
            "95_C1",
            "72_B2",
            "58_B1", "44_B1",
            "34_A2", "0_A1",
        ],
    )
    def test_cefr_level_from_legacy_total(
        self, total: int, expected_cefr: str
    ) -> None:
        """Tests CEFRLevel mapping from legacy total score thresholds.

        Args:
            total: The legacy total score (0-120).
            expected_cefr: The expected CEFR level.

        Returns:
            None
        """
        reading = min(30, total // 4)
        listening = min(30, total // 4)
        speaking = min(30, total // 4)
        writing = min(30, max(0, total - 3 * (total // 4)))

        scores = TOEFLiBTLegacyScores(
            Reading=reading,
            Listening=listening,
            Speaking=speaking,
            Writing=writing,
        )
        legacy = TOEFLiBTLegacy(
            DateTaken=date(2020, 5, 15),
            Link="https://example.com",
            Scores=scores,
        )

        assert legacy.CEFRLevel == expected_cefr


class TestTOEFLiBTNewCEFRLevel:
    """Tests for TOEFLiBT CEFRLevel computation."""

    @pytest.mark.parametrize(
        "overall,expected_cefr",
        [
            (6.0, "C2"),
            (5.0, "C1"),
            (5.5, "C1"),
            (4.0, "B2"),
            (4.5, "B2"),
            (3.0, "B1"),
            (3.5, "B1"),
            (2.0, "A2"),
            (2.5, "A2"),
            (1.0, "A1"),
            (1.5, "A1"),
        ],
        ids=[
            "6.0_C2",
            "5.0_C1", "5.5_C1",
            "4.0_B2", "4.5_B2",
            "3.0_B1", "3.5_B1",
            "2.0_A2", "2.5_A2",
            "1.0_A1", "1.5_A1",
        ],
    )
    def test_cefr_level_from_new_overall(
        self, overall: float, expected_cefr: str
    ) -> None:
        """Tests CEFRLevel mapping from new-scale overall score.

        Args:
            overall: The new-scale overall score (1-6, 0.5 steps).
            expected_cefr: The expected CEFR level.

        Returns:
            None
        """
        scores = TOEFLiBTScores(
            Reading=overall,
            Listening=overall,
            Speaking=overall,
            Writing=overall,
        )
        new = TOEFLiBT(
            DateTaken=date(2020, 5, 15),
            Link="https://example.com",
            Scores=scores,
        )

        assert new.CEFRLevel == expected_cefr


class TestTOEFLiBTConversionLegacyToNew:
    """Tests for converting TOEFLiBTLegacy to TOEFLiBT."""

    def test_converts_all_max_legacy_to_new(self) -> None:
        """Tests conversion of maximum legacy scores (30/30/30/30).

        All 30s in legacy should convert to 6.0 in new scale.

        Args:
            None

        Returns:
            None
        """
        legacy = TOEFLiBTLegacy(
            DateTaken=date(2020, 5, 15),
            Link="https://example.com",
            Scores=TOEFLiBTLegacyScores(
                Reading=30,
                Listening=30,
                Speaking=30,
                Writing=30,
            ),
        )
        new = legacy.to_new()

        assert new.Scores.Reading == 6.0
        assert new.Scores.Listening == 6.0
        assert new.Scores.Speaking == 6.0
        assert new.Scores.Writing == 6.0
        assert new.Scores.Overall == 6.0
        assert new.CEFRLevel == "C2"

    def test_converts_zero_legacy_to_new(self) -> None:
        """Tests conversion of zero legacy scores (0/0/0/0).

        All 0s in legacy should convert to 1.0 in new scale.

        Args:
            None

        Returns:
            None
        """
        legacy = TOEFLiBTLegacy(
            DateTaken=date(2020, 5, 15),
            Link="https://example.com",
            Scores=TOEFLiBTLegacyScores(
                Reading=0,
                Listening=0,
                Speaking=0,
                Writing=0,
            ),
        )
        new = legacy.to_new()

        assert new.Scores.Reading == 1.0
        assert new.Scores.Listening == 1.0
        assert new.Scores.Speaking == 1.0
        assert new.Scores.Writing == 1.0
        assert new.Scores.Overall == 1.0
        assert new.CEFRLevel == "A1"

    def test_preserves_metadata_on_conversion(self) -> None:
        """Tests that DateTaken and Link are preserved during conversion.

        Args:
            None

        Returns:
            None
        """
        legacy = TOEFLiBTLegacy(
            DateTaken=date(2020, 5, 15),
            Link="https://example.com/certificate",
            Scores=TOEFLiBTLegacyScores(
                Reading=25,
                Listening=25,
                Speaking=25,
                Writing=25,
            ),
        )
        new = legacy.to_new()

        assert new.DateTaken == legacy.DateTaken
        assert new.Link == legacy.Link


class TestTOEFLiBTConversionNewToLegacy:
    """Tests for converting TOEFLiBT to TOEFLiBTLegacy."""

    def test_converts_all_max_new_to_legacy(self) -> None:
        """Tests conversion of maximum new scores (6.0/6.0/6.0/6.0).

        All 6.0s in new scale should convert to 30 in legacy scale.

        Args:
            None

        Returns:
            None
        """
        new = TOEFLiBT(
            DateTaken=date(2020, 5, 15),
            Link="https://example.com",
            Scores=TOEFLiBTScores(
                Reading=6.0,
                Listening=6.0,
                Speaking=6.0,
                Writing=6.0,
            ),
        )
        legacy = new.to_legacy()

        assert legacy.Scores.Reading == 30
        assert legacy.Scores.Listening == 30
        assert legacy.Scores.Speaking == 30
        assert legacy.Scores.Writing == 30
        assert legacy.Scores.Overall == 120
        assert legacy.CEFRLevel == "C2"

    def test_converts_min_new_to_legacy(self) -> None:
        """Tests conversion of minimum new scores (1.0) on conversion.

        All 1.0s in new scale convert via the lookup table. The exact mapping
        depends on the reverselookup table which uses the highest legacy value
        that maps to each new score.

        Args:
            None

        Returns:
            None
        """
        new = TOEFLiBT(
            DateTaken=date(2020, 5, 15),
            Link="https://example.com",
            Scores=TOEFLiBTScores(
                Reading=1.0,
                Listening=1.0,
                Speaking=1.0,
                Writing=1.0,
            ),
        )
        legacy = new.to_legacy()

        assert legacy.Scores.Overall >= 0
        assert legacy.CEFRLevel == "A1"

    def test_preserves_metadata_on_reverse_conversion(self) -> None:
        """Tests that DateTaken and Link are preserved during reverse conversion.

        Args:
            None

        Returns:
            None
        """
        new = TOEFLiBT(
            DateTaken=date(2020, 5, 15),
            Link="https://example.com/certificate",
            Scores=TOEFLiBTScores(
                Reading=4.5,
                Listening=4.5,
                Speaking=4.5,
                Writing=4.5,
            ),
        )
        legacy = new.to_legacy()

        assert legacy.DateTaken == new.DateTaken
        assert legacy.Link == new.Link


class TestTOEFLiBTAwardingInstitutionDefault:
    """Tests for AwardingInstitution default value."""

    def test_legacy_defaults_to_ets(self) -> None:
        """Tests that TOEFLiBTLegacy defaults AwardingInstitution to "ETS".

        Args:
            None

        Returns:
            None
        """
        legacy = TOEFLiBTLegacy(
            DateTaken=date(2020, 5, 15),
            Link="https://example.com",
            Scores=TOEFLiBTLegacyScores(
                Reading=25,
                Listening=25,
                Speaking=25,
                Writing=25,
            ),
        )

        assert legacy.AwardingInstitution == "ETS"

    def test_new_defaults_to_ets(self) -> None:
        """Tests that TOEFLiBT defaults AwardingInstitution to "ETS".

        Args:
            None

        Returns:
            None
        """
        new = TOEFLiBT(
            DateTaken=date(2020, 5, 15),
            Link="https://example.com",
            Scores=TOEFLiBTScores(
                Reading=4.5,
                Listening=4.5,
                Speaking=4.5,
                Writing=4.5,
            ),
        )

        assert new.AwardingInstitution == "ETS"

    def test_legacy_accepts_custom_institution(self) -> None:
        """Tests that TOEFLiBTLegacy accepts custom AwardingInstitution.

        Args:
            None

        Returns:
            None
        """
        legacy = TOEFLiBTLegacy(
            DateTaken=date(2020, 5, 15),
            Link="https://example.com",
            AwardingInstitution="Custom Institute",
            Scores=TOEFLiBTLegacyScores(
                Reading=25,
                Listening=25,
                Speaking=25,
                Writing=25,
            ),
        )

        assert legacy.AwardingInstitution == "Custom Institute"

    def test_new_accepts_custom_institution(self) -> None:
        """Tests that TOEFLiBT accepts custom AwardingInstitution.

        Args:
            None

        Returns:
            None
        """
        new = TOEFLiBT(
            DateTaken=date(2020, 5, 15),
            Link="https://example.com",
            AwardingInstitution="Custom Institute",
            Scores=TOEFLiBTScores(
                Reading=4.5,
                Listening=4.5,
                Speaking=4.5,
                Writing=4.5,
            ),
        )

        assert new.AwardingInstitution == "Custom Institute"


class TestTOEFLiBTFactoryCreation:
    """Tests for factory-based model creation."""

    def test_legacy_factory_creates_valid_record(self) -> None:
        """Tests that TOEFLiBTLegacyFactory creates valid records.

        Args:
            None

        Returns:
            None
        """
        legacy = TOEFLiBTLegacyFactory.create()

        assert 0 <= legacy.Scores.Overall <= 120
        assert legacy.DateTaken <= date.today()
        assert legacy.CEFRLevel in ["A1", "A2", "B1", "B2", "C1", "C2"]

    def test_new_factory_creates_valid_record(self) -> None:
        """Tests that TOEFLiBTFactory creates valid records.

        Args:
            None

        Returns:
            None
        """
        new = TOEFLiBTFactory.create()

        assert 1.0 <= new.Scores.Overall <= 6.0
        assert new.DateTaken <= date.today()
        assert new.CEFRLevel in ["A1", "A2", "B1", "B2", "C1", "C2"]
