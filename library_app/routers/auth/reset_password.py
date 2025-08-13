from fastapi import APIRouter

from auth.fastapi_users_auth_router import fastapi_users

router = APIRouter(prefix="/reset-password")
router.include_router(fastapi_users.get_reset_password_router())