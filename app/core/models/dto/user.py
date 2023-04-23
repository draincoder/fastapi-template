from __future__ import annotations

from dataclasses import dataclass


@dataclass
class User:
    db_id: int | None = None
    username: str | None = None
    email: str | None = None

    def add_password(self, hashed_password: str) -> UserWithCreds:
        return UserWithCreds(
            db_id=self.db_id,
            username=self.username,
            email=self.email,
            hashed_password=hashed_password,
        )


@dataclass
class UserWithCreds(User):
    hashed_password: str | None = None

    def without_password(self) -> User:
        return User(
            db_id=self.db_id,
            username=self.username,
            email=self.email,
        )
