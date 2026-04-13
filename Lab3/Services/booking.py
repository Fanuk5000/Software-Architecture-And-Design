from DataAccess.DataBase.models import Booking as BookingModel
from DataAccess.DataBase.models import QuestRoom as QuestRoomModel
from DataAccess.DataBase.models import User as UserModel
from DataAccess.DataBase.schemas import QuestRoom

#
from DataAccess.repository import GenericRepository
from DataAccess.transactions_manager import SqlAlchemyUnitOfWork

#
from Services.certificate import CertificateService
from Services.quest import QuestRoomService
from Services.shared_dataclasses import CustomerRequest


class BookingService:
    def __init__(
        self,
        uow_factory: SqlAlchemyUnitOfWork,
        cert_service: CertificateService | None = None,
        quest_service: QuestRoomService | None = None,
    ) -> None:
        self.__uow = uow_factory

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

            discount_percentage = await self.__certService.use_cert(
                customer_request.user_id, customer_request.user_id
            )

            await self.__verify_booking(customer_request, available_rooms, rooms_repo)

            user = await user_repo.get_by_id(customer_request.user_id)
            if user is None:
                raise ValueError("User not found")

            chosen_room = await rooms_repo.get_by_id(customer_request.room_id)
            if chosen_room is None:
                raise ValueError("Room not found")

            discounted_price = chosen_room.price * (1 - discount_percentage / 100)
            if user.money < discounted_price:
                raise ValueError("Not enough money")

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
        available_rooms: list[QuestRoom] | list[None],
        rooms_repo: GenericRepository[QuestRoomModel],
    ) -> bool:
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
