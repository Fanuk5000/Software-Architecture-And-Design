from DataAccess.DataBase.initDB import async_session

#
from DataAccess.DataBase.models import User as UserModel
from DataAccess.repository import GenericRepository, UserRepository
from DataAccess.transactions_manager import SqlAlchemyUnitOfWork

#
from Services.booking import BookingService
from Services.certificate import CertificateService
from Services.quest import QuestRoomService
from Services.user import UserService


class ChangeUser(SystemExit):
    pass


async def _change_user() -> None:
    raise ChangeUser(0)


async def _exit() -> None:
    raise SystemExit(0)


class MenuEngine:
    def __init__(self) -> None:
        self.__general_uow = SqlAlchemyUnitOfWork(
            async_session, lambda s, m: GenericRepository(s, m)
        )
        self.__user_uow = SqlAlchemyUnitOfWork(
            async_session, lambda s, m: UserRepository(s)
        )

        self.__cert_serv = CertificateService(self.__general_uow)
        self.__quest_serv = QuestRoomService(self.__general_uow)
        self.__booking_serv = BookingService(
            self.__general_uow, self.__cert_serv, self.__quest_serv
        )
        self.__user_serv = UserService(self.__user_uow)

        # fmt: off
        self.__user_options = {
            "1": ("Check available quest rooms", self.__quest_serv.check_available_rooms),
            "2": ("Check room details", self.__quest_serv.get_room_by_id),
            "3": ("Book a quest room", self.__booking_serv.book_room),
            "4": ("View available certificates", self.__cert_serv.get_available_certs),
            "5": ("Change user", _change_user),
            "6": ("Exit", _exit),
        }

        self.__admin_options = {
            "1": ("Add a quest room", self.__quest_serv.add_room),
            "2": ("Delete a quest room", self.__quest_serv.delete_room),
            "3": ("Update a quest room", self.__quest_serv.update_room),
            "4": ("Add a certificate", self.__cert_serv.add_cert),
            "5": ("Delete a certificate", self.__cert_serv.delete_cert),
            "6": ("Update a certificate", self.__cert_serv.update_cert),
            "7": ("Check available quest rooms", self.__quest_serv.check_available_rooms),
            "8": ("Check room details", self.__quest_serv.get_room_by_id),
            "9": ("Book a quest room", self.__booking_serv.book_room),
            "10": ("View available certificates", self.__cert_serv.get_available_certs),
            "11": ("Change user", _change_user),
            "12": ("Exit", _exit),
        }
        # fmt: on

    async def register_user(self) -> int:
        print("\nRegistering a new user...")
        username = input("Enter username: ")
        password = input("Enter password: ")
        money = float(input("Enter initial money: "))
        is_admin_input = input("Is this user an admin? (yes/no): ")

        if is_admin_input.lower() not in ("yes", "no"):
            raise ValueError(
                "Invalid input for admin status. Please enter 'yes' or 'no'."
            )

        is_admin = is_admin_input.lower() == "yes"

        user_id = await self.__user_serv.register_user(
            username, password, money, is_admin
        )
        return user_id

    async def login_user(self) -> int:

        print("\nLogging in...")
        username = input("Enter username: ")
        password = input("Enter password: ")

        user_id = await self.__user_serv.login_user(username, password)
        return user_id

    async def display_menu(self, user_id: int) -> None:
        async with self.__user_uow as uow:
            user_repo: UserRepository = uow.get_repository(UserModel)  # pyright: ignore[reportAssignmentType]
            user = await user_repo.get_by_id(user_id)
            if user is None:
                raise ValueError("User not found")

            options = self.__admin_options if user.is_admin else self.__user_options

            while True:
                print("\nMenu:")
                for key, (description, _) in options.items():
                    print(f"{key}. {description}")
                choice = input("Select an option: ")
                action = options.get(choice)
                if action:
                    _, func = action
                    await func()
                else:
                    print("Invalid option. Please try again.")
