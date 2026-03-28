"""Tests for pydanticcv.cv models.

Covers Name, ContactInfo, PersonalInfo, CVAddress, and CV, including
integration with all other CV section models.
"""

import pytest
from pydantic import ValidationError

from pydanticcv.cv.cv import CV
from pydanticcv.cv.personal_info import ContactInfo, Name, PersonalInfo
from pydanticcv.education import EducationRecord
from pydanticcv.employment import EmploymentHistory
from pydanticcv.languages import NativeLanguage, SelfReportedCEFR
from pydanticcv.languages.certificates import IELTS
from pydanticcv.projects import Project
from pydanticcv.publications import ArxivPreprint, JournalArticle
from pydanticcv.skills import Skill
from pydanticcv.skills.levels import SkillProficiencyLevel
from pydanticcv.skills.skill import SkillType
from pydanticcv.activities import VolunteeringActivity
from pydanticcv.references import Reference, RelationshipType
from pydanticcv.awards import Award
from pydanticcv.utils.locations import CVAddress, Country

from tests.conftest import (
    ArxivPreprintFactory,
    EmploymentBreakFactory,
    EmploymentRecordFactory,
    IELTSFactory,
    JournalArticleFactory,
    ProjectFactory,
    ReferenceFactory,
    SkillFactory,
    VolunteeringActivityFactory,
    AwardFactory,
)


class TestCVAddress:
    """Tests for the CVAddress model."""

    def test_all_fields_none_by_default(self) -> None:
        addr = CVAddress()
        assert addr.City is None
        assert addr.Country is None

    def test_accepts_city_only(self) -> None:
        addr = CVAddress(City="London")
        assert addr.City == "London"
        assert addr.Country is None

    def test_accepts_country_only(self) -> None:
        country = Country(name="United Kingdom", iso="GBR")
        addr = CVAddress(Country=country)
        assert addr.Country.iso == "GBR"
        assert addr.City is None

    def test_accepts_both_fields(self) -> None:
        country = Country(name="France", iso="FRA")
        addr = CVAddress(City="Paris", Country=country)
        assert addr.City == "Paris"
        assert addr.Country.name == "France"


class TestName:
    """Tests for the Name model."""

    def test_requires_family_name(self) -> None:
        with pytest.raises(ValidationError):
            Name()

    def test_family_name_only(self) -> None:
        name = Name(FamilyName="Smith")
        assert name.FamilyName == "Smith"
        assert name.Title is None
        assert name.GivenNames is None
        assert name.MiddleName is None
        assert name.PreferredName is None

    def test_all_fields(self) -> None:
        name = Name(
            Title="Dr.",
            FamilyName="Smith",
            GivenNames=["Alice", "Jane"],
            MiddleName="Marie",
            PreferredName="Ali",
        )
        assert name.Title == "Dr."
        assert name.GivenNames == ["Alice", "Jane"]
        assert name.MiddleName == "Marie"
        assert name.PreferredName == "Ali"


class TestContactInfo:
    """Tests for the ContactInfo model."""

    def test_all_fields_optional(self) -> None:
        contact = ContactInfo()
        assert contact.Email is None
        assert contact.Phone is None
        assert contact.Website is None
        assert contact.LinkedIn is None
        assert contact.GitHub is None
        assert contact.OtherUrls == []

    def test_valid_email(self) -> None:
        contact = ContactInfo(Email="alice@example.com")
        assert contact.Email == "alice@example.com"

    def test_invalid_email_rejected(self) -> None:
        with pytest.raises(ValidationError):
            ContactInfo(Email="not-an-email")

    def test_valid_phone(self) -> None:
        contact = ContactInfo(Phone="+442071234567")
        assert contact.Phone is not None

    def test_invalid_phone_rejected(self) -> None:
        with pytest.raises(ValidationError):
            ContactInfo(Phone="not-a-phone")

    def test_valid_urls(self) -> None:
        contact = ContactInfo(
            Website="https://alice.dev",
            LinkedIn="https://linkedin.com/in/alice",
            GitHub="https://github.com/alice",
            OtherUrls=["https://example.com"],
        )
        assert contact.GitHub is not None
        assert len(contact.OtherUrls) == 1


class TestPersonalInfo:
    """Tests for the PersonalInfo model."""

    def test_requires_name(self) -> None:
        with pytest.raises(ValidationError):
            PersonalInfo()

    def test_name_only(self) -> None:
        pi = PersonalInfo(Name=Name(FamilyName="Smith"))
        assert pi.Name.FamilyName == "Smith"
        assert pi.Contact is None
        assert pi.Address is None
        assert pi.Photo is None

    def test_all_fields(self) -> None:
        pi = PersonalInfo(
            Name=Name(FamilyName="Smith", GivenNames=["Alice"]),
            Contact=ContactInfo(Email="alice@example.com"),
            Address=CVAddress(City="London"),
            Photo="https://example.com/photo.jpg",
        )
        assert pi.Name.GivenNames == ["Alice"]
        assert pi.Contact.Email == "alice@example.com"
        assert pi.Address.City == "London"
        assert pi.Photo is not None


class TestCV:
    """Tests for the top-level CV model."""

    def test_requires_personal_info(self) -> None:
        with pytest.raises(ValidationError):
            CV()

    def test_minimal_cv(self) -> None:
        cv = CV(PersonalInfo=PersonalInfo(Name=Name(FamilyName="Smith")))
        assert cv.PersonalInfo.Name.FamilyName == "Smith"

    def test_round_trip_json(self) -> None:
        cv = CV(
            PersonalInfo=PersonalInfo(
                Name=Name(
                    Title="Dr.",
                    FamilyName="Smith",
                    GivenNames=["Alice"],
                ),
                Contact=ContactInfo(Email="alice@example.com"),
                Address=CVAddress(City="London"),
            )
        )
        json_str = cv.model_dump_json()
        cv2 = CV.model_validate_json(json_str)
        assert cv2.PersonalInfo.Name.FamilyName == "Smith"
        assert cv2.PersonalInfo.Contact.Email == "alice@example.com"


class TestPublicAPI:
    """Tests that the public API re-exports are correct."""

    def test_imports_from_cv_package(self) -> None:
        from pydanticcv.cv import CV, PersonalInfo, Name, ContactInfo  # noqa: F401
        assert CV is not None
        assert PersonalInfo is not None
        assert Name is not None
        assert ContactInfo is not None

    def test_imports_employment_types_from_cv_package(self) -> None:
        from pydanticcv.cv import EmploymentHistory  # noqa: F401
        assert EmploymentHistory is not None

    def test_imports_skill_from_cv_package(self) -> None:
        from pydanticcv.cv import Skill  # noqa: F401
        assert Skill is not None

    def test_imports_project_from_cv_package(self) -> None:
        from pydanticcv.cv import Project  # noqa: F401
        assert Project is not None

    def test_imports_publication_from_cv_package(self) -> None:
        from pydanticcv.cv import Publication  # noqa: F401
        assert Publication is not None

    def test_imports_volunteering_activity_from_cv_package(self) -> None:
        from pydanticcv.cv import VolunteeringActivity  # noqa: F401
        assert VolunteeringActivity is not None


class TestCVEmploymentHistory:
    """Tests for CV with EmploymentHistory."""

    def test_cv_with_employment_history(self) -> None:
        record = EmploymentRecordFactory.create()
        history = EmploymentHistory(Records=[record])
        cv = CV(
            PersonalInfo=PersonalInfo(Name=Name(FamilyName="Smith")),
            EmploymentHistory=history,
        )
        assert cv.EmploymentHistory is not None
        assert len(cv.EmploymentHistory.Records) == 1

    def test_cv_with_employment_history_and_break(self) -> None:
        record = EmploymentRecordFactory.create()
        break_record = EmploymentBreakFactory.create()
        history = EmploymentHistory(Records=[record, break_record])
        cv = CV(
            PersonalInfo=PersonalInfo(Name=Name(FamilyName="Smith")),
            EmploymentHistory=history,
        )
        assert len(cv.EmploymentHistory.Records) == 2


class TestCVSkills:
    """Tests for CV with Skills."""

    def test_cv_with_skills(self) -> None:
        skills = [SkillFactory.create() for _ in range(3)]
        cv = CV(
            PersonalInfo=PersonalInfo(Name=Name(FamilyName="Smith")),
            Skills=skills,
        )
        assert cv.Skills is not None
        assert len(cv.Skills) == 3

    def test_cv_with_single_skill(self) -> None:
        skill = Skill(
            Name="Python",
            Type=SkillType.Technical,
            Level=SkillProficiencyLevel.Expert,
        )
        cv = CV(
            PersonalInfo=PersonalInfo(Name=Name(FamilyName="Smith")),
            Skills=[skill],
        )
        assert cv.Skills[0].Name == "Python"
        assert cv.Skills[0].Level == SkillProficiencyLevel.Expert


class TestCVLanguageProficiencies:
    """Tests for CV with separate language proficiency fields."""

    def test_cv_with_native_language(self) -> None:
        native = NativeLanguage(Language="eng")
        cv = CV(
            PersonalInfo=PersonalInfo(Name=Name(FamilyName="Smith")),
            NativeLanguages=[native],
        )
        assert cv.NativeLanguages is not None
        assert len(cv.NativeLanguages) == 1
        assert isinstance(cv.NativeLanguages[0], NativeLanguage)

    def test_cv_with_self_reported_cefr(self) -> None:
        self_reported = SelfReportedCEFR(Language="fra", Level="B2")
        cv = CV(
            PersonalInfo=PersonalInfo(Name=Name(FamilyName="Smith")),
            SelfReportedLanguages=[self_reported],
        )
        assert len(cv.SelfReportedLanguages) == 1
        assert isinstance(cv.SelfReportedLanguages[0], SelfReportedCEFR)

    def test_cv_with_ielts_certificate(self) -> None:
        from tests.conftest import IELTSFactory
        ielts = IELTSFactory.create()
        cv = CV(
            PersonalInfo=PersonalInfo(Name=Name(FamilyName="Smith")),
            LanguageCertificates=[ielts],
        )
        assert len(cv.LanguageCertificates) == 1
        assert isinstance(cv.LanguageCertificates[0], IELTS)

    def test_cv_with_all_language_fields(self) -> None:
        native = NativeLanguage(Language="eng")
        self_reported = SelfReportedCEFR(Language="fra", Level="B2")
        ielts = IELTSFactory.create()
        cv = CV(
            PersonalInfo=PersonalInfo(Name=Name(FamilyName="Smith")),
            NativeLanguages=[native],
            SelfReportedLanguages=[self_reported],
            LanguageCertificates=[ielts],
        )
        assert len(cv.NativeLanguages) == 1
        assert len(cv.SelfReportedLanguages) == 1
        assert len(cv.LanguageCertificates) == 1
        assert isinstance(cv.NativeLanguages[0], NativeLanguage)
        assert isinstance(cv.SelfReportedLanguages[0], SelfReportedCEFR)
        assert isinstance(cv.LanguageCertificates[0], IELTS)


class TestCVPublications:
    """Tests for CV with Publications."""

    def test_cv_with_journal_article(self) -> None:
        article = JournalArticleFactory.create()
        cv = CV(
            PersonalInfo=PersonalInfo(Name=Name(FamilyName="Smith")),
            Publications=[article],
        )
        assert cv.Publications is not None
        assert len(cv.Publications) == 1
        assert isinstance(cv.Publications[0], JournalArticle)

    def test_cv_with_arxiv_preprint(self) -> None:
        preprint = ArxivPreprintFactory.create()
        cv = CV(
            PersonalInfo=PersonalInfo(Name=Name(FamilyName="Smith")),
            Publications=[preprint],
        )
        assert len(cv.Publications) == 1
        assert isinstance(cv.Publications[0], ArxivPreprint)

    def test_cv_with_mixed_publications(self) -> None:
        article = JournalArticleFactory.create()
        preprint = ArxivPreprintFactory.create()
        cv = CV(
            PersonalInfo=PersonalInfo(Name=Name(FamilyName="Smith")),
            Publications=[article, preprint],
        )
        assert len(cv.Publications) == 2


class TestCVProjects:
    """Tests for CV with Projects."""

    def test_cv_with_project(self) -> None:
        project = ProjectFactory.create()
        cv = CV(
            PersonalInfo=PersonalInfo(Name=Name(FamilyName="Smith")),
            Projects=[project],
        )
        assert cv.Projects is not None
        assert len(cv.Projects) == 1
        assert isinstance(cv.Projects[0], Project)


class TestCVVolunteering:
    """Tests for CV with Volunteering."""

    def test_cv_with_volunteering_activity(self) -> None:
        activity = VolunteeringActivityFactory.create()
        cv = CV(
            PersonalInfo=PersonalInfo(Name=Name(FamilyName="Smith")),
            Volunteering=[activity],
        )
        assert cv.Volunteering is not None
        assert len(cv.Volunteering) == 1
        assert isinstance(cv.Volunteering[0], VolunteeringActivity)


class TestCVEducation:
    """Tests for CV with Education placeholder."""

    def test_cv_with_empty_education(self) -> None:
        cv = CV(
            PersonalInfo=PersonalInfo(Name=Name(FamilyName="Smith")),
            Education=[],
        )
        assert cv.Education == []

    def test_cv_with_education_placeholder(self) -> None:
        record = EducationRecord()
        cv = CV(
            PersonalInfo=PersonalInfo(Name=Name(FamilyName="Smith")),
            Education=[record],
        )
        assert len(cv.Education) == 1


class TestCVReferences:
    """Tests for CV with References."""

    def test_cv_with_empty_references(self) -> None:
        cv = CV(
            PersonalInfo=PersonalInfo(Name=Name(FamilyName="Smith")),
            References=[],
        )
        assert cv.References == []

    def test_cv_with_single_reference(self) -> None:
        reference = ReferenceFactory.create()
        cv = CV(
            PersonalInfo=PersonalInfo(Name=Name(FamilyName="Smith")),
            References=[reference],
        )
        assert cv.References is not None
        assert len(cv.References) == 1
        assert isinstance(cv.References[0], Reference)

    def test_cv_with_multiple_references(self) -> None:
        references = [ReferenceFactory.create() for _ in range(3)]
        cv = CV(
            PersonalInfo=PersonalInfo(Name=Name(FamilyName="Smith")),
            References=references,
        )
        assert cv.References is not None
        assert len(cv.References) == 3
        assert all(isinstance(ref, Reference) for ref in cv.References)

    def test_cv_reference_fields(self) -> None:
        reference = Reference(
            Name="John Doe",
            Title="Senior Engineer",
            Organization="Tech Corp",
            Relationship=RelationshipType.Manager,
            Email="john@example.com",
            Phone="+1234567890",
            LinkedInURL="https://linkedin.com/in/johndoe",
        )
        cv = CV(
            PersonalInfo=PersonalInfo(Name=Name(FamilyName="Smith")),
            References=[reference],
        )
        assert cv.References[0].Name == "John Doe"
        assert cv.References[0].Title == "Senior Engineer"
        assert cv.References[0].Organization == "Tech Corp"
        assert cv.References[0].Relationship == RelationshipType.Manager
        assert cv.References[0].Email == "john@example.com"
        assert cv.References[0].Phone == "+1234567890"
        assert str(cv.References[0].LinkedInURL) == "https://linkedin.com/in/johndoe"

    def test_cv_reference_round_trip_json(self) -> None:
        reference = ReferenceFactory.create()
        cv = CV(
            PersonalInfo=PersonalInfo(Name=Name(FamilyName="Smith")),
            References=[reference],
        )

        json_str = cv.model_dump_json()
        cv2 = CV.model_validate_json(json_str)

        assert cv2.References is not None
        assert len(cv2.References) == 1
        assert cv2.References[0].Name == reference.Name
        assert cv2.References[0].Title == reference.Title
        assert cv2.References[0].Organization == reference.Organization
        assert cv2.References[0].Relationship == reference.Relationship


class TestCVAwards:
    """Tests for CV with Awards."""

    def test_cv_with_empty_awards(self) -> None:
        cv = CV(
            PersonalInfo=PersonalInfo(Name=Name(FamilyName="Smith")),
            Awards=[],
        )
        assert cv.Awards == []

    def test_cv_with_single_award(self) -> None:
        award = AwardFactory.create()
        cv = CV(
            PersonalInfo=PersonalInfo(Name=Name(FamilyName="Smith")),
            Awards=[award],
        )
        assert cv.Awards is not None
        assert len(cv.Awards) == 1
        assert isinstance(cv.Awards[0], Award)

    def test_cv_with_multiple_awards(self) -> None:
        awards = [AwardFactory.create() for _ in range(3)]
        cv = CV(
            PersonalInfo=PersonalInfo(Name=Name(FamilyName="Smith")),
            Awards=awards,
        )
        assert cv.Awards is not None
        assert len(cv.Awards) == 3
        assert all(isinstance(award, Award) for award in cv.Awards)

    def test_cv_award_fields(self) -> None:
        award = Award(
            Title="Nobel Prize in Physics",
            DateReceived="2020-10-06",
            IssuingOrganization="Royal Swedish Academy of Sciences",
            Description="For discoveries in black hole formation.",
        )
        cv = CV(
            PersonalInfo=PersonalInfo(Name=Name(FamilyName="Smith")),
            Awards=[award],
        )
        assert cv.Awards[0].Title == "Nobel Prize in Physics"
        assert cv.Awards[0].DateReceived.isoformat() == "2020-10-06"
        assert cv.Awards[0].IssuingOrganization == "Royal Swedish Academy of Sciences"
        assert cv.Awards[0].Description == "For discoveries in black hole formation."

    def test_cv_award_round_trip_json(self) -> None:
        award = AwardFactory.create()
        cv = CV(
            PersonalInfo=PersonalInfo(Name=Name(FamilyName="Smith")),
            Awards=[award],
        )

        json_str = cv.model_dump_json()
        cv2 = CV.model_validate_json(json_str)

        assert cv2.Awards is not None
        assert len(cv2.Awards) == 1
        assert cv2.Awards[0].Title == award.Title
        assert cv2.Awards[0].DateReceived == award.DateReceived
        assert cv2.Awards[0].IssuingOrganization == award.IssuingOrganization
        assert cv2.Awards[0].Description == award.Description


class TestCVFull:
    """Tests for a fully populated CV with all sections."""

    def test_cv_full_round_trip_json(self) -> None:
        cv = CV(
            PersonalInfo=PersonalInfo(
                Name=Name(
                    Title="Dr.",
                    FamilyName="Smith",
                    GivenNames=["Alice", "Jane"],
                ),
                Contact=ContactInfo(Email="alice@example.com"),
                Address=CVAddress(City="London"),
            ),
            EmploymentHistory=EmploymentHistory(
                Records=[EmploymentRecordFactory.create()]
            ),
            Education=[],
            Skills=[SkillFactory.create(), SkillFactory.create()],
            NativeLanguages=[NativeLanguage(Language="eng")],
            SelfReportedLanguages=[SelfReportedCEFR(Language="fra", Level="B2")],
            LanguageCertificates=[IELTSFactory.create()],
            Publications=[JournalArticleFactory.create()],
            Projects=[ProjectFactory.create()],
            Volunteering=[VolunteeringActivityFactory.create()],
            References=[ReferenceFactory.create()],
            Awards=[AwardFactory.create()],
        )

        json_str = cv.model_dump_json()
        cv2 = CV.model_validate_json(json_str)

        assert cv2.PersonalInfo.Name.FamilyName == "Smith"
        assert cv2.EmploymentHistory is not None
        assert len(cv2.Skills) == 2
        assert len(cv2.NativeLanguages) == 1
        assert len(cv2.SelfReportedLanguages) == 1
        assert len(cv2.LanguageCertificates) == 1
        assert len(cv2.Publications) == 1
        assert len(cv2.Projects) == 1
        assert len(cv2.Volunteering) == 1
        assert len(cv2.References) == 1
        assert len(cv2.Awards) == 1

    def test_cv_all_optional_fields_none(self) -> None:
        cv = CV(PersonalInfo=PersonalInfo(Name=Name(FamilyName="Smith")))
        assert cv.EmploymentHistory is None
        assert cv.Education == []
        assert cv.Skills is None
        assert cv.NativeLanguages is None
        assert cv.SelfReportedLanguages is None
        assert cv.LanguageCertificates is None
        assert cv.Publications is None
        assert cv.Projects is None
        assert cv.Volunteering is None
        assert cv.References is None
        assert cv.Awards is None
