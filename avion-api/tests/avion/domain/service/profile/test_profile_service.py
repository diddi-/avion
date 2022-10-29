from unittest import TestCase

from avion.domain.service.company.model.company_role import CompanyRole
from avion.domain.service.profile.model.profile import Profile
from avion.domain.service.profile.profile_service import ProfileService
from mockito import mock, when


class TestProfileService(TestCase):
    def setUp(self) -> None:
        self.stubbed_profile_repo = mock()
        self.tested_service = ProfileService(repository=self.stubbed_profile_repo)

    def test_company_role_can_be_added_to_profile(self) -> None:
        profile = Profile(123, "John", "Doe")
        company_id = 1
        role = CompanyRole.CEO

        when(self.stubbed_profile_repo).get_profile_by_id(profile.id).thenReturn(profile)
        self.tested_service.add_company_role(profile.id, company_id, role)
        self.assertTrue(profile.has_company_role(company_id, [CompanyRole.CEO]))
