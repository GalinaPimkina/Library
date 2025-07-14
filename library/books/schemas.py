from datetime import datetime

from pydantic import BaseModel, ConfigDict

from students.schemas import StudentPublic


class BookPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    author: str
    publish_date: int
    total_amount: int


class BookSystem(BookPublic):
    id: int
    created_at: datetime
    updated_at: datetime


class BookListStudent(BookPublic):
    taken_amount: int
    students: list["StudentPublic"] = []


class BookUpdate(BookPublic):
    pass

