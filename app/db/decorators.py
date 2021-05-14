from typing import Callable

from .utils import create_db_connection


def dbconn(db_function: Callable):
    """
    Decorator that opens and provides a database connection to passed in functions and
    closes it afterwards

    Args:
        db_function (FunctionType): function for database queries/mutations
    """

    async def decorator(*args):
        conn = await create_db_connection()
        try:
            results = await db_function(conn, *args)
        finally:
            await conn.close()

        return results

    return decorator
