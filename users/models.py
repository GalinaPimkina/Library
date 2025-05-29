from typing import Optional
from library.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    """Библиотекарь. Наделен правами администратора.
    Может регистрировать новых читателей в системе,
    вести контроль за взятыми книги."""

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    full_name = Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r})"

    def __str__(self):
        return str(self.full_name)
