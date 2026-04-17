import re

from DataAccess.DataBase.initDB import Base
from sqlalchemy import (
    Boolean,
    Date,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, validates


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False
    )
    money: Mapped[int] = mapped_column(Integer, default=0)
    password: Mapped[str] = mapped_column(String, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    has_certificate: Mapped[bool] = mapped_column(Boolean, default=False)


class QuestRoom(Base):
    __tablename__ = "quest_rooms"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    max_participants: Mapped[int] = mapped_column(Integer, nullable=False)
    min_participants: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    working_hours: Mapped[str] = mapped_column(String, nullable=False)

    @validates("working_hours")
    def validate_working_hours(self, key, value: str) -> str:
        # Generic "num-num" pattern (no '-' inside each side)
        match = re.match(r"^(\d{1,2})-(\d{1,2})$", value)
        if not match:
            raise ValueError("working_hours must match 'num-num' (e.g. '10-22')")
        start, end = int(match.group(1)), int(match.group(2))
        if not (0 <= start < 24 and 0 <= end < 24):
            raise ValueError("Hours must be between 0 and 23")
        if start >= end:
            raise ValueError("Start hour must be less than end hour")
        return value

    description: Mapped[str] = mapped_column(String, nullable=True)


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    quest_room_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("quest_rooms.id"), nullable=False
    )
    customer_name: Mapped[str] = mapped_column(String, nullable=False)
    participants_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    booking_date: Mapped[Date] = mapped_column(Date, nullable=False)


class Certificate(Base):
    __tablename__ = "certificates"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    discount_percentage: Mapped[int] = mapped_column(Integer, nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
