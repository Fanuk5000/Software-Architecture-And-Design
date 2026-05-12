from datetime import datetime

from DataAccess.DataBase import schemas
from DataAccess.DataBase.models import User as UserModel
from fastapi import APIRouter, Depends, HTTPException, status
from Services.booking import BookingService, CustomerRequest
from sqlalchemy.exc import SQLAlchemyError

from API.dependencies import (
    get_booking_service,
    get_current_admin_user,
    get_current_user,
)

admin_router = APIRouter(
    prefix="/bookings",
    tags=["bookings"],
    dependencies=[Depends(get_current_admin_user)],
)
public_router = APIRouter(prefix="/bookings", tags=["bookings"])


@public_router.post(
    "/book_room",
    status_code=status.HTTP_201_CREATED,
)
async def book_room(
    booking_request: schemas.CreateBooking,
    current_user: UserModel = Depends(get_current_user),
    service: BookingService = Depends(get_booking_service),
) -> None:
    date = booking_request.booking_date

    try:
        parsed_date = datetime.strptime(date, "%H-%d-%m")
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Invalid date format. Please Enter HH-DD-MM."
        )

    customer_request = CustomerRequest(
        user_id=current_user.id,
        room_id=booking_request.quest_room_id,
        customer_name=current_user.username,
        person_amount=booking_request.participants_amount,
        book_date=parsed_date,
    )

    try:
        await service.book_room(customer_request)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@public_router.get("/my")
async def get_my_bookings(
    current_user: UserModel = Depends(get_current_user),
    service: BookingService = Depends(get_booking_service),
):
    try:
        bookings = await service.get_bookings_by_username(current_user.username)
        return bookings
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


@admin_router.get("/all")
async def get_all_bookings(
    service: BookingService = Depends(get_booking_service),
):
    try:
        bookings = await service.get_all_bookings()
        return bookings
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
