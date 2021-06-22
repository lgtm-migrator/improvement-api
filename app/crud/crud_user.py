from asyncpg import PostgresError
from fastapi import HTTPException
from pydantic import UUID4

from app.core.security import get_password_hash
from app.db.decorators import dbconn
from app.models.user import User
from app.models.user import UserCreate
from app.models.user import UserInDB


@dbconn
async def get_user_by_username(conn, username: str) -> UserInDB:
    try:
        user_by_username = """
            SELECT * FROM users WHERE username = $1;
        """
        user = await conn.fetchrow(user_by_username, username)

        return user
    except PostgresError:
        raise HTTPException(status_code=500, detail="Error while fetching a user.")


@dbconn
async def get_user_by_uuid(conn, uuid: UUID4) -> UserInDB:
    try:
        user_by_uuid = """
            SELECT * FROM users WHERE user_uuid = $1;
        """
        user = await conn.fetchrow(user_by_uuid, uuid)

        return user
    except PostgresError:
        raise HTTPException(status_code=500, detail="Error while fetching a user.")


@dbconn
async def create_user(conn, user: UserCreate) -> User:
    try:
        hashed_pwd = get_password_hash(user.password)

        insert_user = """
            INSERT INTO users (
                username,
                is_active,
                password
            ) VALUES (
                $1,
                true,
                $2
            ) RETURNING user_uuid, username;
        """

        new_user = await conn.fetchrow(insert_user, user.username, hashed_pwd)
        return User(**new_user)
    except PostgresError:
        raise HTTPException(status_code=500, detail="Error while trying to create a user.")
