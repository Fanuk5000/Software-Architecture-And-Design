import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


async def main():
    from DataAccess.DataBase.initDB import init_db
    from UI.menu import MenuEngine

    global menu_engine

    await init_db()
    menu_engine = MenuEngine()
    await _start_menu()


async def _start_menu():
    have_user = input("Do you have an account? (yes/no): ").strip().lower()
    if have_user == "yes":
        user_id = await menu_engine.login_user()
        print("\nLogin successful!")
    else:
        user_id = await menu_engine.register_user()
        print("\nRegistration successful!")

    await menu_engine.display_menu(user_id)


if __name__ == "__main__":
    from UI.menu import ChangeUser

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, EOFError):
        print("\nExiting the application.")
    except ChangeUser:
        print("\nChanging user...")
        asyncio.run(_start_menu())
