from unittest import TestCase

from avion.parameters.create_user_account_params import CreateUserAccountParams
from avion.repository.user_account_repository import UserAccountRepository
from tests.avion.repository.db_initializer import DbInitializer


class TestUserAccountRepository(TestCase):

    def setUp(self) -> None:
        self.initializer = DbInitializer()
        self.initializer.run()

    def test_user_account_can_be_created(self) -> None:
        params = CreateUserAccountParams("John", "Doe", "john@example.com")
        user = UserAccountRepository(database=self.initializer.db_path).create(params)
        self.assertIsNotNone(user.id)

    def test_get_all_user_accounts(self) -> None:
        john = CreateUserAccountParams("John", "Doe", "john@example.com")
        trevor = CreateUserAccountParams("Trevor", "Doe", "trevor@example.com")
        repository = UserAccountRepository(database=self.initializer.db_path)
        repository.create(john)
        repository.create(trevor)

        users = repository.get_all_user_accounts()
        self.assertEqual(2, len(users))
        self.assertEqual(users[0].firstname, john.firstname)
        self.assertEqual(users[1].firstname, trevor.firstname)
