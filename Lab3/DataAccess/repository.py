from typing import Generic, Optional, Type, TypeVar

import sqlalchemy.ext.asyncio
from DataAccess.abstracts import AbstractRepository
from sqlalchemy import select

T = TypeVar("T")


class GenericRepository(AbstractRepository[T], Generic[T]):
    def __init__(
        self, session: sqlalchemy.ext.asyncio.AsyncSession, model: Type[T]
    ) -> None:
        self.session = session
        self.model = model

    async def add(self, entity: T) -> None:
        self.session.add(entity)

    async def get_by_id(self, id: int) -> Optional[T]:
        return await self.session.get(self.model, id)

    async def get_all(self) -> list[T]:
        result = await self.session.execute(select(self.model))
        return list(result.scalars().all())

    async def update(self, entity: T) -> None:
        await self.session.merge(entity)

    async def delete(self, entity: T) -> None:
        await self.session.delete(entity)
