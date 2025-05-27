from typing import Optional
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


class Book(Base):
    pass


class Student(Base):
    """Студент, читатель.
    Регистрируется через библиотекаря User,
    выбранные книги добавляются в список books"""

    __tablename__ = "student"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] # в чем разница между optional[str] и [str]
    books: Mapped[list["Book"]] = relationship(back_populates="student", default=None)

    def __repr__(self):
        return f"Student(id={self.id}, fullname={self.full_name})"