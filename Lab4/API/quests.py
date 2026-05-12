from datetime import datetime
from typing import TYPE_CHECKING

from DataAccess.DataBase import schemas
from fastapi import APIRouter, Depends, HTTPException, status
from Services.quest import QuestRoomService
from sqlalchemy.exc import SQLAlchemyError

from API.dependencies import get_current_admin_user, get_quest_service

if TYPE_CHECKING:
    pass


admin_router = APIRouter(
    prefix="/quests", tags=["quests"], dependencies=[Depends(get_current_admin_user)]
)
public_router = APIRouter(prefix="/quests", tags=["quests"])


@admin_router.get("/", response_model=list[schemas.ReadQuestRoom])
async def get_quests(
    service: QuestRoomService = Depends(get_quest_service),
) -> list[schemas.ReadQuestRoom]:
    try:
        rooms = await service.see_all_rooms()

        if not rooms:
            return []

        return rooms  # type: ignore[return-value]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@public_router.get("/available/{date}", response_model=list[schemas.ReadQuestRoom])
async def get_available_quests(
    date: str, service: QuestRoomService = Depends(get_quest_service)
):
    try:
        try:
            parsed_date = datetime.strptime(date, "%H-%d-%m")
        except ValueError:
            raise HTTPException(
                status_code=400, detail="Invalid date format. Please Enter HH-DD-MM."
            )

        available_rooms = await service.check_available_rooms(parsed_date)

        if not available_rooms:
            return []
        return available_rooms  # type: ignore[return-value]
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@public_router.get("/{id}", response_model=schemas.ReadQuestRoom)
async def get_quest_by_id(
    id: int, service: QuestRoomService = Depends(get_quest_service)
) -> schemas.ReadQuestRoom:
    try:
        room = await service.get_room_by_id(id)
        if not room:
            raise HTTPException(status_code=404, detail="Quest room not found")
        return room  # type: ignore[return-value]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@admin_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_quest(
    room: schemas.CreateQuestRoom,
    service: QuestRoomService = Depends(get_quest_service),
) -> None:
    try:
        await service.add_room(room)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@admin_router.put("/{id}", status_code=status.HTTP_201_CREATED)
async def update_quest(
    id: int,
    room: schemas.CreateQuestRoom,
    service: QuestRoomService = Depends(get_quest_service),
) -> None:
    try:
        await service.update_room(id, room)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@admin_router.delete("/{id}", status_code=status.HTTP_201_CREATED)
async def delete_quest(
    id: int, service: QuestRoomService = Depends(get_quest_service)
) -> None:
    try:
        await service.delete_room(id)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
