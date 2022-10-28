import contextlib
import datetime
import sqlite3
from sqlite3 import Row, IntegrityError
from typing import List

from avion.service.account.exceptions.duplicate_account_exception import DuplicateAccountException
from avion.service.account.exceptions.no_such_user_exception import NoSuchUserException
from avion.service.account.model.create_user_account_params import CreateUserAccountParams
from avion.service.account.model.hashed_password import HashedPassword
from avion.service.account.model.user_account import UserAccount


class UserAccountRepository:
    def __init__(self, database: str = "/db/airline-api.db"):
        self._db = database

    def create(self, params: CreateUserAccountParams, password: HashedPassword) -> UserAccount:
        created_at = datetime.datetime.now(datetime.timezone.utc)
        with contextlib.closing(sqlite3.connect(self._db)) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO user_account (created_at, firstname, lastname, email, username, password,"
                            " salt) VALUES (?,?,?,?,?,?,?)",
                            (created_at, params.firstname, params.lastname, params.email, params.email,
                             password.password, password.salt))
                conn.commit()
            except IntegrityError as e:
                if "UNIQUE constraint failed: user_account.username" in str(e):
                    raise DuplicateAccountException(params.email) from e
                raise e

            user_id = cur.lastrowid
            if not user_id:
                raise RuntimeError(f"User Account {params.email} did not receive a row ID!")
            user = UserAccount(user_id, params.firstname, params.lastname, params.email, params.email)
            user.created_at = created_at
        return user

    def get_all_user_accounts(self) -> List[UserAccount]:
        users = []
        with contextlib.closing(sqlite3.connect(self._db)) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM user_account")
            rows = cur.fetchall()
            for row in rows:
                users.append(self._row_to_user_account(row))
        return users

    def get_user_by_username(self, username: str) -> UserAccount:
        with contextlib.closing(sqlite3.connect(self._db)) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(
                "SELECT id, created_at, firstname, lastname, email, username FROM user_account WHERE username=?",
                (username,))
            return self._row_to_user_account(cur.fetchone())

    def get_user_by_id(self, user_id: int) -> UserAccount:
        with contextlib.closing(sqlite3.connect(self._db)) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(
                "SELECT id, created_at, firstname, lastname, email, username FROM user_account WHERE id=?",
                (user_id,))
            return self._row_to_user_account(cur.fetchone())

    def validate_credentials(self, username: str, password: HashedPassword) -> bool:
        with contextlib.closing(sqlite3.connect(self._db)) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM user_account WHERE username=? AND password=?",
                        (username, password.password))
            row = cur.fetchone()
            return row is not None and row[0] == 1

    def get_salt(self, username: str) -> str:
        with contextlib.closing(sqlite3.connect(self._db)) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT salt FROM user_account WHERE username=?", (username,))
            row = cur.fetchone()
            if not row:
                raise NoSuchUserException()
            return str(row[0])

    @staticmethod
    def _row_to_user_account(row: Row) -> UserAccount:
        user = UserAccount(int(row["id"]), row["firstname"], row["lastname"], row["email"], row["username"])
        user.created_at = datetime.datetime.fromisoformat(row["created_at"])
        return user
