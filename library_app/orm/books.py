from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from models.books import Book


class BookAsyncORM:
    @staticmethod
    async def get_all_books(async_session: AsyncSession):
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
    async def get_book_by_title(title: str, async_session: AsyncSession):
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
