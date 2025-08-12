import logging
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin

from database.config import settings
from models.users import User, get_user_db

log = logging.getLogger(__name__)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.reset_password_token_secret
    verification_token_secret = settings.verification_token_secret

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        log.warning("User %r has registered.", user.id)

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        log.warning("User %r has forgot their password. Reset token: %r", user.id, token)

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        log.warning("Verification requested for user %r. Verification token: %r", user.id, token)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)