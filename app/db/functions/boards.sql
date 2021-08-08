CREATE TYPE board_info AS (
    board_uuid UUID,
    board_name TEXT,
    column_order UUID[],
    owner_uuid UUID
);

CREATE OR REPLACE FUNCTION create_board (arg_board_name TEXT, arg_owner_uuid UUID)
    RETURNS SETOF board_info LANGUAGE plpgsql AS $$
DECLARE
    i_board_uuid UUID;
    i_board_name TEXT;
    i_column_order UUID[];
    i_owner_uuid UUID;
BEGIN
    INSERT INTO boards (
            board_name,
            owner_uuid
        )
        VALUES (arg_board_name, arg_owner_uuid)
            RETURNING board_uuid, board_name, column_order, owner_uuid
            INTO i_board_uuid, i_board_name, i_column_order, i_owner_uuid;
    INSERT INTO user_boards
        VALUES (i_owner_uuid, i_board_uuid);
    RETURN NEXT (i_board_uuid, i_board_name, i_column_order, i_owner_uuid);
END;
$$;
