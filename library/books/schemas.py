from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class BookBasic(BaseModel):
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


class BookID(BookBasic):
    id: int


class BookSystem(BookID):
    created_at: datetime
    updated_at: datetime


class BookListStudent(BookBasic):
    # taken_amount: Annotated[int | None, Field(ge=0, le=10)] = None
    students: list["StudentID"] = []


class BookCreate(BookBasic):
    pass


class BookUpdate(BookBasic):
    pass


from library.students.schemas import StudentID
BookListStudent.model_rebuild()