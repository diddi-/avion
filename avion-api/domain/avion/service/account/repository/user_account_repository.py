import contextlib
import datetime
import sqlite3
from sqlite3 import Row
from typing import List

from avion.service.account.exceptions.no_such_user_exception import NoSuchUserException
from avion.service.account.model.hashed_password import HashedPassword
from avion.service.account.model.user_account import UserAccount
from avion.service.account.model.create_user_account_params import CreateUserAccountParams


class UserAccountRepository:
    def __init__(self, database: str = "/db/airline-api.db"):
        self._db = database

    def create(self, params: CreateUserAccountParams, password: HashedPassword) -> UserAccount:
        user = UserAccount(params.firstname, params.lastname, params.email, params.email)
        with contextlib.closing(sqlite3.connect(self._db)) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("INSERT INTO user_account (created_at, firstname, lastname, email, username, password, salt) "
                        "VALUES (?,?,?,?,?,?,?)",
                        (user.created_at, user.firstname, user.lastname, user.email, user.username, password.password,
                         password.salt))
            conn.commit()
            user.id = cur.lastrowid
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
            return row is not None

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
        user = UserAccount(row["firstname"], row["lastname"], row["email"], row["username"])
        user.created_at = datetime.datetime.fromisoformat(row["created_at"])
        user.id = row["id"]
        return user
