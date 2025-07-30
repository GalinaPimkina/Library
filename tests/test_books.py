import pytest
import pytest_asyncio

from fastapi import HTTPException
from httpx import AsyncClient, ASGITransport

from library.main import app


@pytest_asyncio.fixture(scope="function")
async def get_last_book_id():
    '''для теста с удалением книги получает id=5 по списку книги, которая в предыдущем тесте через метод create.
    книги отстортированы по возрастанию id.'''
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(f"/books/")
        data = response.json()
        return data[4]["id"]


class TestBook:
    # тест - поиск книги по названию
    @pytest.mark.parametrize(
        "title, expected_status, res, expected_exception",
        [
            ("онегин",200,[{"title": "онегин","author": "пушкин","publish_date": 2006,"total_amount": 10, "id": 2},],None,),
            ("о",200,[{"title": "онегин","author": "пушкин","publish_date": 2006,"total_amount": 10, "id": 2},{"title": "пикник на обочине","author": "братья стругацкие","publish_date": 2022,"total_amount": 7, "id": 3}],None,),
            ("екореро",404,{"detail": "Книга не найдена"},HTTPException,),
        ]
    )
    @pytest.mark.asyncio
    async def test_get_book_by_title(self, title, expected_status, res, expected_exception):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get(f"/books/search/?title={title}")
            assert response.status_code == expected_status
            assert response.json() == res

    # тест - поиск книги по id
    @pytest.mark.parametrize(
        "book_id, expected_status, res, expected_exception",
        [
            (1, 200, {"title": "KOLOBOK", "author": "бабушка и дедушка", "publish_date": 1996, "total_amount": 3, 'students':[{'full_name': 'семенов семен семенович','group_number': '34вп',},]}, None,),
            (100, 404, {"detail": "Книга не найдена"}, HTTPException,),
            (0, 422, {"detail": [{"ctx": {"ge": 1,}, "input": "0", "loc": ["path", "book_id",], "msg": "Input should be greater than or equal to 1", "type": "greater_than_equal",},]}, HTTPException,),
        ]
    )
    @pytest.mark.asyncio
    async def test_get_book_by_id(self, book_id, expected_status, res, expected_exception):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get(f"/books/{book_id}/")
            assert response.status_code == expected_status
            assert response.json() == res

    # тест - создание новой книги
    @pytest.mark.parametrize(
        "input_json, expected_status, expected_exception",
        [
            ({"title": "abc", "author": "auth", "publish_date": 2022, "total_amount": 10}, 201, None),
            ({"title": "abc", "author": "auth", "publish_date": 2222, "total_amount": 10}, 422, HTTPException),
        ]
    )
    @pytest.mark.asyncio
    async def test_create_book(self, input_json, expected_status, expected_exception):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(f"/books/add/", json=input_json)
            assert response.status_code == expected_status

    # тест - редактирование книги
    @pytest.mark.parametrize(
        "input_json, expected_status, expected_exception",
        [
            ({"title": "ABC", "author": "AUTH", "publish_date": 2022, "total_amount": 7}, 200, None),
            ({"title": "ABC", "author": "AUTH", "publish_date": 2222, "total_amount": 10}, 422, HTTPException),
        ]
    )
    @pytest.mark.asyncio
    async def test_update_item(self, input_json, expected_status, expected_exception):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.put(f"/books/4/edit/", json=input_json)
            assert response.status_code == expected_status

    # тест - удаление книги
    @pytest.mark.asyncio
    async def test_delete_book(self, get_last_book_id):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.delete(f"/books/{get_last_book_id}/delete/")
            assert response.status_code == 200
            response = await client.get(f"/books/{get_last_book_id}/")
            assert response.status_code == 404
