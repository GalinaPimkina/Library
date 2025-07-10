from datetime import datetime

from pydantic import BaseModel, ConfigDict

from models import Student


class BookSystem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class BookPublic(BookSystem):
    title: str
    author: str
    publish_date: int
    total_amount: int
    taken_amount: int


class BookStudent(BookSystem):
    title: str
    taken_amount: int
    # students: list["Student"]

