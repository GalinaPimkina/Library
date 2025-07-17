from datetime import datetime
from pydantic import BaseModel, ConfigDict


class StudentPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    full_name: str | None = None
    group_number: str | None = None


class StudentSystem(StudentPublic):
    id: int
    created_at: datetime
    updated_at: datetime


class StudentListBook(StudentPublic):
    books: list["BookPublic"] = []


class StudentUpdate(StudentPublic):
    pass


class StudentCreate(StudentPublic):
    pass


from books.schemas import BookPublic
StudentListBook.model_rebuild()