CREATE TABLE IF NOT EXISTS boards (
    board_uuid UUID NOT NULL PRIMARY KEY DEFAULT uuid_generate_v4(),
    board_name VARCHAR(150) NOT NULL,
    column_order UUID[],
    owner_uuid UUID REFERENCES users(user_uuid) NOT NULL
);

CREATE TABLE IF NOT EXISTS user_boards (
    user_uuid UUID REFERENCES users(user_uuid) ON UPDATE CASCADE NOT NULL,
    board_uuid UUID REFERENCES boards(board_uuid) ON UPDATE CASCADE ON DELETE CASCADE NOT NULL,
    CONSTRAINT user_boards_uuid PRIMARY KEY (user_uuid, board_uuid)
);
