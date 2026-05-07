from typing import Generic, Optional, Type, TypeVar

import sqlalchemy.ext.asyncio
from sqlalchemy import select

from DataAccess.abstracts import AbstractRepository

T = TypeVar("T")


class GenericRepository(AbstractRepository[T], Generic[T]):
    def __init__(
        self, session: sqlalchemy.ext.asyncio.AsyncSession, model: Type[T]
    ) -> None:
        self._session = session
        self._model = model

    async def add(self, entity: T) -> None:
        self._session.add(entity)

    async def get_by_id(self, id: int) -> Optional[T]:
        return await self._session.get(self._model, id)

    async def get_all(self) -> list[T]:
        result = await self._session.execute(select(self._model))
        return list(result.scalars().all())

    async def get_one_by(self, **filters) -> Optional[T]:
        statement = select(self._model).filter_by(**filters)
        result = await self._session.execute(statement)
        return result.scalars().first()

    async def update(self, entity: T) -> None:
        await self._session.merge(entity)

    async def delete(self, entity: T) -> None:
        await self._session.delete(entity)
