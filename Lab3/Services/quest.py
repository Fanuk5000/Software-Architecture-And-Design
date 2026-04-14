from datetime import datetime
from typing import Any

from DataAccess.DataBase.models import Booking as BookingModel
from DataAccess.DataBase.models import QuestRoom as QuestRoomModel

#
from DataAccess.DataBase.schemas import Booking, QuestRoom
from DataAccess.repository import GenericRepository
from DataAccess.transactions_manager import SqlAlchemyUnitOfWork


class QuestRoomService:
    def __init__(
        self,
        uow_factory: SqlAlchemyUnitOfWork,
    ) -> None:
        self.__uow = uow_factory

    async def check_available_rooms(
        self,
        date: datetime,
        rooms_repo: GenericRepository[Any] | None = None,
        bookings_repo: GenericRepository[Any] | None = None,
    ) -> list[QuestRoom] | list[None]:
        async with self.__uow as uow:
            available_rooms: list[QuestRoom] = []

            if rooms_repo is None:
                rooms_repo = uow.get_repository(QuestRoomModel)
            if bookings_repo is None:
                bookings_repo = uow.get_repository(BookingModel)

            all_rooms: list[QuestRoom] = await rooms_repo.get_all()
            all_bookings: list[Booking] = await bookings_repo.get_all()

            for room in all_rooms:
                if all(
                    room.id != booking.quest_room_id and booking.booking_date != date
                    for booking in all_bookings
                ):
                    available_rooms.append(room)
            return available_rooms

    async def see_all_rooms(self) -> list[QuestRoom] | list[None]:
        async with self.__uow as uow:
            rooms_repo = uow.get_repository(QuestRoomModel)
            return await rooms_repo.get_all()

    async def add_room(self, room: QuestRoomModel) -> None:
        async with self.__uow as uow:
            rooms_repo = uow.get_repository(QuestRoomModel)
            await rooms_repo.add(room)
            await uow.commit()

    async def delete_room(self, room_id: int) -> None:
        async with self.__uow as uow:
            rooms_repo = uow.get_repository(QuestRoomModel)
            room_to_delete = await rooms_repo.get_by_id(room_id)
            if room_to_delete is None:
                raise ValueError("Room not found")
            await rooms_repo.delete(room_to_delete)
            await uow.commit()

    async def update_room(self, room: QuestRoomModel) -> None:
        async with self.__uow as uow:
            rooms_repo = uow.get_repository(QuestRoomModel)
            room_to_update = await rooms_repo.get_by_id(room.id)
            if room_to_update is None:
                raise ValueError("Room not found")
            await rooms_repo.update(room)
            await uow.commit()

    async def get_room_by_id(self, room_id: int) -> QuestRoomModel | None:
        async with self.__uow as uow:
            rooms_repo = uow.get_repository(QuestRoomModel)
            return await rooms_repo.get_by_id(room_id)
