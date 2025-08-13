from fastapi import APIRouter

from schemas.users import UserCreate, UserRead
from auth.fastapi_users_auth_router import fastapi_users

router = APIRouter(prefix="/register")

router.include_router(fastapi_users.get_register_router(UserRead, UserCreate))