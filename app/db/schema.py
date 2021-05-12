# the --sql flag inside the SQL strings is for a vs code extension python-string-sql
# it allows for SQL syntax highlighting inside python multiline strings


db_init = '''
    --sql
    SET TIMEZONE='UTC';

    --sql
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

    -- Trigger function for updating a created at column on a table

    --sql
    CREATE OR REPLACE FUNCTION trigger_set_timestamp()
    RETURNS TRIGGER AS $$
    BEGIN
        IF row(NEW.*) IS DISTINCT FROM row(OLD.*) THEN
        NEW.updated_at = NOW();
        RETURN NEW;
        ELSE
            RETURN OLD;
        END IF;
    END;
    $$ LANGUAGE 'plpgsql';
'''


users_table = '''
    --sql
    CREATE TABLE IF NOT EXISTS users (
        user_uid UUID NOT NULL PRIMARY KEY,
        username VARCHAR(150) NOT NULL,
        email VARCHAR(255),
        is_active BOOLEAN NOT NULL,
        password VARCHAR(255) NOT NULL,
        salt VARCHAR(255) NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
        UNIQUE(username),
        UNIQUE(email)
    );

    --sql
    CREATE TRIGGER set_timestamp
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE PROCEDURE trigger_set_timestamp();
'''


db_schema: dict = {
    "db_init": db_init,
    "users_table": users_table
}
