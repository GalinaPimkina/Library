from fastapi import APIRouter

from auth.backend import authentication_backend
from auth.fastapi_users_auth_router import fastapi_users

router = APIRouter(prefix="/authentication")

router.include_router(fastapi_users.get_auth_router(authentication_backend))