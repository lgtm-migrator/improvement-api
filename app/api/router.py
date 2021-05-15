from fastapi import APIRouter

from app.api.endpoints.auth import auth_router
from app.api.endpoints.user import user_router


api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["authentication"])
api_router.include_router(user_router, prefix="/user", tags=["user"])
