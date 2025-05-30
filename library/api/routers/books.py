from fastapi import APIRouter, HTTPException

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


@router.get("/")
async def read_books() -> list:
    return fake_library_db


@router.get("/{book_id}/")
async def get_book(book_id: int):
    books_id_lst = [v for item in fake_library_db for k, v in item.items() if k == "id"]

    if book_id not in books_id_lst:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    else:
        for book in fake_library_db:
            if book["id"] == book_id:
                return {"book": book}
