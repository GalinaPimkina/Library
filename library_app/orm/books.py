from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from models.books import Book


class BookAsyncORM:
    @staticmethod
    async def get_book_from_title(title: str, async_session: AsyncSession):
        async with async_session as session:
            query = (
                select(Book)
                .filter(Book.title.ilike(f"%{title}%"))
            )
            res = await session.execute(query)
            result = res.scalars().all()
            if not result:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")
            return result
