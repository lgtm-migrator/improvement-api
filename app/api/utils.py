from typing import Union

from app.core.security import verify_password
from app.crud.user import get_user_by_username
from app.models.user import User


async def authenticate(username: str, password: str) -> Union[User, None]:
    user = await get_user_by_username(username)

    if not user:
        return None
    if not verify_password(password, user["password"]):
        return None

    return User(**user)


def user_token_sub(user) -> str:
    return f"user_uuid:{user.user_uuid}username:{user.username}"
