CREATE TYPE board_info AS (
    board_uuid UUID,
    board_name TEXT,
    column_order UUID[],
    owner_uuid UUID
);

CREATE TYPE board_column_order AS (
    column_order UUID[]
);

CREATE OR REPLACE FUNCTION create_board (arg_board_name TEXT, arg_owner_uuid UUID)
    RETURNS SETOF board_info LANGUAGE plpgsql AS $$
DECLARE
    l_board_uuid UUID;
    l_board_name TEXT;
    l_column_order UUID[];
    l_owner_uuid UUID;
BEGIN
    INSERT INTO boards (
            board_name,
            owner_uuid
        )
        VALUES (arg_board_name, arg_owner_uuid)
            RETURNING board_uuid, board_name, column_order, owner_uuid
            INTO l_board_uuid, l_board_name, l_column_order, l_owner_uuid;
    INSERT INTO user_boards
        VALUES (l_owner_uuid, l_board_uuid);
    RETURN NEXT (l_board_uuid, l_board_name, l_column_order, l_owner_uuid);
END;
$$;

CREATE OR REPLACE FUNCTION get_user_boards (arg_user_uuid UUID)
RETURNS SETOF board_info STABLE LANGUAGE sql AS $$
    SELECT  *
        FROM boards
            WHERE boards.owner_uuid = arg_user_uuid;
$$;

CREATE OR REPLACE FUNCTION get_user_board (arg_user_uuid UUID, arg_board_uuid UUID)
RETURNS SETOF board_info STABLE LANGUAGE sql AS $$
    SELECT  *
        FROM boards
            WHERE boards.owner_uuid = arg_user_uuid
            AND boards.board_uuid = arg_board_uuid;
$$;

CREATE OR REPLACE FUNCTION get_board_column_order (arg_board_uuid UUID)
RETURNS board_column_order LANGUAGE sql AS $$
    SELECT column_order
        FROM boards
            WHERE boards.board_uuid = arg_board_uuid;
$$;

CREATE OR REPLACE FUNCTION update_board (arg_board_name TEXT, arg_column_order UUID[], arg_owner_uuid UUID, arg_board_uuid UUID, arg_user_uuid UUID)
RETURNS SETOF board_info LANGUAGE sql AS $$
    UPDATE boards
        SET
            board_name = arg_board_name,
            owner_uuid = arg_owner_uuid,
            column_order = arg_column_order
        WHERE board_uuid = arg_board_uuid AND owner_uuid = arg_user_uuid
        RETURNING *;
$$;

CREATE OR REPLACE FUNCTION update_board_column_order (arg_board_uuid UUID, arg_column_order UUID[])
RETURNS board_column_order LANGUAGE sql AS $$
    UPDATE boards
        SET
            column_order = arg_column_order
        WHERE board_uuid = arg_board_uuid
        RETURNING column_order;
$$;

CREATE OR REPLACE FUNCTION delete_board (arg_board_uuid UUID, arg_user_uuid UUID)
RETURNS void LANGUAGE sql AS $$
    DELETE FROM boards
        WHERE boards.board_uuid = arg_board_uuid AND boards.owner_uuid = arg_user_uuid;
$$;
