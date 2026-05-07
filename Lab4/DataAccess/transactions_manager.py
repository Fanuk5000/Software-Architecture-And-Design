from typing import Any, Callable, Generic, Type, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from DataAccess.abstracts import AbstractUnitOfWork
from DataAccess.repository import GenericRepository

T = TypeVar("T")


class SqlAlchemyUnitOfWork(
    AbstractUnitOfWork,
    Generic[T],
):
    def __init__(
        self,
        session_factory: Callable[[], AsyncSession],
        repository: Callable[[AsyncSession, Type[T]], GenericRepository[T] | Any[T]],
    ) -> None:
        self.__session_factory = session_factory
        self.__session: AsyncSession | None = None
        self.__repository: Callable[
            [AsyncSession, Type[T]], GenericRepository[T] | Any[T]
        ] = repository

    async def __aenter__(self):
        self.__session = self.__session_factory()
        if self.__session is None:
            raise RuntimeError("Failed to create a session.")
        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc_val, traceback):
        # if failure then rollback, otherwise commit
        if exc_type is not None:
            await self.rollback()

        if self.__session is not None:
            await self.__session.close()
        else:
            raise RuntimeError("Session was not created.")

    def get_repository(self, model: Type[T]) -> GenericRepository[T]:
        if self.__session is None:
            raise RuntimeError("Enter the unit of work before getting a repository.")
        return self.__repository(self.__session, model)

    async def commit(self):
        if self.__session is not None:
            await self.__session.commit()
        else:
            raise RuntimeError("Session was not created.")

    async def rollback(self):
        if self.__session is not None:
            await self.__session.rollback()
        else:
            raise RuntimeError("Session was not created.")
