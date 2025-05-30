from fastapi import APIRouter

from .routers.books import router as books_router


router = APIRouter()
router.include_router(router=books_router, prefix="/books")