import asyncio


async def main():
    from DataAccess.DataBase.initDB import init_db
    from UI.menu import MenuEngine

    global menu_engine

    await init_db()
    menu_engine = MenuEngine()
    await _start_menu()


async def _start_menu():
    try:
        have_user = input("Do you have an account? (yes/no): ").strip().lower()

        if have_user == "yes":
            user_id = await menu_engine.login()
            print("\nLogin successful!")
        elif have_user == "no":
            user_id = await menu_engine.register()
            print("\nRegistration successful!")
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")
            await _start_menu()
            return
        await menu_engine.display_menu(user_id)
    except (KeyboardInterrupt, EOFError):
        print("\nExiting the application.")


async def _close_connection():
    from DataAccess.DataBase.initDB import engine

    print("Cleaning up resources...")
    try:
        await asyncio.shield(engine.dispose())
    except Exception as exc:
        print("Error disposing engine:", exc)


if __name__ == "__main__":
    from UI.menu import ChangeUser

    try:
        asyncio.run(main())
    except ChangeUser:
        print("\nChanging user...")
        asyncio.run(_start_menu())
    except (KeyboardInterrupt, EOFError):
        print("\nExiting the application.")
        asyncio.run(_close_connection())
