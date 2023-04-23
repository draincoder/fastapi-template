from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.depends import dao_provider, JWTProvider, jwt_provider
from app.api.models import Token
from app.api.services.auth import authenticate_user
from app.infrastructure.db.dao.holder import HolderDao

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@auth_router.post(
    "/token",
    description="Create access token",
    response_model=Token,
)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                jwt: JWTProvider = Depends(jwt_provider),
                dao: HolderDao = Depends(dao_provider)) -> Token:
    user = await authenticate_user(form_data.username, form_data.password, dao, jwt)
    return jwt.create_user_token(user)
