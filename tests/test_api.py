import pytest
from fastapi import HTTPException
from httpx import AsyncClient, ASGITransport

from library.main import app


class TestBook:
    @pytest.mark.parametrize(
        "query, status_code, res, expected_exception",
        [
            ("онегин",200,[{"title": "онегин","author": "пушкин","publish_date": 2006,"total_amount": 10},],None,),
            # ("о",200,[{"title": "онегин","author": "пушкин","publish_date": 2006,"total_amount": 10},{"title": "пикник на обочине","author": "братья стругацкие","publish_date": 2022,"total_amount": 7}],None,),
            ("екореро",404,{"detail": "Книга не найдена"},HTTPException,),
        ]
    )
    @pytest.mark.asyncio
    async def test_get_book_by_title(self, query, status_code, res, expected_exception):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get(f"/books/search/?title={query}")
            assert response.status_code == status_code
            assert response.json() == res

    @pytest.mark.parametrize(
        "book_id, status_code, res, expected_exception",
        [
            (1, 200, {"title": "KOLOBOK", "author": "бабушка и дедушка", "publish_date": 1996, "total_amount": 3, "students": []}, None,),
            (100, 404, {"detail": "Книга не найдена"}, HTTPException,),
            (0, 422, {"detail": [{"ctx": {"ge": 1,}, "input": "0", "loc": ["path", "book_id",], "msg": "Input should be greater than or equal to 1", "type": "greater_than_equal",},]}, HTTPException,),
        ]
    )
    @pytest.mark.asyncio
    async def test_get_book_by_id(self, book_id, status_code, res, expected_exception):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get(f"/books/{book_id}/")
            assert response.status_code == status_code
            assert response.json() == res

    @pytest.mark.parametrize(
        "input_json, status_code, expected_exception",
        [
            ({"title": "abc", "author": "auth", "publish_date": 2022, "total_amount": 10}, 201, None),
            ({"title": "abc", "author": "auth", "publish_date": 2222, "total_amount": 10}, 422, HTTPException),
        ]
    )
    @pytest.mark.asyncio
    async def test_create_book(self, input_json, status_code, expected_exception):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(f"/books/add/", json=input_json)
            assert response.status_code == status_code


# def test_update_item(item_id):
#     response = client.put(f"/items/{item_id}", json={"name": "Updated Item", "description": "Updated description"})
#     assert response.status_code == 200
#     data = response.json()
#     assert data["name"] == "Updated Item"
#
# def test_delete_item(item_id):
#     response = client.delete(f"/items/{item_id}")
#     assert response.status_code == 200
#     response = client.get(f"/items/{item_id}")
#     assert response.status_code == 404