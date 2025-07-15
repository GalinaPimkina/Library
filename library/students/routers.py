from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import get_session
from models import Student
from students.schemas import StudentPublic

router = APIRouter(prefix="/students", tags=["Студенты"])


@router.get(
    "/",
    summary="Получить список всех студентов",
    response_model=list[StudentPublic],
    status_code=status.HTTP_200_OK
)
async def get_all_students(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Student).order_by(Student.full_name))
    students = result.scalars().all()
    if not students:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Студенты не найдены")
    return students