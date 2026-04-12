from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    money: int
    password: str
    is_admin: bool
    is_active: bool
    has_certificate: bool


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
    user_id: int
    is_active: bool
