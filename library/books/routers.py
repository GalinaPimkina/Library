from fastapi import APIRouter
from library.books.crud import ReadBook

router = APIRouter(prefix='/books', tags=['Книги'])


@router.get("/", summary="Получить список всех книг в библиотеке")
async def get_all_books():
    return await ReadBook.read_all_books()