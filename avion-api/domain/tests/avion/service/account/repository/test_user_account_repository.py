import datetime
from unittest import TestCase

from avion.service.account.exceptions.duplicate_account_exception import DuplicateAccountException
from avion.service.account.model.create_user_account_params import CreateUserAccountParams
from avion.service.account.model.hashed_password import HashedPassword
from avion.service.account.repository.user_account_repository import UserAccountRepository
from avion.testutils.db_initializer import DbInitializer


class TestUserAccountRepository(TestCase):

    def setUp(self) -> None:
        self.initializer = DbInitializer()

    def test_initial_seeded_admin_user_can_login(self) -> None:
        self.initializer.run(include_seeds=True)
        repository = UserAccountRepository(database=self.initializer.db_path)
        salt = repository.get_salt("admin")
        self.assertTrue(repository.validate_credentials("admin", HashedPassword("admin", salt)))

    def test_user_account_can_be_created(self) -> None:
        self.initializer.run()
        params = CreateUserAccountParams("John", "Doe", "john@example.com", "secret")
        user = UserAccountRepository(database=self.initializer.db_path).create(params, HashedPassword("secret"))
        self.assertIsNotNone(user.id)

    def test_get_all_user_accounts(self) -> None:
        self.initializer.run()
        john = CreateUserAccountParams("John", "Doe", "john@example.com", "secret")
        trevor = CreateUserAccountParams("Trevor", "Doe", "trevor@example.com", "abcde")
        repository = UserAccountRepository(database=self.initializer.db_path)
        repository.create(john, HashedPassword("secret"))
        repository.create(trevor, HashedPassword("secret"))

        users = repository.get_all_user_accounts()
        self.assertEqual(2, len(users))
        self.assertEqual(users[0].firstname, john.firstname)
        self.assertEqual(users[1].firstname, trevor.firstname)

    def test_username_must_be_unique(self) -> None:
        self.initializer.run()
        params = CreateUserAccountParams("John", "Doe", "john@example.com", "secret")
        repository = UserAccountRepository(database=self.initializer.db_path)
        repository.create(params, HashedPassword(params.password))

        with self.assertRaises(DuplicateAccountException):
            repository.create(params, HashedPassword(params.password))

    def test_created_at_field_is_set_when_creating_new_account(self) -> None:
        self.initializer.run()
        params = CreateUserAccountParams("John", "Doe", "john@example.com", "secret")
        user = UserAccountRepository(database=self.initializer.db_path).create(params, HashedPassword(params.password))

        # We loosely check if the created_at is within ten seconds. Not great, but it's good enough(tm)
        delta = user.created_at - datetime.datetime.now(datetime.timezone.utc)
        self.assertLess(delta, datetime.timedelta(seconds=10))

    def test_user_can_be_fetched_by_username(self) -> None:
        self.initializer.run()
        params = CreateUserAccountParams("John", "Doe", "john@example.com", "secret")
        repository = UserAccountRepository(database=self.initializer.db_path)
        expected_user = repository.create(params, HashedPassword(params.password))
        actual_user = repository.get_user_by_username(expected_user.username)
        self.assertEqual(expected_user, actual_user)

    def test_user_can_be_fetched_by_id(self) -> None:
        self.initializer.run()
        params = CreateUserAccountParams("John", "Doe", "john@example.com", "secret")
        repository = UserAccountRepository(database=self.initializer.db_path)
        expected_user = repository.create(params, HashedPassword(params.password))
        user_id = expected_user.id if expected_user.id else 0  # For mypy because UserAccount.id is Optional
        actual_user = repository.get_user_by_id(user_id)
        self.assertEqual(expected_user, actual_user)

    def test_password_can_be_validated(self) -> None:
        self.initializer.run()
        params = CreateUserAccountParams("John", "Doe", "john@example.com", "secret")
        repository = UserAccountRepository(database=self.initializer.db_path)
        correct_password = HashedPassword(params.password)
        wrong_password = HashedPassword("wrong-password")
        user = repository.create(params, correct_password)
        self.assertTrue(repository.validate_credentials(user.username, correct_password), "Correct password is valid")
        self.assertFalse(repository.validate_credentials(user.username, wrong_password), "Wrong password is valid")

    def test_salt_can_be_retrieved(self) -> None:
        self.initializer.run()
        params = CreateUserAccountParams("John", "Doe", "john@example.com", "secret")
        repository = UserAccountRepository(database=self.initializer.db_path)
        password = HashedPassword("secret")
        user = repository.create(params, password)
        self.assertEqual(password.salt, repository.get_salt(user.username))
