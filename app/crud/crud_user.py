from datetime import timedelta

from asyncpg import PostgresError
from fastapi import HTTPException

from app.core.config import settings
from app.core.security import create_access_token
from app.core.security import get_password_hash
from app.db.decorators import dbconn
from app.models.user import UserCreate


@dbconn
async def get_user_by_username(conn, username: str):
    try:
        user_by_username = f"""
            SELECT username FROM users WHERE username='{username}';
        """
        user = await conn.fetchrow(user_by_username)

        return user
    except PostgresError:
        raise HTTPException(status_code=500, detail="Error while fetching a user.")


@dbconn
async def create_user_with_token(conn, user: UserCreate):
    try:
        hashed_pwd = get_password_hash(user.password)

        insert_user_with_email = f"""
            INSERT INTO users (
                username,
                email,
                is_active,
                password
            ) VALUES (
                '{user.username}',
                '{user.email}',
                true,
                '{hashed_pwd}'
            ) RETURNING user_uid, username;
        """

        insert_user_no_email = f"""
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

        insert_user = insert_user_no_email if not user.email else insert_user_with_email

        new_user = await conn.fetchrow(insert_user)

        access_token = create_access_token(
            data={"sub": f"username:{user.username}"}, expires_delta=timedelta(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        return {**new_user, "token_data": {"access_token": access_token, "token_type": "bearer"}}
    except PostgresError:
        raise HTTPException(status_code=500, detail="Error while trying to create a user.")
