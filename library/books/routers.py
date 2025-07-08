from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from books.models import Book
from books.schemas import BookPublic
from database import get_session

router = APIRouter(prefix='/books', tags=['Книги'])


@router.get("/", summary="Получить список всех книг в библиотеке", response_model=list[BookPublic])
async def get_all_books(session: AsyncSession = Depends(get_session)):
    books = await session.execute(select(Book).order_by(Book.title))
    return books.scalars().all()


@router.get("/{book_id}/", summary="Получить книгу по id", response_model=BookPublic)
async def get_book_from_id(book_id: int, session: AsyncSession = Depends(get_session)):
    book = await session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return book


