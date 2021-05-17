import asyncio

import asyncpg
import pytest

from app.core.config import settings
from app.core.security import get_password_hash
from app.db.init_db_schema import init_db_schema


def init_test_db():
    # create user in db matching the user_in_db fixture below
    async def create_existing_test_user():
        conn = await asyncpg.connect(settings.TEST_DATABASE_URL)
        hashed_pwd = get_password_hash("superstrongpassword")
        insert_existing_test_user = f"""
            INSERT INTO users (user_uuid, username, email, is_active, password) values ('1088292a-46cc-4258-85b6-9611f09e1830', 'testuser_exists', 'testuser_exists@mail.com', true, '{hashed_pwd}');
        """
        try:
            await conn.execute(insert_existing_test_user)
        except Exception as err:
            print(err)
        finally:
            await conn.close()

    asyncio.get_event_loop().run_until_complete(init_db_schema(test=True))
    asyncio.get_event_loop().run_until_complete(create_existing_test_user())


def clean_up():
    async def clear_test_db():
        print("\n\nClearing test db...")
        conn = await asyncpg.connect(settings.TEST_DATABASE_URL)

        # https://dba.stackexchange.com/a/152463
        # drop all tables from the public schema
        drop_tables = """
            DO $$ DECLARE
                tabname RECORD;
            BEGIN
                FOR tabname IN (SELECT tablename
                                FROM pg_tables
                                WHERE schemaname = 'public')
            LOOP
                EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(tabname.tablename) || ' CASCADE';
            END LOOP;
            END $$;
        """
        try:
            await conn.execute(drop_tables)
        except Exception as err:
            print(err)
        finally:
            await conn.close()

    asyncio.get_event_loop().run_until_complete(clear_test_db())


def pytest_sessionstart(session):
    """whole test run starts."""
    settings.DATABASE_URL = settings.TEST_DATABASE_URL
    init_test_db()


def pytest_sessionfinish(session, exitstatus):
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
