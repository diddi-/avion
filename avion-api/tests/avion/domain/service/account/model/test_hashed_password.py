from unittest import TestCase

from avion.domain.service.account.model.hashed_password import HashedPassword


class TestHashedPassword(TestCase):
    def test_cleartext_password_is_hashed(self) -> None:
        cleartext = "password"
        hashed = HashedPassword(cleartext)
        self.assertNotEqual(cleartext, hashed.password)

    def test_salt_is_randomized_by_default(self) -> None:
        """ This is a tricky one because in theory there MAY be a case where the salt is computed exactly the same.
         It's extremely unlikely but it does make the test brittle. """
        cleartext = "password"
        hashed1 = HashedPassword(cleartext)
        hashed2 = HashedPassword(cleartext)
        self.assertNotEqual(hashed1.salt, hashed2.salt)
        self.assertNotEqual(hashed1.password, hashed2.password)

    def test_salt_can_be_customized(self) -> None:
        cleartext = "password"
        salt = "salt"
        hashed1 = HashedPassword(cleartext, salt)
        hashed2 = HashedPassword(cleartext, salt)
        self.assertEqual(hashed1.salt, hashed2.salt)
        self.assertEqual(hashed1.password, hashed2.password)

    def test_password_cast_to_string_returns_asterisks(self) -> None:
        password = HashedPassword("password")
        self.assertEqual("*****", str(password))

    def test_passwords_are_equal_when_the_hashed_passwords_are_equal(self) -> None:
        cleartext = "password"
        salt = "salt"
        password1 = HashedPassword(cleartext, salt)
        password2 = HashedPassword(cleartext, salt)
        self.assertEqual(password1, password2)

    def test_passwords_are_not_equal_when_the_hashed_passwords_differ(self) -> None:
        cleartext = "password"
        password1 = HashedPassword(cleartext, "salt1")
        password2 = HashedPassword(cleartext, "salt2")
        self.assertNotEqual(password1, password2)
