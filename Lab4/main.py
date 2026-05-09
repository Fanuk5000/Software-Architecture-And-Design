from contextlib import asynccontextmanager

from API import quests
from DataAccess.DataBase.initDB import engine, init_db
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing database...")
    await init_db()
    yield
    await engine.dispose()


app = FastAPI(
    title="Quest Room API",
    description="API for managing quest rooms",
    lifespan=lifespan,
)


@app.get("/")
async def root():
    return {"message": "Hello this is a quest room API!"}


app.router.include_router(quests.router)
