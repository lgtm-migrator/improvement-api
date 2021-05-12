from fastapi import APIRouter
from fastapi import HTTPException

from app.crud.crud_user import create_user_with_token
from app.crud.crud_user import get_user_by_username
from app.models.user import UserCreate
from app.models.user import UserWithToken


auth_router = APIRouter()


@auth_router.post("/register", response_model=UserWithToken)
async def register(user: UserCreate):
    user_exists = await get_user_by_username(user.username)

    if user_exists:
        raise HTTPException(status_code=400, detail="This username is already taken.")

    new_user_with_token = await create_user_with_token(user)
    return new_user_with_token
