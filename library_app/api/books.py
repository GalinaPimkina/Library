from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Query,
    Path,
)
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from orm.books import BookAsyncORM
from schemas.books import (
    BookID,
    BookListStudent,
    BookSystem,
    BookUpdate,
    BookCreate,
)
from database.db import get_session

router = APIRouter(prefix='/books', tags=['Книги'])


# -----------------------------get------------------------------

@router.get(
    "/",
    summary="Получить список всех книг в библиотеке",
    response_model=list[BookID],
    status_code=status.HTTP_200_OK
)
async def get_all_books(
        session: AsyncSession = Depends(get_session)
):
    books = await BookAsyncORM.get_all_books(session)
    return books


@router.get(
    "/search/",
    summary="Найти книгу по названию",
    response_model=list[BookID],
    status_code=status.HTTP_200_OK
)
async def get_book_by_title(
        title: Annotated[str, Query()],
        session: AsyncSession = Depends(get_session)
):
    books = await BookAsyncORM.get_book_by_title(title, session)
    return books


@router.get(
    "/{book_id}/",
    summary="Детальная информация по книге, ввести id",
    response_model=BookListStudent,
    status_code=status.HTTP_200_OK
)
async def get_book_by_id(
        book_id: Annotated[int, Path(ge=1)],
        session: AsyncSession = Depends(get_session)
):
    book = await BookAsyncORM.get_book_by_id(book_id, session)
    return book


# -----------------------------put------------------------------

@router.put(
    "/{book_id}/edit/",
    summary="Редактировать информацию о книге",
    response_model=BookSystem,
    status_code=status.HTTP_200_OK,
)
async def update_book(
        book_id: Annotated[int, Path(ge=1)],
        book_update: BookUpdate,
        session: AsyncSession = Depends(get_session)
):
    book = await BookAsyncORM.update_book(book_id, book_update, session)
    return book


# -----------------------------post------------------------------

@router.post(
    "/add/",
    summary="Добавить новую книгу",
    response_model=BookSystem,
    status_code=status.HTTP_201_CREATED
)
async def create_book(new_book: BookCreate, session: AsyncSession = Depends(get_session)):
    book = await BookAsyncORM.create_book(new_book, session)
    return book


# -----------------------------delete------------------------------

@router.delete(
    "/{book_id}/delete/",
    summary="Удалить книгу",
    status_code=status.HTTP_200_OK
)
async def delete_book(book_id: Annotated[int, Path(ge=1)], session: AsyncSession = Depends(get_session)):
    await BookAsyncORM.delete_book(book_id, session)
    return {"message": "Книга удалена"}
