from DataAccess.DB.database import Base
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
)


class QuestRoom(Base):
    __tablename__ = "quest_rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    max_participants = Column(Integer, nullable=False)
    min_participants = Column(Integer, nullable=False)
    description = Column(String, nullable=True)


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    quest_room_id = Column(Integer, ForeignKey("quest_rooms.id"), nullable=False)
    customer_name = Column(String, nullable=False)
    booking_date = Column(Date, nullable=False)


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    discount_percentage = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
