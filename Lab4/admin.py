from os import environ as os_environ

from DataAccess.DataBase.initDB import async_session
from DataAccess.repository import GenericRepository
from DataAccess.unit_of_work import SqlAlchemyUnitOfWork
from dotenv import load_dotenv
from Services.user import UserService

load_dotenv()


async def create_admin():
    admin_username = os_environ.get("ADMIN_USERNAME")
    admin_password = os_environ.get("ADMIN_PASSWORD")

    if not admin_username or not admin_password:
        raise ValueError(
            "Admin username and password must be set in environment variables"
        )

    uow = SqlAlchemyUnitOfWork(async_session, lambda s, m: GenericRepository(s, m))
    service = UserService(uow)
    try:
        # Пробуємо створити. Якщо юзер вже є - сервіс кине ValueError, і ми просто підемо далі
        await service.register_user(
            username=admin_username, password=admin_password, money=0.0, is_admin=True
        )
        print("Admin user created successfully.", flush=True)
    except ValueError:
        print("Admin user already exists. Skipping creation.", flush=True)
