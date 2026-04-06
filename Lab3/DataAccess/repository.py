import sqlalchemy.ext.asyncio
from DataAccess.abstracteses import AbstractRepository
from DataAccess.DB.models import QuestRoom
from sqlalchemy import select


class QuestRoomRepository(AbstractRepository):
    def __init__(self, session: sqlalchemy.ext.asyncio.AsyncSession) -> None:
        self.session = session

    async def add(self, entity: QuestRoom) -> None:
        self.session.add(entity)

    async def get_by_id(self, id: int) -> QuestRoom | None:
        return await self.session.get(QuestRoom, id)

    async def get_all(self) -> list[QuestRoom]:
        result = await self.session.execute(select(QuestRoom))
        return list(result.scalars().all())

    async def update(self, entity: QuestRoom) -> None:
        await self.session.merge(entity)

    async def delete(self, entity: QuestRoom) -> None:
        await self.session.delete(entity)
