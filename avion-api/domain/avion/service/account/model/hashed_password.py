import hashlib
import secrets
import string
from typing import Any, Optional


class HashedPassword:
    def __init__(self, cleartext: str, salt: Optional[str] = None):
        alphabet = string.ascii_letters + string.digits
        self._salt = salt if salt else ''.join(secrets.choice(alphabet) for _ in range(20))
        self._password = hashlib.sha256(bytes(cleartext + self._salt, "utf-8")).hexdigest()

    @property
    def password(self) -> str:
        return self._password

    @property
    def salt(self) -> str:
        return self._salt

    def __str__(self) -> str:
        # Do not accidentally print to logs or serialize in API responses
        return "*****"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, HashedPassword) and other.password == self.password
