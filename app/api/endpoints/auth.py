from datetime import timedelta
from typing import Dict
from typing import Union

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import settings
from app.core.security import create_access_token
from app.core.security import verify_password
from app.crud.crud_user import create_user
from app.crud.crud_user import get_user_by_username
from app.models.token import Token
from app.models.user import UserDBBase


auth_router = APIRouter()


async def authenticate(username: str, password: str) -> Union[Dict[str, UserDBBase], None]:
    user_record = await get_user_by_username(username)

    if not user_record:
        return None
    if not verify_password(password, user_record["password"]):
        return None

    user = dict(user_record)
    user.pop("password")
    return user


@auth_router.post("/register", response_model=Token)
async def register(form_data: OAuth2PasswordRequestForm = Depends()):
    user_exists = await get_user_by_username(form_data.username)

    if user_exists:
        raise HTTPException(status_code=400, detail="This username is already taken.")

    new_user = await create_user(form_data)

    access_token = create_access_token(
        data={"sub": f"username:{new_user['username']}"}, expires_delta=timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/access-token", response_model=Token)
async def access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_data = await authenticate(form_data.username, form_data.password)

    if not user_data:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    elif not user_data.get("is_active"):
        raise HTTPException(status_code=400, detail="Inactive user")

    access_token = create_access_token(
        data={"sub": f"username:{user_data.get('username')}"},
        expires_delta=timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return {"access_token": access_token, "token_type": "bearer"}
