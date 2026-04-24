from datetime import datetime
from typing import TYPE_CHECKING

from DataAccess.DataBase.initDB import async_session
from DataAccess.DataBase.models import Certificate as CertificateModel
from DataAccess.DataBase.models import QuestRoom as QuestRoomModel

#
from DataAccess.repository import GenericRepository
from DataAccess.transactions_manager import SqlAlchemyUnitOfWork

#
from Services.shared_dataclasses import CustomerRequest

if TYPE_CHECKING:
    from Services.booking import BookingService
    from Services.certificate import CertificateService
    from Services.quest import QuestRoomService
    from Services.user import UserService

# Global variable to store the current username
user_id = 0
username = ""


def make_uow() -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(async_session, lambda s, m: GenericRepository(s, m))


class CertificateRequests:
    def __init__(self, cert_serv: "CertificateService") -> None:
        self.__cert_serv = cert_serv

    async def add_cert(self) -> None:
        name = input("Enter certificate name: ")
        discount_percentage = int(input("Enter discount percentage: "))
        user_id = int(input("Enter user ID for this certificate: "))
        cert = CertificateModel(
            name=name, discount_percentage=discount_percentage, user_id=user_id
        )

        await self.__cert_serv.add_cert(cert, user_id)

    async def delete_cert(self) -> None:
        cert_id = int(input("Enter certificate ID to delete: "))
        await self.__cert_serv.delete_cert(cert_id, user_id)

    async def update_cert(self) -> None:
        cert_id = int(input("Enter certificate ID to update: "))
        name = input("Enter new certificate name: ")
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
            name=name,
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
                text = f"ID: {cert.id}, Name: {cert.name}, Discount: {cert.discount_percentage}%"  # pyright: ignore[reportOptionalMemberAccess]
                print(text)


class QuestRoomRequests:
    def __init__(self, quest_serv: "QuestRoomService") -> None:
        self.__quest_serv = quest_serv

    async def see_all_rooms(self) -> None:
        rooms = await self.__quest_serv.see_all_rooms()
        if not rooms:
            print("No rooms exist.")
        else:
            print("Existing rooms:")
            for room in rooms:
                if room is not None:
                    print(
                        f"ID: {room.id}, Name: {room.name}, Price: {room.price}, Min Participants: {room.min_participants}, Max Participants: {room.max_participants}, Description: {room.description}, Working Hours: {room.working_hours}"
                    )

    async def check_available_rooms(self) -> None:
        book_date = input("Enter a booking date (HH-DD-MM): ")
        book_date = datetime.strptime(book_date, "%H-%d-%m")
        available_rooms = await self.__quest_serv.check_available_rooms(book_date)
        if not available_rooms:
            print("No rooms available on this date.")

        print("Available rooms:")
        for room in available_rooms:
            if room is not None:
                print(
                    f"ID: {room.id}, Name: {room.name}, Price: {room.price}, Min Participants: {room.min_participants}, Max Participants: {room.max_participants}, Description: {room.description}, Working Hours: {room.working_hours}"
                )

    async def get_room_by_id(self) -> None:
        room_id = int(input("Enter room ID: "))
        room = await self.__quest_serv.get_room_by_id(room_id)
        if room is None:
            print("Room not found.")
        else:
            print(
                f"ID: {room.id}, Name: {room.name}, Price: {room.price}, Min Participants: {room.min_participants}, Max Participants: {room.max_participants}, Description: {room.description}, Working Hours: {room.working_hours}"
            )

    async def add_room(self) -> None:
        name = input("Enter room name: ")
        price = float(input("Enter room price: "))
        min_persons = int(input("Enter minimum number of participants: "))
        max_persons = int(input("Enter maximum number of participants: "))
        working_hours = input("Enter working hours (e.g., 10-22): ")
        description = input("Enter room description (optional): ")

        new_room = QuestRoomModel(
            name=name,
            price=price,
            min_participants=min_persons,
            max_participants=max_persons,
            working_hours=working_hours,
            description=description,
        )

        try:
            await self.__quest_serv.add_room(new_room)
        except ValueError:
            print("Invalid time format. Please try again.")
            await self.add_room()

    async def delete_room(self) -> None:
        room_id = int(input("Enter room ID to delete: "))
        await self.__quest_serv.delete_room(room_id)

    async def update_room(self) -> None:
        room_id = int(input("Enter room ID to update: "))
        name = input("Enter new room name: ")
        price = float(input("Enter new room price: "))
        min_persons = int(input("Enter new minimum number of participants: "))
        max_persons = int(input("Enter new maximum number of participants: "))
        working_hours = input("Enter new working hours (e.g., 10-22): ")
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

        try:
            await self.__quest_serv.update_room(updated_room)
        except ValueError:
            print("Invalid time format. Please try again.")
            await self.update_room()


class BookingRequests:
    def __init__(self, booking_serv: "BookingService") -> None:
        self.__booking_serv = booking_serv

    async def book_room(self) -> None:
        room_id = int(input("Enter room ID to book: "))
        person_amount = int(input("Enter number of participants: "))
        book_date = input("Enter a booking date (HH-DD-MM): ")

        # Parse hour-day-month and set current year to avoid year=1900 issues
        try:
            parsed = datetime.strptime(book_date, "%H-%d-%m")
            parsed = parsed.replace(year=datetime.now().year)
            book_date = parsed
        except ValueError:
            print("Invalid date format. Please use HH-DD-MM.")
            return await self.book_room()

        customer_request = CustomerRequest(
            user_id=user_id,
            customer_name=username,
            room_id=room_id,
            person_amount=person_amount,
            book_date=book_date,
        )

        try:
            await self.__booking_serv.book_room(customer_request)
        except ValueError as e:
            print(f"Booking failed: {e}")


class MenuRequests:
    def __init__(self) -> None:
        self.__cert_serv = CertificateService(make_uow())
        self.__quest_serv = QuestRoomService(make_uow())
        self.__booking_serv = BookingService(
            make_uow(), self.__cert_serv, self.__quest_serv
        )


class UserRequests:
    def __init__(self, userService: UserService) -> None:
        self.__user_serv = userService

    async def register_user(self) -> int:
        global username, user_id
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
        global username, user_id
        print("\nLogging in...")
        username = input("Enter username: ")
        password = input("Enter password: ")

        try:
            user_id = await self.__user_serv.login_user(username, password)
        except ValueError:
            print(
                "Invalid username or password, or user is not active. Please try again."
            )
            return await self.login_user()
        return user_id
