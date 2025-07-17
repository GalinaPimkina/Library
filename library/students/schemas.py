from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class StudentPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    full_name: Annotated[str | None, Field(max_length=50)] = None
    group_number: Annotated[str | None, Field(max_length=5)] = None


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