from unittest import TestCase

from mockito import mock, verify
from parameterized import parameterized

from avion.service.company.model.company_role import CompanyRole
from avion.service.fleet.fleet_service import FleetService
from avion.service.profile.model.profile import Profile


class TestFleetService(TestCase):
    def setUp(self) -> None:
        self.stubbed_fleet_repo = mock()
        self.stubbed_profile_service = mock()
        self.tested_service = FleetService(repository=self.stubbed_fleet_repo,
                                           profile_service=self.stubbed_profile_service)

    @parameterized.expand([(CompanyRole.CEO,), (CompanyRole.FLEET_MGMT,)])
    def test_CEO_and_FLEET_MGMT_roles_can_buy_new_aircraft(self, role: CompanyRole) -> None:
        profile = Profile("John", "Doe")
        company_id = 1
        aircraft_model_id = 1
        profile.add_company_role(company_id, role)
        self.tested_service.buy_aircraft(profile, company_id, aircraft_model_id)

        verify(self.stubbed_fleet_repo).add_to_fleet(company_id, aircraft_model_id)

    def test_exception_is_raised_when_unauthorized_role_attempts_to_buy_aircraft(self):
        profile = Profile("John", "Doe")
        company_id = 1
        aircraft_model_id = 1
        profile.add_company_role(company_id, CompanyRole.HR)
        with self.assertRaises(ValueError) as err:
            self.tested_service.buy_aircraft(profile, company_id, aircraft_model_id)
        self.assertIn("Unauthorized", str(err.exception))
