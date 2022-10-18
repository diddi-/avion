import contextlib
import datetime
import sqlite3
from sqlite3 import Row
from typing import List

from avion.service.company.model.company_role import CompanyRole
from avion.service.profile.model.profile import Profile
from avion.service.profile.model.create_profile_params import CreateProfileParams


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
            count = int(cur.fetchone()[0])
            return count == 1

    def get_profile_by_id(self, profile_id: int) -> Profile:
        with contextlib.closing(sqlite3.connect(self._db)) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM profile WHERE id = ?", (profile_id,))
            profile = self._row_to_profile(cur.fetchone())
            cur.execute("SELECT company_id, role from company_profile_role where profile_id=?",
                        (profile.id,))
            rows = cur.fetchall()
            for row in rows:
                profile.add_company_role(row[0], CompanyRole(row[1]))
            return profile

    def get_profiles_by_account_id(self, account_id: int) -> List[Profile]:
        profiles: List[Profile] = []

        with contextlib.closing(sqlite3.connect(self._db)) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM profile WHERE user_account_id = ?", (account_id,))
            rows = cur.fetchall()
            for row in rows:
                profile = self._row_to_profile(row)

                # Perhaps fetching the roles should be a different method altogether. This may just be unnecessary
                # if it's not actually used anywhere.
                cur.execute("SELECT company_id, role from company_profile_role where profile_id=?",
                            (profile.id,))
                roles_rows = cur.fetchall()
                for roles_row in roles_rows:
                    profile.add_company_role(roles_row[0], CompanyRole(roles_row[1]))
                profiles.append(profile)
        return profiles

    def save(self, profile: Profile) -> None:
        with contextlib.closing(sqlite3.connect(self._db)) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("UPDATE profile SET balance = ? WHERE id = ?", (profile.balance, profile.id))

            # This is UGLY. But we're here to make things work first.
            cur.execute("DELETE FROM company_profile_role WHERE profile_id=?", (profile.id,))
            for role in profile.roles:
                cur.execute("INSERT INTO company_profile_role (company_id, profile_id, role)"
                            " VALUES(?,?,?)", (role[0], profile.id, str(role[1])))
            conn.commit()

    @staticmethod
    def _row_to_profile(row: Row) -> Profile:
        profile = Profile(row["firstname"], row["lastname"])
        profile.created_at = datetime.datetime.fromisoformat(row["created_at"])
        profile.id = row["id"]
        profile.balance = row["balance"]
        return profile
