from datetime import datetime

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from models import Book
from books.schemas import (
    BookPublic,
    BookListStudent,
    BookSystem,
    BookUpdate,
    BookCreate
)
from database import get_session

router = APIRouter(prefix='/books', tags=['Книги'])


@router.get(
    "/",
    summary="Получить список всех книг в библиотеке",
    response_model=list[BookPublic],
    status_code=status.HTTP_200_OK
)
async def get_all_books(session: AsyncSession = Depends(get_session)):
    books = await session.execute(select(Book).order_by(Book.title))
    result = books.scalars().all()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книги не найдены")
    return result


@router.get(
    "/{book_id}",
    summary="Книга по id",
    response_model=list[BookListStudent],
    status_code=status.HTTP_200_OK
)
async def get_book_from_id(book_id: int, session: AsyncSession = Depends(get_session)):
    book = await session.execute(select(Book).where(Book.id == book_id))
    result = book.scalars().all()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")
    return result


@router.get(
    "/search/",
    summary="Найти книгу по названию",
    response_model=list[BookPublic],
    status_code=status.HTTP_200_OK
)
async def get_book(query: str, session: AsyncSession = Depends(get_session)):
    books = await session.execute(select(Book).filter(Book.title.ilike(f"%{query}%")))
    result = books.scalars().all()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")
    return result


@router.put(
    "/edit/",
    summary="Редактировать книгу",
    response_model=BookSystem,
    status_code=status.HTTP_200_OK,
)
async def update_book(book_id: int, book_update: BookUpdate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Book).where(Book.id == book_id))
    book = result.scalars().one()
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")

    for field, value in book_update.dict(exclude_unset=True).items():
        setattr(book, field, value)

    book.updated_at = datetime.now()
    await session.commit()
    return book


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


@router.delete(
    "/{book_id}/",
    summary="Удалить книгу",
    status_code=status.HTTP_200_OK
)
async def delete_book(book_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Book).where(Book.id == book_id))
    book = result.scalars().one()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")
    await session.delete(book)
    await session.commit()
    return {"message": "Книга удалена"}
