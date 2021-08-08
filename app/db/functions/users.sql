CREATE TYPE user_info AS (
    user_uuid UUID,
    username TEXT,
    email TEXT,
    is_active BOOLEAN,
    password TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TYPE new_user_info AS (
    user_uuid UUID,
    username TEXT
);

CREATE OR REPLACE FUNCTION get_user_by_uuid (arg_user_uuid UUID)
RETURNS SETOF user_info STABLE LANGUAGE sql AS $$
    SELECT  *
        FROM users
            WHERE users.user_uuid = arg_user_uuid;
$$;

CREATE OR REPLACE FUNCTION get_user_by_username (arg_username TEXT)
RETURNS SETOF user_info STABLE LANGUAGE sql AS $$
    SELECT  *
        FROM users
            WHERE users.username = arg_username;
$$;

CREATE OR REPLACE FUNCTION create_user (arg_username TEXT, arg_hashed_pwd TEXT)
RETURNS SETOF new_user_info LANGUAGE sql AS $$
    INSERT INTO 
        users (
            username,
            is_active,
            password
        ) VALUES (
            arg_username,
            TRUE,
            arg_hashed_pwd
        ) RETURNING user_uuid, username;
$$;
