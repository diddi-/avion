from typing import List
from unittest import TestCase

from avion.service.company.repository.company_repository import CompanyRepository
from avion.service.profile.model.create_profile_params import CreateProfileParams
from avion.service.profile.model.profile import Profile
from avion.service.profile.repository.profile_repository import ProfileRepository
from tests.db_initializer import DbInitializer


class TestProfileRepository(TestCase):
    def setUp(self) -> None:
        self.initializer = DbInitializer()
        self.initializer.run()
        self.tested_repository = ProfileRepository(database=self.initializer.db_path)
        self.company_repository = CompanyRepository(database=self.initializer.db_path)

    def test_get_profile_by_id_return_list_of_profiles(self) -> None:
        account_id = 1
        expected_profiles: List[Profile] = []
        expected_profiles.append(self.tested_repository.create(CreateProfileParams("John", "Doe", owner_id=account_id)))
        expected_profiles.append(self.tested_repository.create(CreateProfileParams("Jane", "Doe", owner_id=account_id)))

        actual_profiles = self.tested_repository.get_profiles_by_account_id(account_id)
        profile_ids = [p.id for p in actual_profiles]
        self.assertEqual(len(expected_profiles), len(profile_ids))
        self.assertIn(expected_profiles[0].id, profile_ids)
        self.assertIn(expected_profiles[1].id, profile_ids)
