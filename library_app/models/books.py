from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from database.db import Base

if TYPE_CHECKING:
    from .students import Student


class Book(Base):
    __tablename__ = "books"

    title: Mapped[str]
    author: Mapped[str]
    publish_date: Mapped[int]

    total_amount: Mapped[int | None] = mapped_column(default=1, server_default="1") #всего книг в библиотеке
    taken_amount: Mapped[int | None] = mapped_column(default=0, server_default="0") #взятые книги

    students: Mapped[list["Student"]] = relationship(secondary="students_books", back_populates="books", lazy="selectin")

    def __str__(self):
        return str(self.title)

