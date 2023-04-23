from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .auth import get_current_user, get_current_db_user
from .jwt import JWTProvider, jwt_provider
from .db import DbProvider, dao_provider
from app.api.config.models.api import AuthConfig


def setup_providers(app: FastAPI, pool: async_sessionmaker[AsyncSession], auth_config: AuthConfig):
    db_provider = DbProvider(pool=pool)
    jwt_provider_ = JWTProvider(auth_config)

    app.dependency_overrides[dao_provider] = db_provider.dao
    app.dependency_overrides[jwt_provider] = lambda: jwt_provider_
    app.dependency_overrides[get_current_user] = get_current_db_user
