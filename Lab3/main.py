import asyncio

from DataAccess.DataBase.initDB import init_db
from UI.menu import ChangeUser, MenuEngine


async def main():
    await init_db()
    menu_engine = MenuEngine()
    have_user = input("Do you have an account? (yes/no): ").strip().lower()
    if have_user == "yes":
        user_id = await menu_engine.login_user()
        print("\nLogin successful!")
    else:
        user_id = await menu_engine.register_user()
        print("\nRegistration successful!")

    await menu_engine.display_menu(user_id)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting the application.")
    except ChangeUser:
        print("\nChanging user...")
        asyncio.run(main())
