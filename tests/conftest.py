import asyncio

import asyncpg
import pytest
from asyncpg import PostgresError

from app.core.config import settings
from app.core.security import get_password_hash
from app.db.init_db_schema_and_functions import init_db_schema_and_functions


def init_test_db():
    # create user in db matching the user_in_db fixture below
    async def create_existing_test_user():
        conn = await asyncpg.connect(settings.TEST_DATABASE_URL)
        hashed_pwd = get_password_hash("superstrongpassword")
        insert_existing_test_user = """
            INSERT INTO users (user_uuid, username, email, is_active, password)
            VALUES ('1088292a-46cc-4258-85b6-9611f09e1830', 'testuser_exists', 'testuser_exists@mail.com', true, $1);
        """
        try:
            await conn.execute(insert_existing_test_user, hashed_pwd)
        except PostgresError as err:
            print(err)
        finally:
            await conn.close()

    asyncio.get_event_loop().run_until_complete(init_db_schema_and_functions(test=True))
    asyncio.get_event_loop().run_until_complete(create_existing_test_user())


def clean_up():
    async def clear_test_db():
        print("\n\nClearing test db...")
        conn = await asyncpg.connect(settings.TEST_DATABASE_URL)

        # drop schema
        # this clears all the data, types and functions from public schema
        drop_schema = """
            DROP SCHEMA public CASCADE;
            CREATE SCHEMA public;
        """

        try:
            await conn.execute(drop_schema)
        except PostgresError as err:
            print(err)
        finally:
            await conn.close()

    asyncio.get_event_loop().run_until_complete(clear_test_db())


def pytest_sessionstart():
    """whole test run starts."""
    settings.DATABASE_URL = settings.TEST_DATABASE_URL
    init_test_db()


def pytest_sessionfinish():
    """whole test run finishes."""
    clean_up()


@pytest.fixture
def test_user():
    return {"username": "testuser", "password": "verystrongpassword"}


# use this user for tests where you need a user that already exists in db
# without first having to create it through API
@pytest.fixture
def user_in_db():
    return {"username": "testuser_exists", "password": "superstrongpassword"}
