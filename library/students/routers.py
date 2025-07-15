from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import get_session
from models import Student
from students.schemas import StudentPublic, StudentListBook


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


@router.get(
    "/{student_id}/",
    summary="Найти студента по id",
    response_model=StudentListBook,
    status_code=status.HTTP_200_OK
)
async def get_student_from_id(student_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Student).where(Student.id == student_id))
    student = result.scalars().one()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Студент не найден")
    return student