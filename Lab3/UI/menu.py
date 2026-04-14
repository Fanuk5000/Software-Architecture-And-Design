from datetime import datetime

from DataAccess.DataBase.initDB import async_session
from DataAccess.DataBase.models import Certificate as CertificateModel
from DataAccess.DataBase.models import QuestRoom as QuestRoomModel
from DataAccess.DataBase.models import User as UserModel

#
from DataAccess.repository import GenericRepository, UserRepository
from DataAccess.transactions_manager import SqlAlchemyUnitOfWork

#
from Services.booking import BookingService
from Services.certificate import CertificateService
from Services.quest import QuestRoomService
from Services.shared_dataclasses import CustomerRequest
from Services.user import UserService


class ChangeUser(SystemExit):
    pass


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
        self.__menu_requests = _MenuRequests()

        # fmt: off
        self.__user_options = {
            "1": ("View all quest rooms", self.__menu_requests.see_all_rooms),
            "2": ("Check available quest rooms", self.__menu_requests.check_available_rooms),
            "3": ("Check room details", self.__menu_requests.get_room_by_id),
            "4": ("Book a quest room", self.__menu_requests.book_room),
            "5": ("View available certificates", self.__menu_requests.get_available_certs),
            "6": ("Change user", _change_user),
            "7": ("Exit", _exit),
        }

        self.__admin_options = {
            "1": ("View all quest rooms", self.__menu_requests.see_all_rooms),
            "2": ("Check available quest rooms", self.__menu_requests.check_available_rooms),
            "3": ("Add a quest room", self.__menu_requests.add_room),
            "4": ("Delete a quest room", self.__menu_requests.delete_room),
            "5": ("Update a quest room", self.__menu_requests.update_room),
            "6": ("Add a certificate", self.__menu_requests.add_cert),
            "7": ("Delete a certificate", self.__menu_requests.delete_cert),
            "8": ("Update a certificate", self.__menu_requests.update_cert),
            "9": ("Check available quest rooms", self.__menu_requests.check_available_rooms),
            "10": ("Check room details", self.__menu_requests.get_room_by_id),
            "11": ("Book a quest room", self.__menu_requests.book_room),
            "12": ("View available certificates", self.__menu_requests.get_available_certs),
            "13": ("Change user", _change_user),
            "14": ("Exit", _exit),
        }
        # fmt: on

    async def register_user(self) -> int:
        print("\nRegistering a new user...")
        username = input("Enter username: ")
        password = input("Enter password: ")
        money = float(input("Enter initial money: "))
        is_admin_input = input("Is this user an admin? (yes/no): ")

        if is_admin_input.lower() not in ("yes", "no"):
            print("Invalid input for admin status. Please enter 'yes' or 'no'.")
            return await self.register_user()

        is_admin = is_admin_input.lower() == "yes"

        try:
            user_id = await self.__user_serv.register_user(
                username, password, money, is_admin
            )
        except ValueError:
            print("Username already exists or user is not active. Please try again.")
            return await self.register_user()
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


class _MenuRequests:
    def __init__(self) -> None:

        self.__general_uow = SqlAlchemyUnitOfWork(
            async_session, lambda s, m: GenericRepository(s, m)
        )
        self.__cert_serv = CertificateService(self.__general_uow)
        self.__quest_serv = QuestRoomService(self.__general_uow)
        self.__booking_serv = BookingService(
            self.__general_uow, self.__cert_serv, self.__quest_serv
        )

    async def see_all_rooms(self) -> None:
        rooms = await self.__quest_serv.see_all_rooms()
        if not rooms:
            print("No rooms available.")
        else:
            print("Available rooms:")
            for room in rooms:
                print(f"ID: {room.id}, Name: {room.name}, Price: {room.price}")  # pyright: ignore[reportOptionalMemberAccess]

    async def check_available_rooms(self) -> None:
        book_date = input("Enter a booking date (HH-DD-MM): ")
        book_date = datetime.strptime(book_date, "%H-%d-%m")
        available_rooms = await self.__quest_serv.check_available_rooms(book_date)
        if not available_rooms:
            print("No rooms available on this date.")

        print("Available rooms:")
        for room in available_rooms:
            print(f"ID: {room.id}, Name: {room.name}, Price: {room.price}")  # pyright: ignore[reportOptionalMemberAccess]

    async def get_room_by_id(self) -> None:
        room_id = int(input("Enter room ID: "))
        room = await self.__quest_serv.get_room_by_id(room_id)
        if room is None:
            print("Room not found.")
        else:
            print(f"ID: {room.id}, Name: {room.name}, Price: {room.price}")

    async def book_room(self) -> None:
        user_id = int(input("Enter your user ID: "))
        customer_name = input("Enter your name: ")
        room_id = int(input("Enter room ID to book: "))
        person_amount = int(input("Enter number of participants: "))
        book_date = input("Enter a booking date (HH-DD-MM): ")

        book_date = datetime.strptime(book_date, "%H-%d-%m")

        customer_request = CustomerRequest(
            user_id=user_id,
            customer_name=customer_name,
            room_id=room_id,
            person_amount=person_amount,
            book_date=book_date,
        )

        await self.__booking_serv.book_room(customer_request)

    async def add_room(self) -> None:
        name = input("Enter room name: ")
        price = float(input("Enter room price: "))
        min_persons = int(input("Enter minimum number of participants: "))
        max_persons = int(input("Enter maximum number of participants: "))
        working_hours = input("Enter working hours (e.g., 10:00-22:00): ")
        description = input("Enter room description (optional): ")

        new_room = QuestRoomModel(
            name=name,
            price=price,
            min_participants=min_persons,
            max_participants=max_persons,
            working_hours=working_hours,
            description=description,
        )

        await self.__quest_serv.add_room(new_room)

    async def delete_room(self) -> None:
        room_id = int(input("Enter room ID to delete: "))
        await self.__quest_serv.delete_room(room_id)

    async def update_room(self) -> None:
        room_id = int(input("Enter room ID to update: "))
        name = input("Enter new room name: ")
        price = float(input("Enter new room price: "))
        min_persons = int(input("Enter new minimum number of participants: "))
        max_persons = int(input("Enter new maximum number of participants: "))
        working_hours = input("Enter new working hours (e.g., 10:00-22:00): ")
        description = input("Enter new room description (optional): ")

        updated_room = QuestRoomModel(
            id=room_id,
            name=name,
            price=price,
            min_participants=min_persons,
            max_participants=max_persons,
            working_hours=working_hours,
            description=description,
        )

        await self.__quest_serv.update_room(updated_room)

    async def add_cert(self) -> None:
        code = input("Enter certificate code: ")
        discount_percentage = int(input("Enter discount percentage: "))
        user_id = int(input("Enter user ID for this certificate: "))
        cert = CertificateModel(
            code=code, discount_percentage=discount_percentage, user_id=user_id
        )

        await self.__cert_serv.add_cert(cert)

    async def delete_cert(self) -> None:
        cert_id = int(input("Enter certificate ID to delete: "))
        await self.__cert_serv.delete_cert(cert_id)

    async def update_cert(self) -> None:
        cert_id = int(input("Enter certificate ID to update: "))
        code = input("Enter new certificate code: ")
        discount_percentage = int(input("Enter new discount percentage: "))
        user_id = int(input("Enter new user ID for this certificate: "))
        is_active_input = input("Is the certificate active? (yes/no): ")

        if is_active_input.lower() not in ("yes", "no"):
            raise ValueError(
                "Invalid input for active status. Please enter 'yes' or 'no'."
            )

        is_active = is_active_input.lower() == "yes"

        updated_cert = CertificateModel(
            id=cert_id,
            code=code,
            discount_percentage=discount_percentage,
            user_id=user_id,
            is_active=is_active,
        )

        await self.__cert_serv.update_cert(updated_cert)

    async def get_available_certs(self) -> None:
        certs = await self.__cert_serv.get_available_certs()
        if not certs:
            print("No certificates available.")
        else:
            print("Available certificates:")
            for cert in certs:
                text = f"ID: {cert.id}, Code: {cert.code}, Discount: {cert.discount_percentage}%"  # pyright: ignore[reportOptionalMemberAccess]
                print(text)
