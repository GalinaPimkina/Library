import asyncio
import contextlib

from database.config import settings
from database.db import get_session
from models.users import get_user_db
from schemas.users import UserCreate
from fastapi_users.exceptions import UserAlreadyExists

from auth.user_manager import get_user_manager

get_async_session_context = contextlib.asynccontextmanager(get_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)

superuser_email = settings.superuser_email
superuser_password = settings.superuser_password


async def create_superuser(
        email: str, password: str, is_superuser: bool = True
):
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    superuser = await user_manager.create(
                        UserCreate(
                            username="admin", email=email, password=password, is_superuser=is_superuser
                        )
                    )
                    print(f"Superuser created {superuser}")
                    return superuser
    except UserAlreadyExists:
        raise


if __name__ == "__main__":
    asyncio.run(create_superuser(email=superuser_email, password=superuser_password))