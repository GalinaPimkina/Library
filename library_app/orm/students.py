from fastapi import HTTPException
from sqlalchemy import select
from starlette import status

from models.students import Student


class StudentAsyncORM:
    @staticmethod
    async def get_all_students(async_session):
        async with async_session as session:
            query = (select(Student).order_by(Student.id))
            result = await session.execute(query)
            students = result.scalars().all()
            if not students:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Студенты не найдены")
            return students
