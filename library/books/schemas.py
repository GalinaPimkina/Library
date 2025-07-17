from datetime import datetime
from pydantic import BaseModel, ConfigDict


class BookPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str | None = None
    author: str | None = None
    publish_date: int | None = None
    total_amount: int | None = None


class BookSystem(BookPublic):
    id: int
    created_at: datetime
    updated_at: datetime


class BookListStudent(BookPublic):
    taken_amount: int | None = None
    students: list["StudentPublic"] = []


class BookUpdate(BookPublic):
    pass


class BookCreate(BookPublic):
    pass


from students.schemas import StudentPublic
BookListStudent.model_rebuild()