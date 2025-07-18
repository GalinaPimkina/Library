from datetime import datetime
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException, Query, Path
)
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from library.models import Book
from library.books.schemas import (
    BookPublic,
    BookListStudent,
    BookSystem,
    BookUpdate,
    BookCreate
)
from library.database import get_session

router = APIRouter(prefix='/books', tags=['Книги'])


# -----------------------------get------------------------------

@router.get(
    "/",
    summary="Получить список всех книг в библиотеке",
    response_model=list[BookPublic],
    status_code=status.HTTP_200_OK
)
async def get_all_books(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Book).order_by(Book.title))
    books = result.scalars().all()
    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книги не найдены")
    return books


@router.get(
    "/search/",
    summary="Найти книгу по названию",
    response_model=list[BookPublic],
    status_code=status.HTTP_200_OK
)
async def get_book_by_title(title: Annotated[str, Query()], session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Book).filter(Book.title.ilike(f"%{title}%")))
    books = result.scalars().all()
    if not books:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")
    return books


@router.get(
    "/{book_id}/",
    summary="Детальная информация по книге, ввести id",
    response_model=BookListStudent,
    status_code=status.HTTP_200_OK
)
async def get_book_by_id(book_id: Annotated[int, Path(ge=1)], session: AsyncSession = Depends(get_session)):
    try:
        result = await session.execute(select(Book).where(Book.id == book_id))
        book = result.scalars().one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")
    return book


# -----------------------------put------------------------------

@router.put(
    "/{book_id}/edit/",
    summary="Редактировать информацию о книге",
    response_model=BookSystem,
    status_code=status.HTTP_200_OK,
)
async def update_book(book_id: Annotated[int, Path(ge=1)], book_update: BookUpdate, session: AsyncSession = Depends(get_session)):
    try:
        result = await session.execute(select(Book).where(Book.id == book_id))
        book = result.scalars().one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")

    for field, value in book_update.dict(exclude_unset=True).items():
        setattr(book, field, value)

    book.updated_at = datetime.now()
    await session.commit()
    return book


# -----------------------------post------------------------------

@router.post(
    "/add/",
    summary="Добавить новую книгу",
    response_model=BookSystem,
    status_code=status.HTTP_201_CREATED
)
async def create_book(new_book: BookCreate, session: AsyncSession = Depends(get_session)):
    book = Book(**new_book.dict())
    session.add(book)
    await session.commit()
    return book


# @router.post(
#     "/{book_id}/share/{student_id}/",
#     summary="Выдать книгу",
#     response_model=StudentListBook,
#     status_code=status.HTTP_200_OK,
# )
# async def share_book(
#         book_id: Annotated[int, Path(ge=1)],
#         student_id: Annotated[int, Path(ge=1)],
#         session: AsyncSession = Depends(get_session)
# ):
#     try:
#         result = await session.execute(select(Book).where(Book.id == book_id))
#         book = result.scalars().one()
#     except NoResultFound:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")
#
#
#
# -----------------------------delete------------------------------

@router.delete(
    "/{book_id}/delete/",
    summary="Удалить книгу",
    status_code=status.HTTP_200_OK
)
async def delete_book(book_id: Annotated[int, Path(ge=1)], session: AsyncSession = Depends(get_session)):
    try:
        result = await session.execute(select(Book).where(Book.id == book_id))
        book = result.scalars().one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")

    await session.delete(book)
    await session.commit()
    return {"message": "Книга удалена"}
