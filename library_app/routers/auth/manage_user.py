from fastapi import APIRouter

from auth.fastapi_users_auth_router import fastapi_users
from schemas.users import UserRead, UserUpdate

router = APIRouter(prefix="/manage-user")

router.include_router(fastapi_users.get_users_router(UserRead, UserUpdate))