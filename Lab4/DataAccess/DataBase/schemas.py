from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    password: str
    money: float
    has_certificate: bool
    is_active: bool
    is_admin: bool


class CreateUser(UserBase):
    is_active: bool = True
    is_admin: bool = False
    has_certificate: bool = False


class ReadUser(UserBase):
    id: int
    model_config = {"from_attributes": True}


class QuestRoomBase(BaseModel):
    name: str
    price: float
    min_participants: int
    max_participants: int
    working_hours: str
    description: str | None = None


class CreateQuestRoom(QuestRoomBase):
    pass


class ReadQuestRoom(QuestRoomBase):
    id: int
    model_config = {"from_attributes": True}


class BookingBase(BaseModel):
    quest_room_id: int
    customer_name: str
    participants_amount: int
    booking_date: str


class CreateBooking(BookingBase):
    pass


class ReadBooking(BookingBase):
    id: int
    model_config = {"from_attributes": True}


class Certificate(BaseModel):
    username: str
    user_id: int
    discount_percentage: int
    is_active: bool


class CreateCertificate(Certificate):
    is_active: bool = True


class ReadCertificate(Certificate):
    id: int
    model_config = {"from_attributes": True}
