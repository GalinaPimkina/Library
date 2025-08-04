from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from library.database import Base
from library.database import get_session


class User(Base, SQLAlchemyBaseUserTable[int]):
    username: Mapped[str]

    @classmethod
    def get_db(cls, session: AsyncSession = Depends(get_session)):
        return SQLAlchemyUserDatabase(session, User)