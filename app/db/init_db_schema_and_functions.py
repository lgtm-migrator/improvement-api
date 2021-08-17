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

SCHEMA_DIR = f"{dir_path}/db/schema"
FUNCTION_DIR = f"{dir_path}/db/functions"

# sql files where the order of executing them matters
# when initializing db for tests
init_schema_files = ["init.sql", "users.sql"]


def read_sql_file(file_path):
    with open(file_path, "r") as f:
        content = f.read()
        return f"{content}\n"


def create_db_schema():
    schema = read_sql_file(f"{SCHEMA_DIR}/init.sql")
    schema += read_sql_file(f"{SCHEMA_DIR}/users.sql")
    for file in listdir(SCHEMA_DIR):
        if file.endswith(".sql") and file not in init_schema_files:
            file_path = f"{SCHEMA_DIR}/{file}"
            file_content = read_sql_file(file_path)
            schema += f"{file_content}\n"
    return schema


def create_db_functions():
    functions = ""
    for file in listdir(FUNCTION_DIR):
        if file.endswith(".sql"):
            file_path = f"{FUNCTION_DIR}/{file}"
            file_content = read_sql_file(file_path)
            functions += f"{file_content}\n"
    return functions


async def init_db_schema_and_functions(test: Optional[bool] = False):
    if test:
        print("Using test db url...")
        conn = await asyncpg.connect(settings.TEST_DATABASE_URL)
    else:
        conn = await asyncpg.connect(settings.DATABASE_URL)

    try:
        schema = create_db_schema()
        functions = create_db_functions()

        await conn.execute(f"{schema} {functions}")
    except Exception as err:
        print(err)
    finally:
        await conn.close()

    return print("DB schema and functions initialized")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init_db_schema_and_functions())
