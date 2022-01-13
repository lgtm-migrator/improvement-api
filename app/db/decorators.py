from typing import Callable

from app.core.config import settings


def dbconn(db_function: Callable):
    """
    Decorator that opens and provides a database connection to passed in functions and
    closes it afterwards

    Args:
        db_function (FunctionType): function for database queries/mutations
    """

    async def decorator(*args):
        conn_pool = settings.CONN_POOL
        async with conn_pool.acquire() as conn:
            results = await db_function(conn, *args)

        return results

    return decorator
