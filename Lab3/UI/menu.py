from os import name as os_name
from subprocess import call
from time import sleep

from DataAccess.DataBase.initDB import async_session
from DataAccess.DataBase.models import User as UserModel

#
from DataAccess.repository import UserRepository
from DataAccess.transactions_manager import SqlAlchemyUnitOfWork
from Services.booking import BookingService
from Services.certificate import CertificateService
from Services.quest import QuestRoomService

#
from Services.user import UserService
from UI.menu_requests import (
    BookingRequests,
    CertificateRequests,
    QuestRoomRequests,
    UserRequests,
    make_uow,
)


class ChangeUser(SystemExit):
    pass


async def clear_screen() -> None:
    call("cls" if os_name == "nt" else "clear", shell=True)


async def _change_user() -> None:
    raise ChangeUser(0)


async def _exit() -> None:
    raise SystemExit(0)


class MenuEngine:
    def __init__(self) -> None:
        self.__user_uow = SqlAlchemyUnitOfWork(
            async_session, lambda s, m: UserRepository(s)
        )
        self.__user_serv = UserService(self.__user_uow)

        cert_serv = CertificateService(make_uow())
        quest_serv = QuestRoomService(make_uow())
        booking_serv = BookingService(make_uow(), cert_serv, quest_serv)

        self.__cert_requests = CertificateRequests(cert_serv)
        self.__quest_requests = QuestRoomRequests(quest_serv)
        self.__booking_requests = BookingRequests(booking_serv)
        self.__user_requests = UserRequests(self.__user_serv)

        # fmt: off
        self.__user_options = {
            "1": ("View all quest rooms", self.__quest_requests.see_all_rooms),
            "2": ("Check available quest rooms", self.__quest_requests.check_available_rooms),
            "3": ("Check room details", self.__quest_requests.get_room_by_id),
            "4": ("Book a quest room", self.__booking_requests.book_room),
            "5": ("View available certificates", self.__cert_requests.get_available_certs),
            "6": ("Change user", _change_user),
            "7": ("Exit", _exit),
        }

        self.__admin_options = {
            "1": ("View all quest rooms", self.__quest_requests.see_all_rooms),
            "2": ("Check available quest rooms", self.__quest_requests.check_available_rooms),
            "3": ("Add a quest room", self.__quest_requests.add_room),
            "4": ("Delete a quest room", self.__quest_requests.delete_room),
            "5": ("Update a quest room", self.__quest_requests.update_room),
            "6": ("Add a certificate", self.__cert_requests.add_cert),
            "7": ("Delete a certificate", self.__cert_requests.delete_cert),
            "8": ("Update a certificate", self.__cert_requests.update_cert),
            "9": ("Check available quest rooms", self.__quest_requests.check_available_rooms),
            "10": ("Check room details", self.__quest_requests.get_room_by_id),
            "11": ("Book a quest room", self.__booking_requests.book_room),
            "12": ("View available certificates", self.__cert_requests.get_available_certs),
            "13": ("Change user", _change_user),
            "14": ("Exit", _exit),
        }
        # fmt: on

    async def display_menu(self, user_id: int) -> None:
        async with self.__user_uow as uow:
            user_repo: UserRepository = uow.get_repository(UserModel)  # pyright: ignore[reportAssignmentType]
            user = await user_repo.get_by_id(user_id)
            if user is None:
                raise ValueError("User not found")

            options = self.__admin_options if user.is_admin else self.__user_options

            while True:
                sleep(0.5)
                await clear_screen()
                print("\nMenu:")
                for key, (description, _) in options.items():
                    print(f"{key}. {description}")
                choice = input("Select an option: ")
                action = options.get(choice)
                if action:
                    _, func = action
                    await func()
                    input("\nPress Enter to continue...")
                else:
                    print("Invalid option. Please try again.")

    async def login(self) -> int:
        return await self.__user_requests.login_user()

    async def register(self) -> int:
        return await self.__user_requests.register_user()
