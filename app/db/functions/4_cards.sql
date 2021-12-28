CREATE TYPE card_info AS (
    card_uuid UUID,
    card_name TEXT,
    card_description TEXT,
    column_uuid UUID,
    board_uuid UUID
);


CREATE TYPE card_uuid_and_column_card_order AS (
    card_uuid UUID,
    column_order UUID[]
);


CREATE TYPE column_card_order AS (
    card_order UUID[]
);


CREATE OR REPLACE FUNCTION create_card (arg_card_name TEXT, arg_column_uuid UUID, arg_board_uuid UUID)
RETURNS SETOF card_info LANGUAGE sql AS $$
    INSERT INTO
        cards (
            card_name,
            column_uuid,
            board_uuid
        ) VALUES (
            arg_card_name,
            arg_column_uuid,
            arg_board_uuid
        ) RETURNING *;
$$;


CREATE OR REPLACE FUNCTION get_board_cards (arg_board_uuid UUID)
RETURNS SETOF card_info STABLE LANGUAGE sql AS $$
    SELECT  *
        FROM cards
            WHERE cards.board_uuid = arg_board_uuid;
$$;


CREATE OR REPLACE FUNCTION update_card_name_or_description (arg_card_uuid UUID, arg_card_name TEXT, arg_card_description TEXT)
RETURNS SETOF card_info LANGUAGE sql AS $$
    UPDATE cards
        SET
            card_name = arg_card_name, card_description = arg_card_description
        WHERE card_uuid = arg_card_uuid
        RETURNING *;
$$;


CREATE OR REPLACE FUNCTION delete_card (arg_card_uuid UUID)
RETURNS void LANGUAGE sql AS $$
    DELETE FROM cards
        WHERE cards.card_uuid = arg_card_uuid;
$$;


CREATE OR REPLACE FUNCTION create_card_and_update_column_card_order (arg_card_name TEXT,
                                                                        arg_column_uuid UUID,
                                                                        arg_board_uuid UUID,
                                                                        arg_card_order UUID[])
RETURNS SETOF card_uuid_and_column_card_order LANGUAGE plpgsql AS $$
DECLARE
    result card_uuid_and_column_card_order;
BEGIN

    SELECT
        card_uuid
    INTO
        result.card_uuid
    FROM create_card(arg_card_name, arg_column_uuid, arg_board_uuid);

    SELECT card_order INTO result.card_order
    FROM update_single_column_card_order(arg_column_uuid, array_prepend(result.card_uuid, arg_card_order));

    RETURN NEXT result;

END $$;


CREATE OR REPLACE FUNCTION delete_card_and_update_column_card_order (arg_card_uuid UUID,
                                                                        arg_column_uuid UUID,
                                                                        arg_column_order UUID[])
RETURNS SETOF column_card_order LANGUAGE plpgsql AS $$
DECLARE
    l_column_order column_card_order;
BEGIN

    PERFORM delete_card(arg_card_uuid);

    SELECT column_order INTO l_column_order
    FROM update_single_column_card_order(arg_column_uuid, arg_column_order);

    RETURN NEXT l_column_order;

END $$;


CREATE OR REPLACE FUNCTION update_card_column_uuid (arg_card_uuid UUID, arg_column_uuid UUID)
RETURNS void LANGUAGE sql AS $$
    UPDATE cards
        SET column_uuid = arg_column_uuid
        WHERE card_uuid = arg_card_uuid;
$$


CREATE OR REPLACE FUNCTION update_card_and_order_in_columns (arg_card_uuid UUID,
                                                                arg_source_column_uuid UUID,
                                                                arg_source_col_card_order UUID[],
                                                                arg_destination_column_uuid UUID,
                                                                arg_destination_col_card_order UUID[])
RETURNS void LANGUAGE plpgsql AS $$
BEGIN

    PERFORM update_card_column_uuid(arg_card_uuid, arg_destination_column_uuid);

    PERFORM update_single_column_card_order(arg_destination_column_uuid, arg_destination_col_card_order);

    PERFORM update_single_column_card_order(arg_source_column_uuid, arg_source_col_card_order);

END $$;
