from unittest import TestCase

from avion.service.company.model.company_role import CompanyRole
from avion.service.profile.model.profile import Profile


class TestProfile(TestCase):
    def test_has_company_role(self) -> None:
        profile = Profile("John", "Doe")
        company_id = 1
        profile.add_company_role(company_id, CompanyRole.CEO)
        profile.add_company_role(company_id, CompanyRole.FLEET_MGMT)

        self.assertTrue(profile.has_company_role(company_id, [CompanyRole.CEO]))
        self.assertTrue(profile.has_company_role(company_id, [CompanyRole.FLEET_MGMT]))
        self.assertTrue(profile.has_company_role(company_id, [CompanyRole.HR, CompanyRole.CEO]))
        self.assertFalse(profile.has_company_role(company_id, [CompanyRole.HR]))
