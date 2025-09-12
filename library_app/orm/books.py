from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from models.books import Book


class BookAsyncORM:
    @staticmethod
    async def get_all_books(async_session):
        async with async_session as session:
            query = (
                select(Book)
                .order_by(Book.id)
            )
            result = await session.execute(query)
            books = result.scalars().all()
            if not books:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книги не найдены")
            return books
    
    @staticmethod
    async def get_book_by_title(title, async_session):
        async with async_session as session:
            query = (
                select(Book)
                .filter(Book.title.ilike(f"%{title}%"))
            )
            result = await session.execute(query)
            books = result.scalars().all()
            if not books:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")
            return books

    @staticmethod
    async def get_book_by_id(book_id, async_session):
        async with async_session as session:
            query = select(Book).where(Book.id == book_id)
            try:
                result = await session.execute(query)
                book = result.scalars().one()
            except NoResultFound:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")
            return book

    @staticmethod
    async def update_book(book_id, book_update, async_session):
        async with async_session as session:
            query = select(Book).where(Book.id == book_id)
            try:
                result = await session.execute(query)
                book = result.scalars().one()
            except NoResultFound:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")

            for field, value in book_update.model_dump(exclude_unset=True).items():
                setattr(book, field, value)

            book.updated_at = datetime.now()
            await session.commit()
            return book

    @staticmethod
    async def create_book(new_book, async_session):
        async with async_session as session:
            book = Book(**new_book.model_dump())
            session.add(book)
            await session.commit()
            return book