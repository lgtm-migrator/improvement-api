SET TIMEZONE='UTC';

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Trigger function for updating a created at column on a table

-- https://stackoverflow.com/a/26284695
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
