from __future__ import annotations

import logging
from datetime import timedelta, datetime

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from app.api.config.models.api import AuthConfig
from app.api.models.auth import Token
from app.core.models import dto
from app.core.utils.datetime_utils import tz_utc

logger = logging.getLogger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def jwt_provider() -> JWTProvider:
    raise NotImplementedError


class JWTProvider:
    def __init__(self, config: AuthConfig):
        self.config = config
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = config.secret_key
        self.algorythm = "HS256"
        self.access_token_expire = timedelta(minutes=config.token_expire_minutes)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def _create_access_token(self, data: dict, expires_delta: timedelta) -> Token:
        to_encode = data.copy()
        expire = datetime.now(tz=tz_utc) + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorythm)
        return Token(access_token=encoded_jwt, token_type="bearer")

    def create_user_token(self, user: dto.User) -> Token:
        return self._create_access_token(data={"sub": user.username}, expires_delta=self.access_token_expire)

    def get_payload_username(self, token: str) -> str:
        payload = jwt.decode(token, self.secret_key, algorithms=[self.algorythm])
        return payload.get("sub")
