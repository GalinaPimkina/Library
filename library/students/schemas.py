from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class StudentUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    full_name: Annotated[str | None, Field(max_length=50)] = None
    group_number: Annotated[str | None, Field(max_length=5)] = None


class StudentSystem(StudentUpdate):
    id: int
    created_at: datetime
    updated_at: datetime


class StudentListBook(StudentUpdate):
    books: list["BookPublic"] = []


class StudentPublic(StudentUpdate):
    id: int


class StudentCreate(StudentUpdate):
    pass


from library.books.schemas import BookPublic
StudentListBook.model_rebuild()