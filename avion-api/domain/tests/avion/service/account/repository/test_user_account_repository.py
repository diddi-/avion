from unittest import TestCase

from avion.service.account.model.create_user_account_params import CreateUserAccountParams
from avion.service.account.model.hashed_password import HashedPassword
from avion.service.account.repository.user_account_repository import UserAccountRepository
from tests.db_initializer import DbInitializer


class TestUserAccountRepository(TestCase):

    def setUp(self) -> None:
        self.initializer = DbInitializer()
        self.initializer.run()

    def test_user_account_can_be_created(self) -> None:
        params = CreateUserAccountParams("John", "Doe", "john@example.com", "secret")
        user = UserAccountRepository(database=self.initializer.db_path).create(params, HashedPassword("secret"))
        self.assertIsNotNone(user.id)

    def test_get_all_user_accounts(self) -> None:
        john = CreateUserAccountParams("John", "Doe", "john@example.com", "secret")
        trevor = CreateUserAccountParams("Trevor", "Doe", "trevor@example.com", "abcde")
        repository = UserAccountRepository(database=self.initializer.db_path)
        repository.create(john, HashedPassword("secret"))
        repository.create(trevor, HashedPassword("secret"))

        users = repository.get_all_user_accounts()
        self.assertEqual(3, len(users))  # Seeded admin user too!
        self.assertEqual(users[1].firstname, john.firstname)
        self.assertEqual(users[2].firstname, trevor.firstname)
