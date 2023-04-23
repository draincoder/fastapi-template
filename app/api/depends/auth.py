import logging

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from starlette import status

from app.api.depends.db import dao_provider
from app.api.depends.jwt import JWTProvider, jwt_provider
from app.core.models import dto
from app.core.utils.exceptions import NoUsernameFound
from app.infrastructure.db.dao.holder import HolderDao

logger = logging.getLogger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_current_user(token: str = Depends(oauth2_scheme)) -> dto.User:  # token only for authorize button in Swagger
    raise NotImplementedError


async def get_current_db_user(
        jwt: JWTProvider = Depends(jwt_provider),
        token: str = Depends(oauth2_scheme),
        dao: HolderDao = Depends(dao_provider)
) -> dto.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        username = jwt.get_payload_username(token)
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    try:
        user = await dao.user.get_by_username(username)
    except NoUsernameFound:
        raise credentials_exception
    return user
