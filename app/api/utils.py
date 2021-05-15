from typing import Union

from app.crud.crud_user import get_user_by_username
from app.core.security import verify_password
from app.models.user import UserDBBase


async def authenticate(username: str, password: str) -> Union[UserDBBase, None]:
    user = await get_user_by_username(username)

    if not user:
        return None
    if not verify_password(password, user["password"]):
        return None

    return UserDBBase(**user)


def user_token_sub(user) -> str:
    return f"user_uuid:{user.user_uid}username:{user.username}"
