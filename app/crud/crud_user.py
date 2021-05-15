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
        user_by_username = f"""
            SELECT * FROM users WHERE username='{username}';
        """
        user = await conn.fetchrow(user_by_username)

        return user
    except PostgresError:
        raise HTTPException(status_code=500, detail="Error while fetching a user.")


@dbconn
async def get_user_by_uuid(conn, uuid: UUID4) -> UserInDB:
    try:
        user_by_uuid = f"""
            SELECT * FROM users WHERE user_uid='{uuid}';
        """
        user = await conn.fetchrow(user_by_uuid)

        return user
    except PostgresError:
        raise HTTPException(status_code=500, detail="Error while fetching a user.")


@dbconn
async def create_user(conn, user: UserCreate) -> User:
    try:
        hashed_pwd = get_password_hash(user.password)

        insert_user = f"""
            INSERT INTO users (
                username,
                is_active,
                password
            ) VALUES (
                '{user.username}',
                true,
                '{hashed_pwd}'
            ) RETURNING user_uid, username;
        """

        new_user = await conn.fetchrow(insert_user)
        return User(**new_user)
    except PostgresError:
        raise HTTPException(status_code=500, detail="Error while trying to create a user.")
