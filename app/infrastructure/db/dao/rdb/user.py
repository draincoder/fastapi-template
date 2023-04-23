from sqlalchemy import select, Result
from sqlalchemy.exc import MultipleResultsFound, NoResultFound, DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import dto
from app.core.utils.exceptions import (MultipleUsernameFound,
                                       NoUsernameFound,
                                       UsernameExist,
                                       MultipleEmailFound,
                                       NoEmailFound,
                                       EmailExist,
                                       RepoError)
from app.infrastructure.db.dao.rdb.base import BaseDAO
from app.infrastructure.db.models import User


class UserDao(BaseDAO[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_by_username(self, username: str) -> dto.User:
        user = await self._get_by_username(username)
        return user.to_dto()

    async def _get_by_username(self, username: str) -> User:
        result: Result[tuple[User]] = await self.session.execute(
            select(User).where(User.username == username)
        )
        try:
            user = result.scalar_one()
        except MultipleResultsFound as e:
            raise MultipleUsernameFound(username=username) from e
        except NoResultFound as e:
            raise NoUsernameFound(username=username) from e
        return user

    async def get_by_email(self, email: str) -> dto.User:
        user = await self._get_by_email(email)
        return user.to_dto()

    async def _get_by_email(self, email: str) -> User:
        result: Result[tuple[User]] = await self.session.execute(
            select(User).where(User.email == email)
        )
        try:
            user = result.scalar_one()
        except MultipleResultsFound as e:
            raise MultipleEmailFound(email=email) from e
        except NoResultFound as e:
            raise NoEmailFound(email=email) from e
        return user

    async def get_by_username_with_password(self, username: str) -> dto.UserWithCreds:
        user = await self._get_by_username(username)
        return user.to_dto().add_password(user.hashed_password)

    async def set_password(self, user: dto.User, hashed_password: str):
        assert user.db_id
        db_user = await self._get_by_id(user.db_id)
        db_user.hashed_password = hashed_password
        user.hashed_password = hashed_password

    async def create_user(self, user: dto.UserWithCreds) -> dto.User:
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password
        )
        self._save(db_user)
        try:
            await self.session.flush((db_user,))
        except IntegrityError as err:
            self._parse_error(err, db_user)
        return db_user.to_dto()

    def _parse_error(self, err: DBAPIError, user: dto.User) -> None:
        match err.__cause__.__cause__.constraint_name:  # type: ignore
            case "uq_users_email":
                raise EmailExist(user.email) from err
            case "uq_users_username":
                raise UsernameExist(user.username) from err
            case _:
                raise RepoError from err
