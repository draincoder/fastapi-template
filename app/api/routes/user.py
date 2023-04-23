from fastapi import APIRouter, Depends

from app.api.depends import dao_provider, JWTProvider, jwt_provider
from app.api.depends.auth import get_current_user
from app.api.models import UserRegister
from app.api.services.user import create_new_user
from app.core.models import dto
from app.infrastructure.db.dao.holder import HolderDao

user_router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@user_router.get(
    "/info",
    description="Get info about current user",
    response_model=dto.User,
)
async def get_user_info(user: dto.User = Depends(get_current_user)) -> dto.User:
    return user


@user_router.post(
    "/register",
    description="Create new user",
    response_model=dto.User,
)
async def register_user(user: UserRegister,
                        jwt: JWTProvider = Depends(jwt_provider),
                        dao: HolderDao = Depends(dao_provider)) -> dto.User:
    return await create_new_user(user, jwt, dao)


@user_router.get(
    "/@{username}",
    description="Get info about user by username",
    response_model=dto.User,
)
async def get_user_by_id(username: str, dao: HolderDao = Depends(dao_provider)) -> dto.User:
    return await dao.user.get_by_username(username)


@user_router.get(
    "/{email}",
    description="Get info about user by email",
    response_model=dto.User,
)
async def get_user_by_email(email: str, dao: HolderDao = Depends(dao_provider)) -> dto.User:
    return await dao.user.get_by_email(email)
