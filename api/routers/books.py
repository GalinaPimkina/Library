from fastapi import APIRouter

router = APIRouter()

fake_library_db = [
    {
        "id": 1,
        "author": "Н.В. Гоголь",
        "title": "Мертвые души",
        "amount": 4,
    },
    {
        "id": 2,
        "author": "Ф.М. Достоевский",
        "title": "Преступление и наказание",
        "amount": 7,
    },
    {
        "id": 3,
        "author": "А.С. Пушкин",
        "title": "Евгений Онегин",
        "amount": 6,
    },
    {
        "id": 4,
        "author": "М.Ю. Лермонтов",
        "title": "Герой нашего времени",
        "amount": 5,
    },
    {
        "id": 5,
        "author": "И.С. Тургенев",
        "title": "Отцы и дети",
        "amount": 2,
    },
]


@router.get("/books/")
async def read_books() -> list:
    return fake_library_db
