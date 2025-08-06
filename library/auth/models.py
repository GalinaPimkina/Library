from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyBaseAccessTokenTable, SQLAlchemyAccessTokenDatabase


from library.database import Base, get_session


class User(Base, SQLAlchemyBaseUserTable[int]):
    username: Mapped[str]

    @classmethod
    def get_db(cls, session: AsyncSession = Depends(get_session)):
        return SQLAlchemyUserDatabase(session, User)


class AccessToken(Base, SQLAlchemyBaseAccessTokenTable[int]):
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="cascade"),
        nullable=False,
    )

    @classmethod
    def get_db(cls, session: AsyncSession = Depends(get_session)):
        return SQLAlchemyAccessTokenDatabase(session, cls)