import pytest
import pytest_asyncio
from fastapi import HTTPException
from httpx import AsyncClient, ASGITransport

from library.main import app


@pytest_asyncio.fixture(scope="function")
async def get_student_delete_id():
    '''для теста с удалением студента получает id 4-ого в списке студента(id может быть != 5), который добавляется в предыдущем тесте через метод create.
    студента отстортированы по возрастанию id.'''
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(f"/students/")
        data = response.json()
        return data[3]["id"]


class TestStudent:
    # тест поиск студента по фио или номеру группы
    @pytest.mark.parametrize(
        "query, expected_status, res, expected_exception",
        [
            ("student_1",200,[{"full_name": "test_student_1","group_number": "t_g_1"}],None,),
            ("student",200,[{"full_name": "test_student_1","group_number": "t_g_1"},{"full_name": "test_student_2","group_number": "t_g_2"}],None,),
            ("studentstudent",404,{"detail": "Студент не найден"}, HTTPException,),
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
            (1, 200, {"full_name": "test_student_1","group_number": "t_g_1","books": [{"title": "test_book_2","author": "test_author_2","publish_date": 2006,"total_amount": 10,"id": 2},{"title": "test_book_3","author": "test_author_3","publish_date": 2022,"total_amount": 7,"id": 3}]}, None),
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
            ({"full_name": "test_student_3", "group_number": "t_g_3"}, 201, None),
            ({"full_name": "test_student_4", "group_number": "test_group_4"}, 422, HTTPException),
        ]
    )
    @pytest.mark.asyncio
    async def test_create_student(self, input_json, expected_status, expected_exception):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.post(f"/students/add/", json=input_json)
            assert response.status_code == expected_status