from datetime import datetime
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Path,
)
from sqlalchemy import select, or_
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database.db import get_session
from models.students import Student
from schemas.students import (
    StudentID,
    StudentListBook,
    StudentSystem,
    StudentUpdate,
    StudentCreate,)
from utils.create_student_username import get_random_username

router = APIRouter(prefix="/students", tags=["Студенты"])


# ---------------------------get-----------------------------------

@router.get(
    "/",
    summary="Получить список всех студентов",
    response_model=list[StudentID],
    status_code=status.HTTP_200_OK
)
async def get_all_students(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Student).order_by(Student.id))
    students = result.scalars().all()
    if not students:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Студенты не найдены")
    return students


@router.get(
    "/search/",
    summary="Найти студента по ФИО или номеру группы",
    response_model=list[StudentID],
    status_code=status.HTTP_200_OK
)
async def get_student_by_name_or_group(query: Annotated[str, Query()], session: AsyncSession = Depends(get_session)):
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
async def get_student_from_id(student_id: Annotated[int, Path(ge=1)], session: AsyncSession = Depends(get_session)):
    try:
        result = await session.execute(select(Student).where(Student.id == student_id))
        student = result.scalars().one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Студент не найден")
    return student


# ---------------------------put-----------------------------------

@router.put(
    "/{student_id}/edit/",
    summary="Редактировать информацию о студенте",
    response_model=StudentSystem,
    status_code=status.HTTP_200_OK,
)
async def update_student(student_id: Annotated[int, Path(ge=1)], student_update: StudentUpdate, session: AsyncSession = Depends(get_session)):
    try:
        result = await session.execute(select(Student).where(Student.id == student_id))
        student = result.scalars().one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Студент не найден")

    for field, value in student_update.model_dump(exclude_unset=True).items():
        setattr(student, field, value)

    student.updated_at = datetime.now()
    await session.commit()
    return student


# ---------------------------post-----------------------------------

@router.post(
    "/add/",
    summary="Добавить нового студента",
    response_model=StudentSystem,
    status_code=status.HTTP_201_CREATED,
)
async def create_student(new_student: StudentCreate, session: AsyncSession = Depends(get_session)):
    student = Student(**new_student.model_dump())
    student.username = get_random_username()
    session.add(student)
    await session.commit()
    return student


# ---------------------------delete-----------------------------------

@router.delete(
    "/{student_id}/delete/",
    summary="Удалить студента",
    status_code=status.HTTP_200_OK,
)
async def delete_student(student_id: Annotated[int, Path(ge=1)], session: AsyncSession = Depends(get_session)):
    try:
        result = await session.execute(select(Student).where(Student.id == student_id))
        student = result.scalars().one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Студент не найден")

    await session.delete(student)
    await session.commit()
    return {"message": "Студент удален"}