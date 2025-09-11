from fastapi import APIRouter, Depends

from .authentication import router as auth_router
from .register import router as register_router
from .verify import router as verify_router
from .reset_password import router as reset_password_router
from .manage_user import router as manage_user_router

from fastapi.security import HTTPBearer


http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(tags=["Auth"], dependencies=[Depends(http_bearer)])
router.include_router(auth_router)
router.include_router(register_router)
router.include_router(verify_router)
router.include_router(reset_password_router)
router.include_router(manage_user_router)