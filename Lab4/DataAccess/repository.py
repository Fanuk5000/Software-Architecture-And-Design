from typing import Generic, Optional, Type, TypeVar

import sqlalchemy.ext.asyncio
from sqlalchemy import select

from DataAccess.abstracts import AbstractRepository

T = TypeVar("T")


class GenericRepository(AbstractRepository[T], Generic[T]):
    def __init__(
        self, session: sqlalchemy.ext.asyncio.AsyncSession, model: Type[T]
    ) -> None:
        self.__session = session
        self.__model = model

    async def add(self, entity: T) -> None:
        self.__session.add(entity)

    async def get_by_id(self, id: int) -> Optional[T]:
        return await self.__session.get(self.__model, id)

    async def get_all(self) -> list[T]:
        result = await self.__session.execute(select(self.__model))
        return list(result.scalars().all())

    async def get_one_by(self, **filters) -> Optional[T]:
        statement = select(self.__model).filter_by(**filters)
        result = await self.__session.execute(statement)
        return result.scalars().first()

    async def get_all_by(self, **filters) -> list[T] | list:
        statement = select(self.__model).filter_by(**filters)
        result = await self.__session.execute(statement)
        return list(result.scalars().all())

    async def update(self, entity: T) -> None:
        await self.__session.merge(entity)

    async def delete(self, entity: T) -> None:
        await self.__session.delete(entity)
