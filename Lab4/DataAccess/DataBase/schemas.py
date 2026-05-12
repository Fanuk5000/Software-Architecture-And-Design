import re

from pydantic import BaseModel, Field, field_validator, model_validator


class UserBase(BaseModel):
    username: str = Field(..., description="Unique username of the user")
    password: str = Field(..., description="User's password (should be stored hashed)")
    money: float = Field(..., description="Account balance in the user's currency")
    has_certificate: bool = Field(
        ..., description="Whether the user has a discount certificate"
    )
    is_active: bool = Field(..., description="Whether the user account is active")
    is_admin: bool = Field(..., description="Whether the user has admin privileges")

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Username cannot be empty")
        return value

    @field_validator("money")
    @classmethod
    def validate_money(cls, value: float) -> float:
        if value < 0:
            raise ValueError("Money cannot be negative")
        return value


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

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Name cannot be empty")
        return value

    @field_validator("min_participants", "max_participants")
    @classmethod
    def validate_participants(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("participants must be a positive integer")
        return value

    @model_validator(mode="after")
    def validate_participants_range(self) -> "QuestRoomBase":
        if self.min_participants > self.max_participants:
            raise ValueError(
                "min_participants must be less than or equal to max_participants"
            )
        return self

    @field_validator("price")
    @classmethod
    def validate_price(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("price must be a positive number")
        return value

    @field_validator("working_hours")
    @classmethod
    def validate_working_hours(cls, value: str) -> str:
        match = re.match(r"^(\d{1,2})-(\d{1,2})$", value)
        if not match:
            raise ValueError("working_hours must match 'num-num' (e.g. '10-22')")
        start, end = int(match.group(1)), int(match.group(2))
        if not (0 <= start < 24 and 0 <= end < 24):
            raise ValueError("Hours must be between 0 and 23")
        if start >= end:
            raise ValueError("Start hour must be less than end hour")
        return value


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

    @field_validator("discount_percentage")
    @classmethod
    def validate_discount_percentage(cls, value: int) -> int:
        if not (0 < value <= 100):
            raise ValueError("discount_percentage must be between 0 and 100")
        return value


class CreateCertificate(Certificate):
    is_active: bool = True


class ReadCertificate(Certificate):
    id: int
    model_config = {"from_attributes": True}
