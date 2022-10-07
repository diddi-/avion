import contextlib
import datetime
import sqlite3
from sqlite3 import Row

from avion.model.profile import Profile
from avion.parameters.create_profile_params import CreateProfileParams


class ProfileRepository:
    def __init__(self, database: str = "/db/airline-api.db"):
        self._db = database

    def create(self, params: CreateProfileParams) -> Profile:
        profile = Profile(params.firstname, params.lastname)
        profile.created_at = datetime.datetime.now(datetime.timezone.utc)
        profile.owner_id = params.owner_id
        profile.balance = params.balance
        with contextlib.closing(sqlite3.connect(self._db)) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("INSERT INTO profile (created_at, user_account_id, firstname, lastname, balance) "
                        "VALUES (?,?,?,?,?)",
                        (profile.created_at, profile.owner_id, profile.firstname, profile.lastname, profile.balance))
            conn.commit()
            profile.id = cur.lastrowid
        return profile

    def account_has_profile(self, account_id: int, profile_id: int) -> bool:
        with contextlib.closing(sqlite3.connect(self._db)) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM profile WHERE user_account_id=? AND id=?",
                        (account_id, profile_id))
            conn.commit()
            count = cur.fetchone()[0]
            return count == 1

    def get_profile_by_id(self, profile_id: int) -> Profile:
        with contextlib.closing(sqlite3.connect(self._db)) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM profile WHERE id = ?", (profile_id,))
            conn.commit()
            return self._row_to_profile(cur.fetchone())

    def save(self, profile: Profile):
        with contextlib.closing(sqlite3.connect(self._db)) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("UPDATE profile SET balance = ? WHERE id = ?", (profile.balance, profile.id))
            conn.commit()

    @staticmethod
    def _row_to_profile(row: Row) -> Profile:
        profile = Profile(row["firstname"], row["lastname"])
        profile.created_at = datetime.datetime.fromisoformat(row["created_at"])
        profile.id = row["id"]
        profile.balance = row["balance"]
        return profile
