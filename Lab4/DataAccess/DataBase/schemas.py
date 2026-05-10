from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(..., description="Unique username of the user")
    password: str = Field(..., description="User's password (should be stored hashed)")
    money: float = Field(..., description="Account balance in the user's currency")
    has_certificate: bool = Field(
        ..., description="Whether the user has a discount certificate"
    )
    is_active: bool = Field(..., description="Whether the user account is active")
    is_admin: bool = Field(..., description="Whether the user has admin privileges")


class CreateUser(UserBase):
    is_active: bool = True
    is_admin: bool = False
    has_certificate: bool = False


class ReadUser(UserBase):
    id: int
    model_config = {"from_attributes": True}


class QuestRoomBase(BaseModel):
    name: str = Field(..., description="Name of the quest room")
    price: float = Field(..., description="Price for booking the quest room")
    min_participants: int = Field(..., description="Minimum number of participants")
    max_participants: int = Field(..., description="Maximum number of participants")
    working_hours: str = Field(
        ..., description="Working hours or schedule for the room"
    )
    description: str | None = Field(
        None, description="Optional description of the quest room"
    )


class CreateQuestRoom(QuestRoomBase):
    pass


class ReadQuestRoom(QuestRoomBase):
    id: int
    model_config = {"from_attributes": True}


class BookingBase(BaseModel):
    quest_room_id: int
    customer_name: str
    participants_amount: int
    booking_date: str = Field(..., description="Booking date/time in format (HH-DD-MM)")


class CreateBooking(BaseModel):
    quest_room_id: int
    participants_amount: int
    booking_date: str = Field(..., description="Booking date/time in format (HH-DD-MM)")


class ReadBooking(BookingBase):
    id: int
    model_config = {"from_attributes": True}


class Certificate(BaseModel):
    username: str = Field(..., description="Username the certificate is issued to")
    user_id: int = Field(..., description="ID of the user who owns the certificate")
    discount_percentage: int = Field(
        ..., description="Discount percentage provided by the certificate"
    )
    is_active: bool = Field(..., description="Whether the certificate is active")


class CreateCertificate(Certificate):
    is_active: bool = True


class ReadCertificate(Certificate):
    id: int
    model_config = {"from_attributes": True}
