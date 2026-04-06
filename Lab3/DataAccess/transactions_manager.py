from DataAccess.abstracteses import AbstractUnitOfWork
from DataAccess.repository import QuestRoomRepository
from sqlalchemy.ext.asyncio import async_sessionmaker


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory: async_sessionmaker):
        self.session_factory = session_factory
        self.session = None

    async def __aenter__(self):
        self.session = self.session_factory()
        self.quest_rooms = QuestRoomRepository(self.session)
        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc_val, traceback):
        # if failure then rollback, otherwise commit
        if exc_type is not None:
            await self.rollback()

        if self.session is not None:
            await self.session.close()
        else:
            raise RuntimeError("Session was not created.")

    async def commit(self):
        if self.session is not None:
            await self.session.commit()
        else:
            raise RuntimeError("Session was not created.")

    async def rollback(self):
        if self.session is not None:
            await self.session.rollback()
        else:
            raise RuntimeError("Session was not created.")
