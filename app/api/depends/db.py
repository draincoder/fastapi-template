from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from app.infrastructure.db.dao.holder import HolderDao


def dao_provider() -> HolderDao:
    raise NotImplementedError


class DbProvider:
    def __init__(self, pool: async_sessionmaker[AsyncSession]):
        self.pool = pool

    async def dao(self):
        async with self.pool() as session:
            yield HolderDao(session=session)
