from dataclasses import dataclass
from datetime import datetime


@dataclass
class CustomerRequest:
    user_id: int
    room_id: int
    customer_name: str
    person_amount: int
    book_date: datetime
    money_given: int
