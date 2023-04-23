from app.api.depends import JWTProvider
from app.api.models import UserRegister
from app.core.models import dto
from app.infrastructure.db.dao.holder import HolderDao


async def create_new_user(
        user: UserRegister,
        jwt: JWTProvider,
        dao: HolderDao
) -> dto.User:
    hashed_password = jwt.get_password_hash(user.password)
    user = await dao.user.create_user(user.to_dto().add_password(hashed_password))
    await dao.commit()
    return user
