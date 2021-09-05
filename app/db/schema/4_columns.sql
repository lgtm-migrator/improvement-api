CREATE TABLE IF NOT EXISTS columns (
    column_uuid UUID NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    column_name VARCHAR(150) NOT NULL,
    board_uuid UUID REFERENCES boards(board_uuid) ON UPDATE CASCADE ON DELETE CASCADE NOT NULL
);
