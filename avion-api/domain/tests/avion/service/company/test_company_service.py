from unittest import TestCase

from mockito import mock, when

from avion.model.currency import Currency
from avion.service.company.company_service import CompanyService
from avion.service.company.model.company import Company
from avion.service.company.model.create_company_params import CreateCompanyParams


class TestCompanyService(TestCase):
    def setUp(self) -> None:
        self.stubbed_repo = mock()
        self.stubbed_profile_service = mock()
        self.tested_service = CompanyService(company_repository=self.stubbed_repo,
                                             profile_service=self.stubbed_profile_service)

    def test_company_can_be_created(self) -> None:
        account_id = 1
        params = CreateCompanyParams("SAS", 123, 10000)
        expected_company = Company(params.name)
        when(self.stubbed_profile_service).account_has_profile(account_id, params.owner_id).thenReturn(True)
        when(self.stubbed_repo).create(params).thenReturn(expected_company)

        actual_company = self.tested_service.create_company(account_id, params)
        self.assertEqual(expected_company.name, actual_company.name)

    def test_withdraw_currency_from_company(self):
        company = Company("SAS")
        company.id = 1
        company.balance = Currency(100)
        when(self.stubbed_repo).get_company_by_id(company.id).thenReturn(company)
        self.tested_service.withdraw(company.id, Currency(50))
        self.assertEqual(Currency(50), company.balance)

    def test_withdraw_raises_exception_when_balance_is_too_low(self):
        company = Company("SAS")
        company.id = 1
        company.balance = Currency(50)
        when(self.stubbed_repo).get_company_by_id(company.id).thenReturn(company)
        with self.assertRaises(ValueError) as err:
            self.tested_service.withdraw(company.id, Currency(100))
        self.assertIn("Insufficient funds", str(err.exception))
