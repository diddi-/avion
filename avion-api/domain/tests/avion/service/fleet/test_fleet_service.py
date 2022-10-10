from unittest import TestCase

from mockito import mock, verify, when
from parameterized import parameterized

from avion.model.currency import Currency
from avion.service.company.model.company_role import CompanyRole
from avion.service.fleet.fleet_service import FleetService
from avion.service.fleet.model.aircraft_model import AircraftModel
from avion.service.profile.model.profile import Profile


class TestFleetService(TestCase):
    def setUp(self) -> None:
        self.stubbed_fleet_repo = mock()
        self.stubbed_profile_service = mock()
        self.stubbed_company_service = mock()
        self.tested_service = FleetService(repository=self.stubbed_fleet_repo,
                                           profile_service=self.stubbed_profile_service,
                                           company_service=self.stubbed_company_service)

    @parameterized.expand([(CompanyRole.CEO,), (CompanyRole.FLEET_MGMT,)])  # type: ignore
    def test_CEO_and_FLEET_MGMT_roles_can_buy_new_aircraft(self, role: CompanyRole) -> None:
        profile = Profile("John", "Doe")
        company_id = 1
        aircraft_model_id = 1
        profile.add_company_role(company_id, role)
        self.tested_service.buy_aircraft(profile, company_id, aircraft_model_id)

        verify(self.stubbed_fleet_repo).add_to_fleet(company_id, aircraft_model_id)

    def test_exception_is_raised_when_unauthorized_role_attempts_to_buy_aircraft(self) -> None:
        profile = Profile("John", "Doe")
        company_id = 1
        aircraft_model_id = 1
        profile.add_company_role(company_id, CompanyRole.HR)
        with self.assertRaises(ValueError) as err:
            self.tested_service.buy_aircraft(profile, company_id, aircraft_model_id)
        self.assertIn("Unauthorized", str(err.exception))

    def test_money_is_withdrawn_from_company_when_buying_aircraft(self) -> None:
        profile = Profile("John", "Doe")
        company_id = 1
        aircraft_model = AircraftModel("Cessna", "172", "C172")
        aircraft_model.id = 1
        aircraft_model.price = Currency(100)
        profile.add_company_role(company_id, CompanyRole.CEO)

        when(self.stubbed_fleet_repo).get_aircraft_model_by_id(aircraft_model.id).thenReturn(aircraft_model)
        self.tested_service.buy_aircraft(profile, company_id, aircraft_model.id)
        verify(self.stubbed_company_service).withdraw(company_id, aircraft_model.price)
