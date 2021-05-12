import os
from itertools import chain
import asyncpg
import asyncio

from dotenv import load_dotenv

from app.db.schema import db_schema

load_dotenv()

schema = "".join(list(chain(*db_schema.values())))


async def init_db_schema():
    conn = await asyncpg.connect(os.getenv("DATABASE_URL"))
    try:
        await conn.execute(schema)
    except Exception as err:
        print(err)
    finally:
        await conn.close()

    return print('DB initialized')


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init_db_schema())
