from typing import Optional
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


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


class Student(Base):
    pass


class Book(Base):
    pass