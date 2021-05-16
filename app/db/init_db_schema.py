import asyncio
import sys
from itertools import chain
from os import pardir
from os import path
from typing import Optional

import asyncpg

dir_path = path.dirname(path.abspath(__file__).replace("db", ""))
sys.path.append(path.abspath(path.join(dir_path, pardir)))

from app.db.schema import db_schema  # noqa: E402
from app.core.config import settings  # noqa: E402


schema = "".join(list(chain(*db_schema.values())))


async def init_db_schema(test: Optional[bool] = False):
    if test:
        print("Using test db url...")
        conn = await asyncpg.connect(settings.TEST_DATABASE_URL)
    else:
        conn = await asyncpg.connect(settings.DATABASE_URL)

    try:
        await conn.execute(schema)
    except Exception as err:
        print(err)
    finally:
        await conn.close()

    return print("DB initialized")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init_db_schema())
