from pydantic import BaseModel


class QuestRoom(BaseModel):
    id: int
    name: str
    max_participants: int
    min_participants: int
    description: str | None = None


class Booking(BaseModel):
    id: int
    quest_room_id: int
    customer_name: str
    booking_date: str


class Certificate(BaseModel):
    id: int
    code: str
    discount_percentage: int
    is_active: bool
