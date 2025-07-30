import pytest
from fastapi import HTTPException
from httpx import AsyncClient, ASGITransport

from library.main import app


class TestStudent:
    # тест поиск студента по фио или номеру группы
    @pytest.mark.parametrize(
        "query, expected_status, res, expected_exception",
        [
            ("12АРА",200,[{"full_name": "петров петр петрович","group_number": "12АРА"}],None,),
            ("е",200,[{"full_name": "петров петр петрович","group_number": "12АРА"},{"full_name": "семенов семен семенович","group_number": "34вп"}],None,),
            ("увкпув",404,{"detail": "Студент не найден"}, HTTPException,),
        ]
    )
    @pytest.mark.asyncio
    async def test_get_student_by_name_or_group(self, query, expected_status, res, expected_exception):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get(f"/students/search/?query={query}")
            assert response.status_code == expected_status
            assert response.json() == res

    # тест - поиск студента по id
    @pytest.mark.parametrize(
        "student_id, expected_status, res, expected_exception",
        [
            (1, 200, {"full_name": "петров петр петрович","group_number": "12АРА","books": [{"title": "онегин","author": "пушкин","publish_date": 2006,"total_amount": 10,"id": 2},{"title": "пикник на обочине","author": "братья стругацкие","publish_date": 2022,"total_amount": 7,"id": 3}]}, None,),
            (100, 404, {"detail": "Студент не найден"}, HTTPException,),
            (0, 422, {"detail": [{"ctx": {"ge": 1, }, "input": "0", "loc": ["path", "student_id", ],
                                  "msg": "Input should be greater than or equal to 1",
                                  "type": "greater_than_equal", }, ]}, HTTPException,),
        ]
    )
    @pytest.mark.asyncio
    async def test_get_student_by_id(self, student_id, expected_status, res, expected_exception):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get(f"/students/{student_id}/")
            assert response.status_code == expected_status
            assert response.json() == res

    # тест - создание нового студента
    @pytest.mark.parametrize(
        "input_json, expected_status, expected_exception",
        [
            ({"full_name": "student student", "group_number": "45st"}, 201, None),
            ({"full_name": "student student", "group_number": "45ststst"}, 422, HTTPException),
        ]
    )
    @pytest.mark.asyncio
    async def test_create_student(self, input_json, expected_status, expected_exception):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(f"/students/add/", json=input_json)
            assert response.status_code == expected_status