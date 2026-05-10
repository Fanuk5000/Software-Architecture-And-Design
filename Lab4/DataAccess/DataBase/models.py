import re

from sqlalchemy import (
    Boolean,
    Date,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, validates

from DataAccess.DataBase.initDB import Base


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

    @validates("username")
    def validate_username(self, key, value: str) -> str:
        if not value.strip():
            raise ValueError("Username cannot be empty")
        return value

    @validates("money")
    def validate_money(self, key, value: int) -> int:
        if value < 0:
            raise ValueError("Money cannot be negative")
        return value


class QuestRoom(Base):
    __tablename__ = "quest_rooms"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    max_participants: Mapped[int] = mapped_column(Integer, nullable=False)
    min_participants: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    working_hours: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)

    @validates("name")
    def validate_name(self, key, value: str) -> str:
        if not value.strip():
            raise ValueError("Name cannot be empty")
        return value

    @validates("max_participants", "min_participants")
    def validate_participants(self, key, value: int) -> int:
        if value <= 0:
            raise ValueError(f"{key} must be a positive integer")
        if key == "max_participants" and hasattr(self, "min_participants"):
            if value < self.min_participants:
                raise ValueError(
                    "max_participants must be greater than or equal to min_participants"
                )
        if key == "min_participants" and hasattr(self, "max_participants"):
            if value > self.max_participants:
                raise ValueError(
                    "min_participants must be less than or equal to max_participants"
                )
        return value

    @validates("price")
    def validate_price(self, key, value: int) -> int:
        if value <= 0:
            raise ValueError(f"{key} must be a positive integer")
        return value

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
    username: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    discount_percentage: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean, ForeignKey("users.has_certificate"), default=True
    )
