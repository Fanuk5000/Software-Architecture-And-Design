from DataAccess.DataBase.initDB import Base
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    money = Column(Integer, default=0)
    password_hash = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    has_certificate = Column(Boolean, default=False)


class QuestRoom(Base):
    __tablename__ = "quest_rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    price = Column(Integer, nullable=False)
    max_participants = Column(Integer, nullable=False)
    min_participants = Column(Integer, nullable=False)
    description = Column(String, nullable=True)


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    quest_room_id = Column(Integer, ForeignKey("quest_rooms.id"), nullable=False)
    customer_name = Column(String, nullable=False)
    participants_amount = Column(Integer, nullable=False)
    booking_date = Column(Date, nullable=False)


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    discount_percentage = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_active = Column(Boolean, default=True)
