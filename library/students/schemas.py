from books.schemas import *  #datetime, BaseModel, ConfigDict циклический импорт


class StudentPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    full_name: str
    group_number: str


class StudentSystem(StudentPublic):
    id: int
    created_at: datetime
    updated_at: datetime


class StudentListBook(StudentPublic):
    books: list["BookPublic"] = []


class StudentUpdate(StudentPublic):
    pass