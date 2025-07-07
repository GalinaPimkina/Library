from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from library.database import Base


student_book_relation_table = Table(
    "student_book_relation_table",
    Base.metadata,
    Column("student_id", ForeignKey("student.id"), primary_key=True),
    Column("book_id", ForeignKey("book.id"), primary_key=True),
)


class Book(Base):
    """Книга.
    title - заголовок,
    total_amount - общее количество книг, принадлежащих библиотеке,
    taken_amount - количество книг, которые взяли студенты,
    student - связь 'многие ко многим' с таблицей Student """

    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    total_amount: Mapped[int] = mapped_column(default=1) # всего книг в системе
    taken_amount: Mapped[int] = mapped_column(default=0)# взятые книги
    student: Mapped[list["Student"]] = relationship(secondary=student_book_relation_table, backref="book")

    def __str__(self):
        return str(self.title)


class Student(Base):
    """Студент, читатель.
    Регистрируется через библиотекаря User,
    full_name - ФИО студента,
    books - список взятых студентом книг"""

    __tablename__ = "student"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] # в чем разница между optional[str] и [str]
    books: Mapped[list["Book"]] = relationship(secondary=student_book_relation_table, back_populates="student")

    def __repr__(self):
        return f"Student(id={self.id}, fullname={self.full_name})"

    def __str__(self):
        return str(self.full_name)


