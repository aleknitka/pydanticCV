"""Tests for pydanticcv.languages.certificates.eng.toefl_itp models.

Covers TOEFL ITP section scores, total computation, level-dependent total
range validation, and CEFR level derivation (Level 1 only).
"""

from datetime import date

import pytest
from pydantic import ValidationError, TypeAdapter

from pydanticcv.languages.certificates.eng.toefl_itp import (
    TOEFLITPLevel,
    TOEFLITPSectionScore,
    TOEFLITPScores,
    TOEFLITP,
)
from tests.conftest import (
    TOEFLITPLevel1Factory,
    TOEFLITPLevel2Factory,
)


class TestTOEFLITPLevelValidation:
    """Tests for TOEFLITPLevel literal validation."""

    def test_accepts_level_1(self) -> None:
        """Tests that TOEFLITPLevel accepts "Level 1".

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(TOEFLITPLevel)
        result = validator.validate_python("Level 1")

        assert result == "Level 1"

    def test_accepts_level_2(self) -> None:
        """Tests that TOEFLITPLevel accepts "Level 2".

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(TOEFLITPLevel)
        result = validator.validate_python("Level 2")

        assert result == "Level 2"

    def test_rejects_invalid_level(self) -> None:
        """Tests that TOEFLITPLevel rejects invalid level strings.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(TOEFLITPLevel)

        with pytest.raises(ValidationError, match="Input should be"):
            validator.validate_python("Level 3")


class TestTOEFLITPSectionScoreValidation:
    """Tests for TOEFL ITP section score (16-68) validation."""

    def test_accepts_valid_section_scores(self) -> None:
        """Tests that section scores accept all values 16-68.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(TOEFLITPSectionScore)
        valid_scores = [16, 40, 68]

        for score in valid_scores:
            result = validator.validate_python(score)
            assert result == score

    def test_rejects_section_score_below_sixteen(self) -> None:
        """Tests that section scores reject values below 16.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(TOEFLITPSectionScore)

        with pytest.raises(ValidationError, match="must be 16-68"):
            validator.validate_python(15)

    def test_rejects_section_score_above_sixty_eight(self) -> None:
        """Tests that section scores reject values above 68.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(TOEFLITPSectionScore)

        with pytest.raises(ValidationError, match="must be 16-68"):
            validator.validate_python(69)

    def test_accepts_section_score_boundaries(self) -> None:
        """Tests that section scores accept 16 and 68.

        Args:
            None

        Returns:
            None
        """
        validator = TypeAdapter(TOEFLITPSectionScore)

        assert validator.validate_python(16) == 16
        assert validator.validate_python(68) == 68


class TestTOEFLITPScoresComputation:
    """Tests for TOEFLITPScores Total computation."""

    def test_computes_total_from_three_sections(self) -> None:
        """Tests that Total = round((L + S + R) * 10 / 3).

        Args:
            None

        Returns:
            None
        """
        scores = TOEFLITPScores(
            ListeningComprehension=50,
            StructureWrittenExpression=50,
            ReadingComprehension=50,
        )

        assert scores.Total == 500

    def test_computes_total_at_min_boundary(self) -> None:
        """Tests Total computation at minimum section values.

        Args:
            None

        Returns:
            None
        """
        scores = TOEFLITPScores(
            ListeningComprehension=16,
            StructureWrittenExpression=16,
            ReadingComprehension=16,
        )

        assert scores.Total == 160

    def test_computes_total_at_max_boundary(self) -> None:
        """Tests Total computation at maximum section values.

        Args:
            None

        Returns:
            None
        """
        scores = TOEFLITPScores(
            ListeningComprehension=68,
            StructureWrittenExpression=68,
            ReadingComprehension=68,
        )

        assert scores.Total == 680

    def test_total_rounds_correctly(self) -> None:
        """Tests that Total rounds (L+S+R)*10/3 correctly.

        For sections (30, 30, 30): (30+30+30)*10/3 = 300.
        For sections (31, 31, 31): (31+31+31)*10/3 = 310.

        Args:
            None

        Returns:
            None
        """
        scores1 = TOEFLITPScores(
            ListeningComprehension=30,
            StructureWrittenExpression=30,
            ReadingComprehension=30,
        )
        scores2 = TOEFLITPScores(
            ListeningComprehension=31,
            StructureWrittenExpression=31,
            ReadingComprehension=31,
        )

        assert scores1.Total == 300
        assert scores2.Total == 310


class TestTOEFLITPLevel1TotalRangeValidation:
    """Tests for Level 1 total score range validation (310-677)."""

    def test_accepts_level_1_total_in_valid_range(self) -> None:
        """Tests that Level 1 accepts total in valid range.

        Args:
            None

        Returns:
            None
        """
        itp = TOEFLITP(
            Level="Level 1",
            DateTaken=date(2020, 5, 15),
            Link="https://example.com",
            Scores=TOEFLITPScores(
                ListeningComprehension=50,
                StructureWrittenExpression=50,
                ReadingComprehension=50,
            ),
        )

        assert 310 <= itp.Scores.Total <= 677

    def test_rejects_level_1_total_below_min(self) -> None:
        """Tests that Level 1 rejects total below 310.

        Args:
            None

        Returns:
            None
        """
        with pytest.raises(
            ValidationError, match="Level 1 total score must be 310-677"
        ):
            TOEFLITP(
                Level="Level 1",
                DateTaken=date(2020, 5, 15),
                Link="https://example.com",
                Scores=TOEFLITPScores(
                    ListeningComprehension=16,
                    StructureWrittenExpression=16,
                    ReadingComprehension=16,
                ),
            )


class TestTOEFLITPLevel2TotalRangeValidation:
    """Tests for Level 2 total score range validation (200-500)."""

    def test_accepts_level_2_total_in_valid_range(self) -> None:
        """Tests that Level 2 accepts total in valid range.

        Args:
            None

        Returns:
            None
        """
        itp = TOEFLITP(
            Level="Level 2",
            DateTaken=date(2020, 5, 15),
            Link="https://example.com",
            Scores=TOEFLITPScores(
                ListeningComprehension=30,
                StructureWrittenExpression=30,
                ReadingComprehension=30,
            ),
        )

        assert 200 <= itp.Scores.Total <= 500

    def test_rejects_level_2_total_below_min(self) -> None:
        """Tests that Level 2 rejects total below 200.

        Args:
            None

        Returns:
            None
        """
        with pytest.raises(
            ValidationError, match="Level 2 total score must be 200-500"
        ):
            TOEFLITP(
                Level="Level 2",
                DateTaken=date(2020, 5, 15),
                Link="https://example.com",
                Scores=TOEFLITPScores(
                    ListeningComprehension=16,
                    StructureWrittenExpression=16,
                    ReadingComprehension=16,
                ),
            )

    def test_rejects_level_2_total_above_max(self) -> None:
        """Tests that Level 2 rejects total above 500.

        Args:
            None

        Returns:
            None
        """
        with pytest.raises(
            ValidationError, match="Level 2 total score must be 200-500"
        ):
            TOEFLITP(
                Level="Level 2",
                DateTaken=date(2020, 5, 15),
                Link="https://example.com",
                Scores=TOEFLITPScores(
                    ListeningComprehension=68,
                    StructureWrittenExpression=68,
                    ReadingComprehension=68,
                ),
            )


class TestTOEFLITPLevel1CEFRLevel:
    """Tests for TOEFLITP Level 1 CEFRLevel computation."""

    def test_cefr_c1_at_high_level_1_score(self) -> None:
        """Tests that Level 1 high scores map to C1 CEFR level.

        Args:
            None

        Returns:
            None
        """
        itp = TOEFLITP(
            Level="Level 1",
            DateTaken=date(2020, 5, 15),
            Link="https://example.com",
            Scores=TOEFLITPScores(
                ListeningComprehension=60,
                StructureWrittenExpression=60,
                ReadingComprehension=60,
            ),
        )

        assert itp.CEFRLevel == "C1"

    def test_cefr_b2_at_mid_level_1_score(self) -> None:
        """Tests that Level 1 mid scores map to B2 CEFR level.

        Args:
            None

        Returns:
            None
        """
        itp = TOEFLITP(
            Level="Level 1",
            DateTaken=date(2020, 5, 15),
            Link="https://example.com",
            Scores=TOEFLITPScores(
                ListeningComprehension=50,
                StructureWrittenExpression=50,
                ReadingComprehension=50,
            ),
        )

        assert itp.CEFRLevel == "B2"

    def test_cefr_b1_at_low_mid_level_1_score(self) -> None:
        """Tests that Level 1 low-mid scores map to B1 CEFR level.

        Args:
            None

        Returns:
            None
        """
        itp = TOEFLITP(
            Level="Level 1",
            DateTaken=date(2020, 5, 15),
            Link="https://example.com",
            Scores=TOEFLITPScores(
                ListeningComprehension=35,
                StructureWrittenExpression=35,
                ReadingComprehension=35,
            ),
        )

        assert itp.CEFRLevel == "B1"

    def test_cefr_a2_at_low_level_1_score(self) -> None:
        """Tests that Level 1 low scores map to A2 CEFR level.

        For a total of 310 at the minimum: (310/3) = 103.33, so 31+31+31*10/3 = 310.

        Args:
            None

        Returns:
            None
        """
        itp = TOEFLITP(
            Level="Level 1",
            DateTaken=date(2020, 5, 15),
            Link="https://example.com",
            Scores=TOEFLITPScores(
                ListeningComprehension=31,
                StructureWrittenExpression=31,
                ReadingComprehension=31,
            ),
        )

        assert itp.CEFRLevel == "A2"

    def test_level_1_cefr_is_not_none(self) -> None:
        """Tests that Level 1 always has a CEFRLevel value.

        Args:
            None

        Returns:
            None
        """
        itp = TOEFLITP(
            Level="Level 1",
            DateTaken=date(2020, 5, 15),
            Link="https://example.com",
            Scores=TOEFLITPScores(
                ListeningComprehension=50,
                StructureWrittenExpression=50,
                ReadingComprehension=50,
            ),
        )

        assert itp.CEFRLevel is not None


class TestTOEFLITPLevel2CEFRLevel:
    """Tests for TOEFLITP Level 2 CEFRLevel computation."""

    def test_level_2_cefr_is_none(self) -> None:
        """Tests that Level 2 always has CEFRLevel = None.

        Args:
            None

        Returns:
            None
        """
        itp = TOEFLITP(
            Level="Level 2",
            DateTaken=date(2020, 5, 15),
            Link="https://example.com",
            Scores=TOEFLITPScores(
                ListeningComprehension=30,
                StructureWrittenExpression=30,
                ReadingComprehension=30,
            ),
        )

        assert itp.CEFRLevel is None

    def test_level_2_cefr_none_regardless_of_score(self) -> None:
        """Tests that Level 2 CEFRLevel is None even at high scores.

        Args:
            None

        Returns:
            None
        """
        itp = TOEFLITP(
            Level="Level 2",
            DateTaken=date(2020, 5, 15),
            Link="https://example.com",
            Scores=TOEFLITPScores(
                ListeningComprehension=50,
                StructureWrittenExpression=50,
                ReadingComprehension=50,
            ),
        )

        assert itp.CEFRLevel is None


class TestTOEFLITPAwardingInstitutionDefault:
    """Tests for AwardingInstitution default value."""

    def test_defaults_to_ets(self) -> None:
        """Tests that TOEFLITP defaults AwardingInstitution to "ETS".

        Args:
            None

        Returns:
            None
        """
        itp = TOEFLITP(
            Level="Level 1",
            DateTaken=date(2020, 5, 15),
            Link="https://example.com",
            Scores=TOEFLITPScores(
                ListeningComprehension=50,
                StructureWrittenExpression=50,
                ReadingComprehension=50,
            ),
        )

        assert itp.AwardingInstitution == "ETS"

    def test_accepts_custom_institution(self) -> None:
        """Tests that TOEFLITP accepts custom AwardingInstitution.

        Args:
            None

        Returns:
            None
        """
        itp = TOEFLITP(
            Level="Level 1",
            DateTaken=date(2020, 5, 15),
            Link="https://example.com",
            AwardingInstitution="Custom Institute",
            Scores=TOEFLITPScores(
                ListeningComprehension=50,
                StructureWrittenExpression=50,
                ReadingComprehension=50,
            ),
        )

        assert itp.AwardingInstitution == "Custom Institute"


class TestTOEFLITPFactoryCreation:
    """Tests for factory-based model creation."""

    def test_level_1_factory_creates_valid_record(self) -> None:
        """Tests that TOEFLITPLevel1Factory creates valid Level 1 records.

        Args:
            None

        Returns:
            None
        """
        itp = TOEFLITPLevel1Factory.create()

        assert itp.Level == "Level 1"
        assert 310 <= itp.Scores.Total <= 677
        assert itp.CEFRLevel in ["A2", "B1", "B2", "C1"]

    def test_level_2_factory_creates_valid_record(self) -> None:
        """Tests that TOEFLITPLevel2Factory creates valid Level 2 records.

        Args:
            None

        Returns:
            None
        """
        itp = TOEFLITPLevel2Factory.create()

        assert itp.Level == "Level 2"
        assert 200 <= itp.Scores.Total <= 500
        assert itp.CEFRLevel is None

    def test_factories_create_distinct_records(self) -> None:
        """Tests that factories create independent record instances.

        Args:
            None

        Returns:
            None
        """
        itp1 = TOEFLITPLevel1Factory.create()
        itp2 = TOEFLITPLevel1Factory.create()

        assert itp1 is not itp2
        assert itp1.Scores is not itp2.Scores
