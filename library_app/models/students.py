from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship
from database.db import Base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column

if TYPE_CHECKING:
    from .books import Book


class Student(Base):
    __tablename__ = "students"

    full_name: Mapped[str]
    group_number: Mapped[str]
    books: Mapped[list["Book"]] = relationship(secondary="students_books", back_populates="students", lazy="selectin")

    def __repr__(self):
        return f"Student(id={self.id}, fullname={self.full_name})"

    def __str__(self):
        return str(self.full_name)


class StudentBookRelation(Base):
    __tablename__ = "students_books"

    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), primary_key=True)
