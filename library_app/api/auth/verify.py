from fastapi import APIRouter

from auth.fastapi_users_auth_router import fastapi_users
from schemas.users import UserRead

router = APIRouter(prefix="/verify")

router.include_router(fastapi_users.get_verify_router(UserRead))