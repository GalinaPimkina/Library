from typing import Optional
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    """Библиотекарь. Наделен правами администратора.
    Может регистрировать новых читателей в системе,
    вести контроль за взятыми книги."""

    __tablename__ = "user_librarian"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    full_name = Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r})"


student_book_relation_table = Table(
    "student_book_relation_table",
    Base.metadata,
    Column("student_id", ForeignKey("student.id"), primary_key=True),
    Column("book_id", ForeignKey("book.id"), primary_key=True),
)


class Student(Base):
    """Студент, читатель.
    Регистрируется через библиотекаря User,
    выбранные книги добавляются в список books"""

    __tablename__ = "student"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] # в чем разница между optional[str] и [str]
    books: Mapped[list["Book"]] = relationship(secondary=student_book_relation_table, back_populates="student")

    def __repr__(self):
        return f"Student(id={self.id}, fullname={self.full_name})"


class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    total_amount: Mapped[int] = mapped_column(default=1) # всего книг в системе
    taken_amount: Mapped[int] = mapped_column(default=0)# взятые книги
    student: Mapped[list["Student"]] = relationship(secondary=student_book_relation_table, back_populates="book")