"""Tests for pydanticcv.cv.personal_info models.

Covers SocialPlatform, ProfileLink with platform auto-detection,
and expanded ContactInfo fields.
"""

import pytest
from pydantic import ValidationError

from pydanticcv.cv.personal_info import ContactInfo, ProfileLink, SocialPlatform


class TestSocialPlatform:
    """Tests for the SocialPlatform enum."""

    def test_all_platform_values(self) -> None:
        """Test that all expected platform values exist."""
        assert SocialPlatform.LinkedIn == "LinkedIn"
        assert SocialPlatform.GitHub == "GitHub"
        assert SocialPlatform.Twitter == "Twitter"
        assert SocialPlatform.Website == "Website"
        assert SocialPlatform.ORCID == "ORCID"
        assert SocialPlatform.GoogleScholar == "GoogleScholar"
        assert SocialPlatform.ResearchGate == "ResearchGate"
        assert SocialPlatform.Behance == "Behance"
        assert SocialPlatform.Dribbble == "Dribbble"
        assert SocialPlatform.Custom == "Custom"


class TestProfileLink:
    """Tests for the ProfileLink model with auto platform detection."""

    def test_detects_linkedin(self) -> None:
        """Test LinkedIn URL detection."""
        link = ProfileLink(url="https://linkedin.com/in/johndoe")
        assert link.platform == SocialPlatform.LinkedIn

    def test_detects_linkedin_pub(self) -> None:
        """Test LinkedIn publication URL detection."""
        link = ProfileLink(url="https://linkedin.com/pub/johndoe/123/456")
        assert link.platform == SocialPlatform.LinkedIn

    def test_detects_github(self) -> None:
        """Test GitHub URL detection."""
        link = ProfileLink(url="https://github.com/johndoe")
        assert link.platform == SocialPlatform.GitHub

    def test_detects_github_with_path(self) -> None:
        """Test GitHub URL with repo path detection."""
        link = ProfileLink(url="https://github.com/johndoe/myproject")
        assert link.platform == SocialPlatform.GitHub

    def test_detects_twitter(self) -> None:
        """Test Twitter URL detection."""
        link = ProfileLink(url="https://twitter.com/johndoe")
        assert link.platform == SocialPlatform.Twitter

    def test_detects_x_com(self) -> None:
        """Test X.com URL detection."""
        link = ProfileLink(url="https://x.com/johndoe")
        assert link.platform == SocialPlatform.Twitter

    def test_detects_orcid(self) -> None:
        """Test ORCID URL detection."""
        link = ProfileLink(url="https://orcid.org/0000-0001-2345-6789")
        assert link.platform == SocialPlatform.ORCID

    def test_detects_google_scholar(self) -> None:
        """Test Google Scholar URL detection."""
        link = ProfileLink(url="https://scholar.google.com/citations?user=abc123")
        assert link.platform == SocialPlatform.GoogleScholar

    def test_detects_researchgate(self) -> None:
        """Test ResearchGate URL detection."""
        link = ProfileLink(url="https://www.researchgate.net/profile/John-Doe")
        assert link.platform == SocialPlatform.ResearchGate

    def test_detects_behance(self) -> None:
        """Test Behance URL detection."""
        link = ProfileLink(url="https://www.behance.net/johndoe")
        assert link.platform == SocialPlatform.Behance

    def test_detects_dribbble(self) -> None:
        """Test Dribbble URL detection."""
        link = ProfileLink(url="https://dribbble.com/johndoe")
        assert link.platform == SocialPlatform.Dribbble

    def test_custom_platform_for_unknown(self) -> None:
        """Test custom platform for unrecognized URLs."""
        link = ProfileLink(url="https://example.com/profile/johndoe")
        assert link.platform == SocialPlatform.Custom

    def test_url_case_insensitive_detection(self) -> None:
        """Test URL detection is case-insensitive."""
        link = ProfileLink(url="https://GITHUB.COM/johndoe")
        assert link.platform == SocialPlatform.GitHub

    def test_with_label(self) -> None:
        """Test ProfileLink with optional label."""
        link = ProfileLink(
            url="https://linkedin.com/in/johndoe",
            label="My LinkedIn",
        )
        assert link.label == "My LinkedIn"
        assert link.platform == SocialPlatform.LinkedIn


class TestProfileLinkValidation:
    """Tests for ProfileLink URL validation."""

    def test_rejects_http_url(self) -> None:
        """Test that HTTP URLs are rejected."""
        with pytest.raises(ValidationError):
            ProfileLink(url="http://linkedin.com/in/johndoe")


class TestContactInfoExpanded:
    """Tests for expanded ContactInfo with new platform fields."""

    def test_all_fields_optional(self) -> None:
        """Test that all new fields are optional."""
        contact = ContactInfo()
        assert contact.Email is None
        assert contact.Phone is None
        assert contact.Website is None
        assert contact.LinkedIn is None
        assert contact.GitHub is None
        assert contact.Twitter is None
        assert contact.ORCID is None
        assert contact.GoogleScholar is None
        assert contact.ResearchGate is None
        assert contact.Behance is None
        assert contact.Dribbble is None
        assert contact.ProfileLinks == []
        assert contact.OtherUrls == []

    def test_accepts_new_platform_fields(self) -> None:
        """Test that new platform URL fields are accepted."""
        contact = ContactInfo(
            Twitter="https://twitter.com/johndoe",
            ORCID="https://orcid.org/0000-0001-2345-6789",
            GoogleScholar="https://scholar.google.com/citations?user=abc",
            ResearchGate="https://researchgate.net/profile/johndoe",
            Behance="https://behance.net/johndoe",
            Dribbble="https://dribbble.com/johndoe",
        )
        assert contact.Twitter is not None
        assert contact.ORCID is not None
        assert contact.GoogleScholar is not None
        assert contact.ResearchGate is not None
        assert contact.Behance is not None
        assert contact.Dribbble is not None

    def test_accepts_profile_links(self) -> None:
        """Test that ProfileLinks field is accepted."""
        links = [
            ProfileLink(url="https://linkedin.com/in/johndoe"),
            ProfileLink(url="https://github.com/johndoe", label="Code"),
        ]
        contact = ContactInfo(ProfileLinks=links)
        assert len(contact.ProfileLinks) == 2
        assert contact.ProfileLinks[0].platform == SocialPlatform.LinkedIn
        assert contact.ProfileLinks[1].platform == SocialPlatform.GitHub


class TestContactInfoBackwardCompatibility:
    """Tests for backward compatibility with existing ContactInfo usage."""

    def test_existing_fields_still_work(self) -> None:
        """Test that original ContactInfo fields remain functional."""
        contact = ContactInfo(
            Email="john@example.com",
            Phone="+442071234567",
            Website="https://johndoe.com",
            LinkedIn="https://linkedin.com/in/johndoe",
            GitHub="https://github.com/johndoe",
            OtherUrls=["https://blog.johndoe.com"],
        )
        assert contact.Email == "john@example.com"
        assert contact.Phone is not None
        assert contact.Website is not None
        assert contact.LinkedIn is not None
        assert contact.GitHub is not None
        assert len(contact.OtherUrls) == 1
