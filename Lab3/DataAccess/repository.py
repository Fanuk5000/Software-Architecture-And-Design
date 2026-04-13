from typing import Generic, Optional, Type, TypeVar

import sqlalchemy.ext.asyncio
from DataAccess.abstracts import AbstractRepository
from DataAccess.DataBase.models import User as UserModel
from sqlalchemy import select

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

    async def update(self, entity: T) -> None:
        await self._session.merge(entity)

    async def delete(self, entity: T) -> None:
        await self._session.delete(entity)


class UserRepository(GenericRepository[UserModel]):
    def __init__(self, session: sqlalchemy.ext.asyncio.AsyncSession) -> None:
        super().__init__(session, UserModel)

    async def get_by_username(self, username: str) -> Optional[UserModel]:
        result = await self._session.execute(
            select(self._model).where(self._model.username == username)
        )
        return result.scalars().first()
