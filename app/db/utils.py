import asyncpg
from asyncpg.connection import Connection
from fastapi import HTTPException

from app.core.config import settings


def create_db_connection() -> Connection:
    try:
        conn = asyncpg.connect(settings.DATABASE_URL)
    except Exception:
        raise HTTPException(status_code=500, detail="Database connection failure")

    return conn
