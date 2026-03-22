"""Shared pytest fixtures and factories for the pydanticCV test suite.

This module provides reusable fixtures and polyfactory-based factories
for constructing valid test instances of all models.
"""

from datetime import date
from typing import Any

import pytest
from faker import Faker
from polyfactory.factories.pydantic_factory import ModelFactory
from pydantic import AnyUrl

from pydanticcv.languages.certificates.eng.ielts import (
    IELTS,
    IELTSScores,
)
from pydanticcv.languages.certificates.eng.toefl_ibt import (
    TOEFLiBT,
    TOEFLiBTScores,
    TOEFLiBTLegacy,
    TOEFLiBTLegacyScores,
)
from pydanticcv.languages.certificates.eng.toefl_itp import (
    TOEFLITP,
    TOEFLITPScores,
)


fake = Faker()


@pytest.fixture
def past_date() -> date:
    """Provides a valid past date for exam records.

    Returns:
        A date between 5 and 1 years ago.
    """
    return fake.date_between(start_date="-5y", end_date="-1y")


@pytest.fixture
def valid_url() -> AnyUrl:
    """Provides a valid URL for certificate links.

    Returns:
        A generated URL string as AnyUrl.
    """
    return AnyUrl(fake.url())


class IELTSScoresFactory(ModelFactory):
    """Factory for generating valid IELTSScores instances.

    Overrides the Overall field to ensure it matches the average of the
    four section scores, as required by the model validator.
    """

    __model__ = IELTSScores

    @classmethod
    def create(cls, **kwargs: Any) -> IELTSScores:
        """Create a valid IELTSScores instance.

        If Listening, Reading, Writing, and Speaking are provided,
        Overall is automatically computed to match their average.
        Otherwise, all five scores are generated randomly.

        Args:
            **kwargs: Field overrides.

        Returns:
            A valid IELTSScores instance with consistent Overall.
        """
        if any(k in kwargs for k in ["Listening", "Reading", "Writing", "Speaking"]):
            listening = kwargs.get(
                "Listening",
                fake.random_element(
                    [v for v in [x * 0.5 for x in range(0, 19)] if 0 <= v <= 9]
                ),
            )  # noqa: E501
            reading = kwargs.get(
                "Reading",
                fake.random_element(
                    [v for v in [x * 0.5 for x in range(0, 19)] if 0 <= v <= 9]
                ),
            )  # noqa: E501
            writing = kwargs.get(
                "Writing",
                fake.random_element(
                    [v for v in [x * 0.5 for x in range(0, 19)] if 0 <= v <= 9]
                ),
            )  # noqa: E501
            speaking = kwargs.get(
                "Speaking",
                fake.random_element(
                    [v for v in [x * 0.5 for x in range(0, 19)] if 0 <= v <= 9]
                ),
            )  # noqa: E501
            overall = round((listening + reading + writing + speaking) / 4 * 2) / 2
            return IELTSScores(
                Listening=listening,
                Reading=reading,
                Writing=writing,
                Speaking=speaking,
                Overall=overall,
            )
        return IELTSScores(
            Listening=5.5,
            Reading=6.0,
            Writing=5.5,
            Speaking=6.0,
            Overall=6.0,
        )


class IELTSFactory(ModelFactory):
    """Factory for generating valid IELTS exam records."""

    __model__ = IELTS

    @classmethod
    def create(cls, **kwargs) -> IELTS:
        """Create a valid IELTS instance with consistent scores.

        Args:
            **kwargs: Field overrides.

        Returns:
            A valid IELTS instance.
        """
        if "Scores" not in kwargs:
            kwargs["Scores"] = IELTSScoresFactory.create()
        if "DateTaken" not in kwargs:
            kwargs["DateTaken"] = fake.date_between(start_date="-5y", end_date="-1y")
        if "Link" not in kwargs:
            kwargs["Link"] = AnyUrl(fake.url())
        if "ExamType" not in kwargs:
            kwargs["ExamType"] = fake.random_element(["Academic", "General Training"])
        return cls.__model__(**kwargs)


class TOEFLiBTLegacyScoresFactory(ModelFactory):
    """Factory for generating valid TOEFLiBTLegacyScores instances.

    Uses fixed mid-range values to ensure Overall (computed) is valid.
    """

    __model__ = TOEFLiBTLegacyScores

    @classmethod
    def create(cls, **kwargs) -> TOEFLiBTLegacyScores:
        """Create a valid TOEFLiBTLegacyScores instance.

        Args:
            **kwargs: Field overrides.

        Returns:
            A valid TOEFLiBTLegacyScores instance.
        """
        if "Reading" not in kwargs:
            kwargs["Reading"] = 25
        if "Listening" not in kwargs:
            kwargs["Listening"] = 25
        if "Speaking" not in kwargs:
            kwargs["Speaking"] = 25
        if "Writing" not in kwargs:
            kwargs["Writing"] = 25
        return cls.__model__(**kwargs)


class TOEFLiBTLegacyFactory(ModelFactory):
    """Factory for generating valid TOEFLiBTLegacy exam records."""

    __model__ = TOEFLiBTLegacy

    @classmethod
    def create(cls, **kwargs) -> TOEFLiBTLegacy:
        """Create a valid TOEFLiBTLegacy instance.

        Args:
            **kwargs: Field overrides.

        Returns:
            A valid TOEFLiBTLegacy instance.
        """
        if "Scores" not in kwargs:
            kwargs["Scores"] = TOEFLiBTLegacyScoresFactory.create()
        if "DateTaken" not in kwargs:
            kwargs["DateTaken"] = fake.date_between(start_date="-5y", end_date="-1y")
        if "Link" not in kwargs:
            kwargs["Link"] = AnyUrl(fake.url())
        return cls.__model__(**kwargs)


class TOEFLiBTScoresFactory(ModelFactory):
    """Factory for generating valid TOEFLiBTScores instances.

    Uses fixed mid-range values (4.5) to ensure Overall is valid.
    """

    __model__ = TOEFLiBTScores

    @classmethod
    def create(cls, **kwargs) -> TOEFLiBTScores:
        """Create a valid TOEFLiBTScores instance.

        Args:
            **kwargs: Field overrides.

        Returns:
            A valid TOEFLiBTScores instance.
        """
        if "Reading" not in kwargs:
            kwargs["Reading"] = 4.5
        if "Listening" not in kwargs:
            kwargs["Listening"] = 4.5
        if "Speaking" not in kwargs:
            kwargs["Speaking"] = 4.5
        if "Writing" not in kwargs:
            kwargs["Writing"] = 4.5
        return cls.__model__(**kwargs)


class TOEFLiBTFactory(ModelFactory):
    """Factory for generating valid TOEFLiBT exam records."""

    __model__ = TOEFLiBT

    @classmethod
    def create(cls, **kwargs) -> TOEFLiBT:
        """Create a valid TOEFLiBT instance.

        Args:
            **kwargs: Field overrides.

        Returns:
            A valid TOEFLiBT instance.
        """
        if "Scores" not in kwargs:
            kwargs["Scores"] = TOEFLiBTScoresFactory.create()
        if "DateTaken" not in kwargs:
            kwargs["DateTaken"] = fake.date_between(start_date="-5y", end_date="-1y")
        if "Link" not in kwargs:
            kwargs["Link"] = AnyUrl(fake.url())
        return cls.__model__(**kwargs)


class TOEFLITPLevel1ScoresFactory(ModelFactory):
    """Factory for generating TOEFLITPScores valid for Level 1.

    Uses fixed mid-range values (50, 50, 50) to produce a valid total
    for Level 1 (310-677): round((50+50+50)*10/3) = 500.
    """

    __model__ = TOEFLITPScores

    @classmethod
    def create(cls, **kwargs) -> TOEFLITPScores:
        """Create a valid Level 1 TOEFLITPScores instance.

        Args:
            **kwargs: Field overrides.

        Returns:
            A valid TOEFLITPScores instance for Level 1.
        """
        if "ListeningComprehension" not in kwargs:
            kwargs["ListeningComprehension"] = 50
        if "StructureWrittenExpression" not in kwargs:
            kwargs["StructureWrittenExpression"] = 50
        if "ReadingComprehension" not in kwargs:
            kwargs["ReadingComprehension"] = 50
        return cls.__model__(**kwargs)


class TOEFLITPLevel2ScoresFactory(ModelFactory):
    """Factory for generating TOEFLITPScores valid for Level 2.

    Uses fixed mid-range values (30, 30, 30) to produce a valid total
    for Level 2 (200-500): round((30+30+30)*10/3) = 300.
    """

    __model__ = TOEFLITPScores

    @classmethod
    def create(cls, **kwargs) -> TOEFLITPScores:
        """Create a valid Level 2 TOEFLITPScores instance.

        Args:
            **kwargs: Field overrides.

        Returns:
            A valid TOEFLITPScores instance for Level 2.
        """
        if "ListeningComprehension" not in kwargs:
            kwargs["ListeningComprehension"] = 30
        if "StructureWrittenExpression" not in kwargs:
            kwargs["StructureWrittenExpression"] = 30
        if "ReadingComprehension" not in kwargs:
            kwargs["ReadingComprehension"] = 30
        return cls.__model__(**kwargs)


class TOEFLITPLevel1Factory(ModelFactory):
    """Factory for generating valid TOEFLITP Level 1 exam records."""

    __model__ = TOEFLITP

    @classmethod
    def create(cls, **kwargs) -> TOEFLITP:
        """Create a valid Level 1 TOEFLITP instance.

        Args:
            **kwargs: Field overrides.

        Returns:
            A valid TOEFLITP Level 1 instance.
        """
        if "Level" not in kwargs:
            kwargs["Level"] = "Level 1"
        if "Scores" not in kwargs:
            kwargs["Scores"] = TOEFLITPLevel1ScoresFactory.create()
        if "DateTaken" not in kwargs:
            kwargs["DateTaken"] = fake.date_between(start_date="-5y", end_date="-1y")
        if "Link" not in kwargs:
            kwargs["Link"] = AnyUrl(fake.url())
        return cls.__model__(**kwargs)


class TOEFLITPLevel2Factory(ModelFactory):
    """Factory for generating valid TOEFLITP Level 2 exam records."""

    __model__ = TOEFLITP

    @classmethod
    def create(cls, **kwargs) -> TOEFLITP:
        """Create a valid Level 2 TOEFLITP instance.

        Args:
            **kwargs: Field overrides.

        Returns:
            A valid TOEFLITP Level 2 instance.
        """
        if "Level" not in kwargs:
            kwargs["Level"] = "Level 2"
        if "Scores" not in kwargs:
            kwargs["Scores"] = TOEFLITPLevel2ScoresFactory.create()
        if "DateTaken" not in kwargs:
            kwargs["DateTaken"] = fake.date_between(start_date="-5y", end_date="-1y")
        if "Link" not in kwargs:
            kwargs["Link"] = AnyUrl(fake.url())
        return cls.__model__(**kwargs)
