from contextlib import asynccontextmanager

from DataAccess.DataBase.initDB import engine, init_db
from fastapi import FastAPI

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await engine.dispose()
