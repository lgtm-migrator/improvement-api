CREATE TABLE IF NOT EXISTS cards (
    card_uuid UUID NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    card_name VARCHAR(150) NOT NULL,
    card_description VARCHAR,
    column_uuid UUID REFERENCES columns(column_uuid) ON UPDATE CASCADE ON DELETE CASCADE NOT NULL,
    board_uuid UUID REFERENCES boards(board_uuid) ON UPDATE CASCADE ON DELETE CASCADE NOT NULL
);
