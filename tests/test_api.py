import pytest
from httpx import AsyncClient, ASGITransport

from library.main import app


@pytest.mark.parametrize(
    "query, status_code, res",
    [
        (
                "онегин",
                200,
                [{
                    "title": "онегин",
                    "author": "пушкин",
                    "publish_date": 2006,
                    "total_amount": 10
                }]
        ),
        (
                "о",
                200,
                [
                    {
                        "title": "онегин",
                        "author": "пушкин",
                        "publish_date": 2006,
                        "total_amount": 10
                    },
                    {
                        "title": "пикник на обочине",
                        "author": "братья стругацкие",
                        "publish_date": 2022,
                        "total_amount": 7
                    }
                ]
        ),
        (
                "екореро",
                404,
                {
                    "detail": "Книга не найдена"
                }),
    ]
)
@pytest.mark.asyncio
async def test_get_book_by_title(query, status_code, res):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(f"/books/search/?title={query}")
        assert response.status_code == status_code
        assert response.json() == res


@pytest.mark.parametrize(
    "book_id, status_code, res",
    [
        (
            1,
            200,
            {
                "title": "KOLOBOK",
                "author": "бабушка и дедушка",
                "publish_date": 1996,
                "total_amount": 3,
                "students": []
            }
        ),
        (
            100,
            404,
            {
                "detail": "Книга не найдена"
            }
        ),
        (
            0,
            422,
            {
                "detail":  [
                    {
                        "ctx":
                            {
                                "ge": 1,
                            },
                        "input": "0",
                        "loc": [
                            "path",
                            "book_id",
                            ],
                        "msg": "Input should be greater than or equal to 1",
                        "type": "greater_than_equal",
                    },
                        ]
            }
        ),
    ]
)
@pytest.mark.asyncio
async def test_get_book_by_id(book_id, status_code, res):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(f"/books/{book_id}/")
        assert response.status_code == status_code
        assert response.json() == res

