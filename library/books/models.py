from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from library.database import Base


class Book(Base):
    __tablename__ = "books"

    title: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    publish_date: Mapped[int] = mapped_column(nullable=False)

    total_amount: Mapped[int] = mapped_column(default=1) #всего книг в библиотеке
    taken_amount: Mapped[int] = mapped_column(default=0, nullable=True) #взятые книги

    students: Mapped[list["Student"]] = relationship(secondary="students_books", back_populates="books")

    def __str__(self):
        return str(self.title)


class Student(Base):
    __tablename__ = "students"

    full_name: Mapped[str] = mapped_column(nullable=False)
    group_number: Mapped[str] = mapped_column(nullable=False)
    books: Mapped[list["Book"]] = relationship(secondary="students_books", back_populates="students")

    def __repr__(self):
        return f"Student(id={self.id}, fullname={self.full_name})"

    def __str__(self):
        return str(self.full_name)


class StudentBookRelation(Base):
    __tablename__ = "students_books"

    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), primary_key=True)

