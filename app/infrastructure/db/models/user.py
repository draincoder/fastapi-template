from sqlalchemy import BigInteger, Text
from sqlalchemy.orm import mapped_column, Mapped

from .base import TimedBaseModel
from app.core.models import dto


class User(TimedBaseModel):
    __tablename__ = "users"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(Text, nullable=True)

    def __repr__(self):
        return f"<User id={self.id} username={self.username} email={self.email}>"

    def to_dto(self) -> dto.User:
        return dto.User(
            db_id=self.id,
            username=self.username,
            email=self.email,
        )
