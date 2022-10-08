import contextlib
import datetime
import sqlite3
from sqlite3 import Row
from typing import List

from avion.service.account.model.user_account import UserAccount
from avion.service.account.model.create_user_account_params import CreateUserAccountParams


class UserAccountRepository:
    def __init__(self, database: str = "/db/airline-api.db"):
        self._db = database

    def create(self, params: CreateUserAccountParams, hashed_password: str, salt: str) -> UserAccount:
        user = UserAccount(params.firstname, params.lastname)
        user.created_at = datetime.datetime.now(datetime.timezone.utc)
        user.email = params.email
        with contextlib.closing(sqlite3.connect(self._db)) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("INSERT INTO user_account (created_at, firstname, lastname, email, username, password, salt) "
                        "VALUES (?,?,?,?,?,?,?)",
                        (user.created_at, user.firstname, user.lastname, user.email, user.email, hashed_password, salt))
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
            cur.execute("SELECT id, created_at, firstname, lastname, email FROM user_account WHERE username=?",
                        (username,))
            return self._row_to_user_account(cur.fetchone())

    def validate_credentials(self, username: str, password: str) -> bool:
        with contextlib.closing(sqlite3.connect(self._db)) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM user_account WHERE username=? AND password=?",
                        (username, password))
            count = cur.fetchone()[0]
            return count == 1

    def get_salt(self, username: str) -> str:
        with contextlib.closing(sqlite3.connect(self._db)) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT salt FROM user_account WHERE username=?", (username,))
            return cur.fetchone()[0]

    @staticmethod
    def _row_to_user_account(row: Row) -> UserAccount:
        user = UserAccount(row["firstname"], row["lastname"])
        user.created_at = datetime.datetime.fromisoformat(row["created_at"])
        user.id = row["id"]
        return user
