from datetime import datetime

from pydantic import BaseModel

from app.core.models import dto


class UserAuth(BaseModel):
    id: int
    auth_date: datetime
    email: str
    hash: str
    username: str | None = None

    def to_dto(self) -> dto.User:
        return dto.User(
            tg_id=self.id,
            username=self.username,
            email=self.email
        )


class Token(BaseModel):
    access_token: str
    token_type: str
