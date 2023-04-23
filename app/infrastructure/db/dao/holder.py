from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.dao.rdb import UserDao


class HolderDao:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user = UserDao(self.session)

    async def commit(self):
        await self.session.commit()
