from typing import TYPE_CHECKING, Annotated

from fastapi import Depends
from fastapi_users.authentication.strategy.db import AccessTokenDatabase, DatabaseStrategy

if TYPE_CHECKING:
    from library.models import AccessToken
    from sqlalchemy.ext.asyncio import AsyncSession

from library.config import settings
from library.auth.models import User


async def get_user_db(session: "AsyncSession"):
    yield User.get_db(session=session)


async def get_access_token_db(session: "AsyncSession"):
    yield AccessToken.get_db(session=session)


def get_database_strategy(
        access_token_db: Annotated[
            AccessTokenDatabase["AccessToken"],
            Depends(get_access_token_db),
        ]
) -> DatabaseStrategy:
    return DatabaseStrategy(
        access_token_db,
        lifetime_seconds=settings.access_token.lifetime_seconds,
    )