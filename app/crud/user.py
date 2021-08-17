from asyncpg import PostgresError
from fastapi import HTTPException
from pydantic import UUID4

from app.core.security import get_password_hash
from app.db.decorators import dbconn
from app.models.user import UserBase
from app.models.user import UserCreate
from app.models.user import UserInDB


@dbconn
async def get_user_by_username(conn, username: str) -> UserInDB:
    try:
        user = await conn.fetchrow("SELECT * FROM get_user_by_username($1);", username)

        return user
    except PostgresError:
        raise HTTPException(status_code=500, detail="Error while fetching a user from database.")


@dbconn
async def get_user_by_uuid(conn, uuid: UUID4) -> UserInDB:
    try:
        user = await conn.fetchrow("SELECT * FROM get_user_by_uuid($1);", uuid)

        return user
    except PostgresError:
        raise HTTPException(status_code=500, detail="Error while fetching a user from database.")


@dbconn
async def create_user(conn, user: UserCreate) -> UserBase:
    try:
        hashed_pwd = get_password_hash(user.password)
        new_user = await conn.fetchrow("SELECT * FROM create_user($1, $2);", user.username, hashed_pwd)

        return UserBase(**new_user)
    except PostgresError:
        raise HTTPException(status_code=500, detail="Error while trying to create a user in database.")
