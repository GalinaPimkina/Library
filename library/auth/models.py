from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped

from library.database import Base


class User(Base, SQLAlchemyBaseUserTable[int]):
    username: Mapped[str]