from dataclasses import dataclass
from datetime import datetime
from typing import Any

from DataAccess.DataBase.models import Booking as BookingModel
from DataAccess.DataBase.models import QuestRoom as QuestRoomModel
from DataAccess.DataBase.models import User as UserModel

#
from DataAccess.repository import GenericRepository
from DataAccess.unit_of_work import SqlAlchemyUnitOfWork

#
from Services.certificate import CertificateService
from Services.quest import QuestRoomService


@dataclass
class CustomerRequest:
    user_id: int
    room_id: int
    customer_name: str
    person_amount: int
    book_date: datetime


class BookingService:
    def __init__(
        self,
        uow_factory: SqlAlchemyUnitOfWork,
        cert_service: CertificateService | None = None,
        quest_service: QuestRoomService | None = None,
    ) -> None:
        self.__uow: SqlAlchemyUnitOfWork[Any] = uow_factory

        self.__certService = (
            CertificateService(uow_factory) if cert_service is None else cert_service
        )
        self.__questService = (
            QuestRoomService(uow_factory) if quest_service is None else quest_service
        )

    async def book_room(self, customer_request: CustomerRequest):
        async with self.__uow as uow:
            bookings_repo = uow.get_repository(BookingModel)
            rooms_repo = uow.get_repository(QuestRoomModel)
            user_repo = uow.get_repository(UserModel)

            available_rooms = await self.__questService.check_available_rooms(
                date=customer_request.book_date,
                rooms_repo=rooms_repo,
                bookings_repo=bookings_repo,
            )

            # Verify booking details before proceeding
            user: UserModel | None = await user_repo.get_by_id(customer_request.user_id)
            await self.__verify_booking(
                customer_request, available_rooms, rooms_repo, user
            )

            # If verification passed, proceed with booking
            chosen_room: QuestRoomModel | None = await rooms_repo.get_by_id(
                customer_request.room_id
            )
            if chosen_room is None:
                raise ValueError("Room not found")

            # Calculate discounted price if user has a certificate
            discounted_price = await self.__calculate_discounted_price(
                chosen_room.price,
                user,  # pyright: ignore[reportArgumentType]
                customer_request.user_id,  # pyright: ignore[reportArgumentType]
            )
            if user.money < discounted_price:  # pyright: ignore[reportOptionalMemberAccess]
                raise ValueError("Not enough money")
            user.money -= discounted_price  # pyright: ignore[reportOptionalMemberAccess]
            await user_repo.update(user)

            new_booking = BookingModel(
                quest_room_id=customer_request.room_id,
                customer_name=customer_request.customer_name,
                participants_amount=customer_request.person_amount,
                booking_date=customer_request.book_date,
            )

            await bookings_repo.add(new_booking)
            await uow.commit()

    async def __verify_booking(
        self,
        customer_request: CustomerRequest,
        available_rooms: list[QuestRoomModel] | list[None],
        rooms_repo: GenericRepository[QuestRoomModel],
        user: UserModel | None,
    ) -> bool:
        if user is None:
            raise ValueError("User not found")

        if not available_rooms:
            raise ValueError("There is no available room")

        chosen_room: QuestRoomModel | None = await rooms_repo.get_by_id(
            customer_request.room_id
        )

        if not isinstance(chosen_room, QuestRoomModel):
            raise ValueError("Room not found")
        min_parts = chosen_room.min_participants
        max_parts = chosen_room.max_participants

        if (
            customer_request.person_amount < min_parts
            or customer_request.person_amount > max_parts
        ):
            raise ValueError(
                f"Participants amount is out of range must be lower than {max_parts} and higher than {min_parts}"
            )

        return True

    async def __calculate_discounted_price(
        self,
        room_price: int,
        user: UserModel,
        user_id: int,
    ) -> int:
        if user.has_certificate:
            discount_percentage = await self.__certService.use_cert(user_id)
        else:
            discount_percentage = 0

        discounted_price = room_price * (1 - discount_percentage / 100)

        return int(discounted_price)
