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

from pydanticcv.activities.volunteering import VolunteeringActivity, VolunteeringArea
from pydanticcv.employment.breaks import EmploymentBreak
from pydanticcv.employment.record import EmploymentRecord
from pydanticcv.employment.types import EmploymentType
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
from pydanticcv.languages.self_reported import NativeLanguage, SelfReportedCEFR
from pydanticcv.projects.project import Project
from pydanticcv.publications.arxiv import ArxivPreprint
from pydanticcv.publications.journal import JournalArticle
from pydanticcv.references import Reference, RelationshipType
from pydanticcv.skills.skill import Skill, SkillType
from pydanticcv.skills.levels import SkillProficiencyLevel


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
        if "LanguageCertified" not in kwargs:
            kwargs["LanguageCertified"] = "eng"
        return cls.__model__(**kwargs)


class EmploymentRecordFactory(ModelFactory):
    """Factory for generating valid EmploymentRecord instances."""

    __model__ = EmploymentRecord

    @classmethod
    def create(cls, **kwargs) -> EmploymentRecord:
        """Create a valid EmploymentRecord instance.

        Args:
            **kwargs: Field overrides.

        Returns:
            A valid EmploymentRecord instance.
        """
        if "EmployerName" not in kwargs:
            kwargs["EmployerName"] = fake.company()
        if "Role" not in kwargs:
            kwargs["Role"] = fake.job()
        if "EmploymentType" not in kwargs:
            kwargs["EmploymentType"] = EmploymentType.EMPLOYEE
        if "StartDate" not in kwargs:
            kwargs["StartDate"] = fake.date_between(start_date="-10y", end_date="-2y")
        return cls.__model__(**kwargs)


class EmploymentBreakFactory(ModelFactory):
    """Factory for generating valid EmploymentBreak instances."""

    __model__ = EmploymentBreak

    @classmethod
    def create(cls, **kwargs) -> EmploymentBreak:
        """Create a valid EmploymentBreak instance.

        Args:
            **kwargs: Field overrides.

        Returns:
            A valid EmploymentBreak instance.
        """
        if "StartDate" not in kwargs:
            kwargs["StartDate"] = fake.date_between(start_date="-5y", end_date="-1y")
        return cls.__model__(**kwargs)


class SkillFactory(ModelFactory):
    """Factory for generating valid Skill instances."""

    __model__ = Skill

    @classmethod
    def create(cls, **kwargs) -> Skill:
        """Create a valid Skill instance.

        Args:
            **kwargs: Field overrides.

        Returns:
            A valid Skill instance.
        """
        if "Name" not in kwargs:
            kwargs["Name"] = fake.word().capitalize()
        if "Type" not in kwargs:
            kwargs["Type"] = SkillType.Technical
        if "Level" not in kwargs:
            kwargs["Level"] = SkillProficiencyLevel.Intermediate
        return cls.__model__(**kwargs)


class NativeLanguageFactory(ModelFactory):
    """Factory for generating valid NativeLanguage instances."""

    __model__ = NativeLanguage


class SelfReportedCEFRFactory(ModelFactory):
    """Factory for generating valid SelfReportedCEFR instances."""

    __model__ = SelfReportedCEFR


class ProjectFactory(ModelFactory):
    """Factory for generating valid Project instances."""

    __model__ = Project

    @classmethod
    def create(cls, **kwargs) -> Project:
        """Create a valid Project instance.

        Args:
            **kwargs: Field overrides.

        Returns:
            A valid Project instance.
        """
        if "Name" not in kwargs:
            kwargs["Name"] = fake.catch_phrase()
        if "Description" not in kwargs:
            kwargs["Description"] = fake.sentence(nb_words=10)
        if "StartDate" not in kwargs:
            kwargs["StartDate"] = fake.date_between(start_date="-5y", end_date="-1y")
        return cls.__model__(**kwargs)


class JournalArticleFactory(ModelFactory):
    """Factory for generating valid JournalArticle instances."""

    __model__ = JournalArticle

    @classmethod
    def create(cls, **kwargs) -> JournalArticle:
        """Create a valid JournalArticle instance.

        Args:
            **kwargs: Field overrides.

        Returns:
            A valid JournalArticle instance.
        """
        if "Title" not in kwargs:
            kwargs["Title"] = fake.sentence(nb_words=8)
        if "Authors" not in kwargs:
            kwargs["Authors"] = [fake.name() for _ in range(fake.random_int(min=1, max=5))]
        if "Year" not in kwargs:
            kwargs["Year"] = fake.random_int(min=2000, max=date.today().year)
        if "Journal" not in kwargs:
            kwargs["Journal"] = fake.catch_phrase()
        return cls.__model__(**kwargs)


class ArxivPreprintFactory(ModelFactory):
    """Factory for generating valid ArxivPreprint instances."""

    __model__ = ArxivPreprint

    @classmethod
    def create(cls, **kwargs) -> ArxivPreprint:
        """Create a valid ArxivPreprint instance.

        Args:
            **kwargs: Field overrides.

        Returns:
            A valid ArxivPreprint instance.
        """
        if "Title" not in kwargs:
            kwargs["Title"] = fake.sentence(nb_words=8)
        if "Authors" not in kwargs:
            kwargs["Authors"] = [fake.name() for _ in range(fake.random_int(min=1, max=5))]
        if "Year" not in kwargs:
            kwargs["Year"] = fake.random_int(min=2000, max=date.today().year)
        if "ArxivID" not in kwargs:
            kwargs["ArxivID"] = f"{fake.numerify('####')}.{fake.numerify('####')}"
        if "Categories" not in kwargs:
            kwargs["Categories"] = [fake.random_element(["cs.AI", "cs.LG", "stat.ML"])]
        if "Submitted" not in kwargs:
            kwargs["Submitted"] = fake.date_between(start_date="-5y", end_date="-1y")
        return cls.__model__(**kwargs)


class ReferenceFactory(ModelFactory):
    """Factory for generating valid Reference instances."""

    __model__ = Reference

    @classmethod
    def create(cls, **kwargs) -> Reference:
        """Create a valid Reference instance.

        Args:
            **kwargs: Field overrides.

        Returns:
            A valid Reference instance.
        """
        if "Name" not in kwargs:
            kwargs["Name"] = fake.name()
        if "Title" not in kwargs:
            kwargs["Title"] = fake.job()
        if "Organization" not in kwargs:
            kwargs["Organization"] = fake.company()
        if "Relationship" not in kwargs:
            kwargs["Relationship"] = fake.random_element(list(RelationshipType))
        return cls.__model__(**kwargs)


class VolunteeringActivityFactory(ModelFactory):
    """Factory for generating valid VolunteeringActivity instances."""

    __model__ = VolunteeringActivity

    @classmethod
    def create(cls, **kwargs) -> VolunteeringActivity:
        """Create a valid VolunteeringActivity instance.

        Args:
            **kwargs: Field overrides.

        Returns:
            A valid VolunteeringActivity instance.
        """
        if "Organisation" not in kwargs:
            kwargs["Organisation"] = fake.company()
        if "Role" not in kwargs:
            kwargs["Role"] = fake.random_element(["Volunteer", "Coordinator", "Mentor"])
        if "Area" not in kwargs:
            kwargs["Area"] = VolunteeringArea.Community
        if "StartDate" not in kwargs:
            kwargs["StartDate"] = fake.date_between(start_date="-5y", end_date="-1y")
        if "Description" not in kwargs:
            kwargs["Description"] = fake.sentence(nb_words=12)
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
