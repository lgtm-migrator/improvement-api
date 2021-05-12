import os
from datetime import datetime
from datetime import timedelta
from typing import Optional

import asyncpg
from jose import jwt
from passlib.context import CryptContext

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=ALGORITHM)
    return encoded_jwt


async def get_user_by_username(username: str):
    conn = await asyncpg.connect(os.getenv("DATABASE_URL"))
    try:
        user_by_username = f"""
            SELECT username FROM users WHERE username='{username}';
        """
        user = await conn.fetchrow(user_by_username)

        return user
    except Exception as err:
        print(err)
    finally:
        await conn.close()


async def create_user_with_token(user):
    conn = await asyncpg.connect(os.getenv("DATABASE_URL"))
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
            data={"sub": f"username:{user.username}"}, expires_delta=timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        return {**new_user, "token_data": {"access_token": access_token, "token_type": "bearer"}}
    except Exception as err:
        print(err)
    finally:
        await conn.close()
