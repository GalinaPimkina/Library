
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, or_
from sqlalchemy.exc import NoResultFound
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
    "/search/",
    summary="Найти студента по ФИО или номеру группы",
    response_model=list[StudentPublic],
    status_code=status.HTTP_200_OK
)
async def get_student(query: Annotated[str, Query()], session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Student).filter(or_(Student.full_name.ilike(f"%{query}%"), (Student.group_number.ilike(f"%{query}%")))))
    students = result.scalars().all()
    if not students:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Студент не найден")
    return students


@router.get(
    "/{student_id}/",
    summary="Детальная информация по студенту, ввести id",
    response_model=StudentListBook,
    status_code=status.HTTP_200_OK
)
async def get_student_from_id(student_id: int, session: AsyncSession = Depends(get_session)):
    try:
        result = await session.execute(select(Student).where(Student.id == student_id))
        student = result.scalars().one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Студент не найден")
    return student