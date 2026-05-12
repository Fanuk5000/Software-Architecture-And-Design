from sqlalchemy import (
    Boolean,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

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


class QuestRoom(Base):
    __tablename__ = "quest_rooms"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    max_participants: Mapped[int] = mapped_column(Integer, nullable=False)
    min_participants: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    working_hours: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    quest_room_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("quest_rooms.id"), nullable=False
    )
    customer_name: Mapped[str] = mapped_column(String, nullable=False)
    participants_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    booking_date: Mapped[String] = mapped_column(String, nullable=False)


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
