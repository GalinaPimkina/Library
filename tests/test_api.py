import pytest
from httpx import AsyncClient, ASGITransport

from library.main import app


@pytest.mark.asyncio
async def test_get_book_by_title():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/books/search/?title=онегин")
        assert response.status_code == 200
        assert response.json() == [{
            "title": "онегин",
            "author": "пушкин",
            "publish_date": 2006,
            "total_amount": 10
        }]

