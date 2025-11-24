from fastapi import APIRouter

router = APIRouter()

from .endpoints import user

router.include_router(user.router, prefix="/users", tags=["users"])
