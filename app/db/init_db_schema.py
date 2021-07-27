import asyncio
import sys
from os import listdir
from os import pardir
from os import path
from typing import Optional

import asyncpg

dir_path = path.dirname(path.abspath(__file__).replace("db", ""))
sys.path.append(path.abspath(path.join(dir_path, pardir)))

from app.core.config import settings  # noqa: E402


SCHEMA_DIR = "app/db/schema"


def read_sql_file(file_path):
    with open(file_path, "r") as f:
        content = f.read()
        return f"{content}\n"


def create_db_schema():
    schema = read_sql_file(f"{SCHEMA_DIR}/init.sql")
    for file in listdir(SCHEMA_DIR):
        if file.endswith(".sql") and file != "init.sql":
            file_path = f"{SCHEMA_DIR}/{file}"
            file_content = read_sql_file(file_path)
            schema += f"{file_content}\n"
    return schema


async def init_db_schema(test: Optional[bool] = False):
    if test:
        print("Using test db url...")
        conn = await asyncpg.connect(settings.TEST_DATABASE_URL)
    else:
        conn = await asyncpg.connect(settings.DATABASE_URL)
    try:
        schema = create_db_schema()
        await conn.execute(schema)
    except Exception as err:
        print(err)
    finally:
        await conn.close()

    return print("DB initialized")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init_db_schema())
