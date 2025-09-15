from datetime import datetime
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Path,
)
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database.db import get_session
from models.students import Student
from orm.students import StudentAsyncORM
from schemas.students import (
    StudentID,
    StudentListBook,
    StudentSystem,
    StudentUpdate,
    StudentCreate,
    StudentUsername,
)
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
    students = await StudentAsyncORM.get_all_students(session)
    return students


@router.get(
    "/search/",
    summary="Найти студента по username",
    response_model=list[StudentUsername],
    status_code=status.HTTP_200_OK
)
async def get_student_by_username(username: Annotated[str, Query()], session: AsyncSession = Depends(get_session)):
    students = await StudentAsyncORM.get_student_by_username(username, session)
    return students


@router.get(
    "/{student_id}/",
    summary="Детальная информация по студенту, ввести id",
    response_model=StudentListBook,
    status_code=status.HTTP_200_OK
)
async def get_student_from_id(student_id: Annotated[int, Path(ge=1)], session: AsyncSession = Depends(get_session)):
    student = await StudentAsyncORM.get_student_from_id(student_id, session)
    return student


# ---------------------------put-----------------------------------

@router.put(
    "/{student_id}/edit/",
    summary="Редактировать информацию о студенте",
    response_model=StudentSystem,
    status_code=status.HTTP_200_OK,
)
async def update_student(student_id: Annotated[int, Path(ge=1)], update: StudentUpdate, session: AsyncSession = Depends(get_session)):
    student = await StudentAsyncORM.update_student(student_id, update, session)
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