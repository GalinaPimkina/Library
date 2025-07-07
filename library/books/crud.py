from sqlalchemy import select
from library.books.models import Book
from library.database import async_session_maker


class ReadBook:
    @classmethod
    async def read_all_books(cls):
        async with async_session_maker() as session:
            query = select(Book)
            books = await session.execute(query)
            return books.scalars().all()