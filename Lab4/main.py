from contextlib import asynccontextmanager

from API import bookigs, certs, quests, users
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


routers = (
    quests.admin_router,
    quests.public_router,
    users.admin_router,
    users.public_router,
    bookigs.admin_router,
    bookigs.public_router,
    certs.admin_router,
    certs.public_router,
)

for router in routers:
    app.router.include_router(router)
