from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class StudentBasic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    full_name: Annotated[str | None, Field(max_length=50)] = None
    group_number: Annotated[str | None, Field(max_length=5)] = None


class StudentID(StudentBasic):
    id: int


class StudentSystem(StudentID):
    created_at: datetime
    updated_at: datetime


class StudentListBook(StudentBasic):
    books: list["BookID"] = []


class StudentCreate(StudentBasic):
    pass


class StudentUpdate(StudentBasic):
    pass


from .books import BookID
StudentListBook.model_rebuild()