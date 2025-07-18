from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, field_validator, Field


class BookPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str | None = None
    author: str | None = None
    publish_date: int | None = None
    total_amount: int | None = None

    @field_validator("publish_date")
    def validate_publish_date(cls, value):
        current_year = datetime.now().year
        if not (1000 <= value <= current_year):
            raise ValueError(f"Год издания должен быть в пределах от 1000 до {current_year}.")
        return value


class BookSystem(BookPublic):
    id: int
    created_at: datetime
    updated_at: datetime


class BookListStudent(BookPublic):
    # taken_amount: Annotated[int | None, Field(ge=0, le=10)] = None
    students: list["StudentPublic"] = []


class BookUpdate(BookPublic):
    pass


class BookCreate(BookPublic):
    pass


from library.students.schemas import StudentPublic
BookListStudent.model_rebuild()