from fastapi import HTTPException
from starlette import status

from app.api.depends import JWTProvider
from app.core.models import dto
from app.core.utils.exceptions import NoUsernameFound
from app.infrastructure.db.dao.holder import HolderDao


async def authenticate_user(username: str, password: str, dao: HolderDao, jwt: JWTProvider) -> dto.User:
    http_status_401 = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        user = await dao.user.get_by_username_with_password(username)
    except NoUsernameFound:
        raise http_status_401
    if not jwt.verify_password(password, user.hashed_password or ""):
        raise http_status_401
    return user.without_password()
