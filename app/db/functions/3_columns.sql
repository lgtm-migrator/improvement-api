CREATE TYPE column_info AS (
    column_uuid UUID,
    column_name TEXT,
    board_uuid UUID
);


CREATE TYPE column_and_board_column_order AS (
    column_uuid UUID,
    column_name TEXT,
    board_uuid UUID,
    column_order UUID[]
);


CREATE OR REPLACE FUNCTION create_column (arg_column_name TEXT, arg_board_uuid UUID)
RETURNS SETOF column_info LANGUAGE sql AS $$
    INSERT INTO
        columns (
            column_name,
            board_uuid
        ) VALUES (
            arg_column_name,
            arg_board_uuid
        ) RETURNING *;
$$;


CREATE OR REPLACE FUNCTION get_board_columns (arg_board_uuid UUID)
RETURNS SETOF column_info STABLE LANGUAGE sql AS $$
    SELECT  *
        FROM columns
            WHERE columns.board_uuid = arg_board_uuid;
$$;


CREATE OR REPLACE FUNCTION update_column (arg_column_uuid UUID, arg_column_name TEXT, arg_board_uuid UUID)
RETURNS SETOF column_info LANGUAGE sql AS $$
    UPDATE columns
        SET
            column_name = arg_column_name
        WHERE column_uuid = arg_column_uuid AND board_uuid = arg_board_uuid
        RETURNING *;
$$;


CREATE OR REPLACE FUNCTION delete_column (arg_column_uuid UUID)
RETURNS void LANGUAGE sql AS $$
    DELETE FROM columns
        WHERE columns.column_uuid = arg_column_uuid;
$$;


CREATE OR REPLACE FUNCTION create_column_and_update_board_column_order (arg_column_name TEXT,
                                                                        arg_board_uuid UUID,
                                                                        arg_column_order UUID[] default null)
RETURNS SETOF column_and_board_column_order LANGUAGE plpgsql AS $$
DECLARE
    result column_and_board_column_order;
BEGIN

    SELECT
        column_uuid,
        column_name,
        board_uuid
    INTO
        result.column_uuid,
        result.column_name,
        result.board_uuid
    FROM create_column(arg_column_name, arg_board_uuid);

    SELECT column_order INTO result.column_order
    FROM update_board_column_order(arg_board_uuid, array_append(arg_column_order, result.column_uuid));

    RETURN NEXT result;

END $$;


CREATE OR REPLACE FUNCTION update_column_and_update_board_column_order (arg_column_uuid UUID,
                                                                        arg_column_name TEXT,
                                                                        arg_board_uuid UUID,
                                                                        arg_column_order UUID[] default null)
RETURNS SETOF column_and_board_column_order LANGUAGE plpgsql AS $$
DECLARE
    result column_and_board_column_order;
BEGIN

    SELECT
        column_uuid,
        column_name,
        board_uuid
    INTO
        result.column_uuid,
        result.column_name,
        result.board_uuid
    FROM update_column(arg_column_uuid, arg_column_name, arg_board_uuid);

    SELECT column_order INTO result.column_order
    FROM update_board_column_order(arg_board_uuid, arg_column_order);

    RETURN NEXT result;

END $$;


CREATE OR REPLACE FUNCTION delete_column_and_update_board_column_order (arg_board_uuid UUID,
                                                                        arg_column_uuid UUID,
                                                                        arg_column_order UUID[] default null)
RETURNS SETOF board_column_order LANGUAGE plpgsql AS $$
DECLARE
    l_column_order board_column_order;
BEGIN

    PERFORM delete_column(arg_column_uuid);

    SELECT column_order INTO l_column_order
    FROM update_board_column_order(arg_board_uuid, arg_column_order);

    RETURN NEXT l_column_order;

END $$;


CREATE OR REPLACE FUNCTION get_board_columns_and_column_order (arg_board_uuid UUID)
RETURNS SETOF column_and_board_column_order STABLE LANGUAGE sql AS $$
    SELECT * FROM get_board_columns(arg_board_uuid)
    JOIN (SELECT * FROM get_board_column_order(arg_board_uuid) AS sub) sub ON true;
$$;
