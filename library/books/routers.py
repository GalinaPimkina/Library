from fastapi import APIRouter
from sqlalchemy import select
from library.database import async_session_maker
from library.books.models import Book

router = APIRouter(prefix='/books', tags=['Книги'])

