from typing import List
from unittest import TestCase

from avion.service.company.repository.company_repository import CompanyRepository
from avion.service.profile.exceptions.duplicate_profile_exception import DuplicateProfileException
from avion.service.profile.model.create_profile_params import CreateProfileParams
from avion.service.profile.model.profile import Profile
from avion.service.profile.repository.profile_repository import ProfileRepository
from avion.testutils.db_initializer import DbInitializer


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
        expected_profiles.append(self.tested_repository.create(CreateProfileParams("Jane", "Hawkins",
                                                                                   owner_id=account_id)))

        actual_profiles = self.tested_repository.get_profiles_by_account_id(account_id)
        profile_ids = [p.id for p in actual_profiles]
        self.assertEqual(len(expected_profiles), len(profile_ids))
        self.assertIn(expected_profiles[0].id, profile_ids)
        self.assertIn(expected_profiles[1].id, profile_ids)

    def test_two_profiles_with_same_name_cant_be_created_by_a_single_account(self) -> None:
        params = CreateProfileParams("John", "Doe", owner_id=1)
        self.tested_repository.create(params)

        with self.assertRaises(DuplicateProfileException):
            self.tested_repository.create(params)

    def test_two_profiles_with_same_name_can_be_created_by_two_different_accounts(self) -> None:
        profile1params = CreateProfileParams("John", "Doe", owner_id=1)
        profile2params = CreateProfileParams(profile1params.firstname, profile1params.lastname, owner_id=2)

        profile1 = self.tested_repository.create(profile1params)
        profile2 = self.tested_repository.create(profile2params)
        self.assertEqual(profile1.firstname, profile2.firstname)
        self.assertEqual(profile1.lastname, profile2.lastname)
        self.assertNotEqual(profile1.owner_id, profile2.owner_id)
