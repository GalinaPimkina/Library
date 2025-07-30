import pytest
from fastapi import HTTPException
from httpx import AsyncClient, ASGITransport

from library.main import app


class TestStudent:
    @pytest.mark.parametrize(
        "query, status_code, res, expected_exception",
        [
            ("12АРА",200,[{"full_name": "петров петр петрович","group_number": "12АРА"}],None,),
            ("е",200,[{"full_name": "петров петр петрович","group_number": "12АРА"},{"full_name": "семенов семен семенович","group_number": "34вп"}],None,),
            ("увкпув",404,{"detail": "Студент не найден"}, HTTPException,),
        ]
    )
    @pytest.mark.asyncio
    async def test_get_student_by_name_or_group(self, query, status_code, res, expected_exception):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get(f"/students/search/?query={query}")
            assert response.status_code == status_code
            assert response.json() == res