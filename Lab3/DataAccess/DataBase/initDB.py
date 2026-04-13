import json
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./quest_rooms.db"

debug = False
try:
    with open("db_config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
        debug: bool = config.get("Debug", False)
except FileNotFoundError:
    print("db_config.json not found. Using default settings.")
except json.JSONDecodeError:
    print("Error decoding db_config.json. Using default settings.")
except IOError:
    print("Error reading db_config.json. Using default settings.")

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # Only needed for SQLite
    echo=debug,  # Optional: prints SQL queries to the console for debugging
)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def init_db() -> None:
    # Ensure models are imported so Base.metadata is populated.
    from DataAccess.DataBase import models  # noqa: F401

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Returns a generator for DB session"""
    async with async_session() as session:
        yield session
