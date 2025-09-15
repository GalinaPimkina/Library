from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from starlette import status

from models.students import Student
from utils.create_student_username import get_random_username


class StudentAsyncORM:
    @staticmethod
    async def get_all_students(async_session):
        async with async_session as session:
            query = select(Student).order_by(Student.id)
            result = await session.execute(query)
            students = result.scalars().all()
            if not students:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Студенты не найдены")
            return students

    @staticmethod
    async def get_student_by_username(username, async_session):
        async with async_session as session:
            query = select(Student).filter(Student.username.ilike(f"%{username}%"))
            result = await session.execute(query)
            students = result.scalars().all()
            if not students:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Студент не найден")
            return students

    @staticmethod
    async def get_student_from_id(student_id, async_session):
        async with async_session as session:
            query = select(Student).where(Student.id == student_id)
            try:
                result = await session.execute(query)
                student = result.scalars().one()
            except NoResultFound:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Студент не найден")
            return student

    @staticmethod
    async def update_student(student_id, update, async_session):
        async with async_session as session:

            query = select(Student).where(Student.id == student_id)
            try:
                result = await session.execute(query)
                student = result.scalars().one()
            except NoResultFound:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Студент не найден")

            for field, value in update.model_dump(exclude_unset=True).items():
                setattr(student, field, value)

            student.updated_at = datetime.now()
            await session.commit()
            return student

    @staticmethod
    async def create_student(new_student, async_session):
        async with async_session as session:
            student = Student(**new_student.model_dump())
            student.username = get_random_username()
            session.add(student)
            await session.commit()
            return student

    @staticmethod
    async def delete_student(student_id, async_session):
        async with async_session as session:
            query = select(Student).where(Student.id == student_id)
            try:
                result = await session.execute(query)
                student = result.scalars().one()
            except NoResultFound:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Студент не найден")

            await session.delete(student)
            await session.commit()



    # @staticmethod
    # async def add_vacancies_and_replies():
    #     async with async_session_factory() as session:
    #         new_vacancy = VacanciesOrm(title="Python разработчик", compensation=100000)
    #         get_resume_1 = select(ResumesOrm).options(selectinload(ResumesOrm.vacancies_replied)).filter_by(id=1)
    #         get_resume_2 = select(ResumesOrm).options(selectinload(ResumesOrm.vacancies_replied)).filter_by(id=2)
    #         resume_1 = (await session.execute(get_resume_1)).scalar_one()
    #         resume_2 = (await session.execute(get_resume_2)).scalar_one()
    #         resume_1.vacancies_replied.append(new_vacancy)
    #         resume_2.vacancies_replied.append(new_vacancy)
    #         await session.commit()