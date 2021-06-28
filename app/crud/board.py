from asyncpg import PostgresError
from fastapi import HTTPException
from pydantic.types import UUID4

from app.db.decorators import dbconn
from app.models.board import Board
from app.models.board import BoardCreate


@dbconn
async def create_board(conn, board: BoardCreate):
    try:
        insert_board = """
            INSERT INTO boards (
                board_name,
                owner_uuid
            )
            VALUES ($1,$2)
            RETURNING *;
        """

        new_board = await conn.fetchrow(insert_board, board.board_name, board.owner_uuid)

        insert_user_board = """
            INSERT INTO user_boards
            VALUES ($1,$2);
        """

        await conn.fetchrow(insert_user_board, new_board["owner_uuid"], new_board["board_uuid"])

        return new_board
    except PostgresError:
        raise HTTPException(status_code=500, detail="Error while trying to create a board.")


@dbconn
async def get_user_boards(conn, user_uuid: UUID4):
    # TODO: Change this later to also list the boards where the user is a member
    # (ie. boards related to user but where they're not the owner)
    try:
        fetch_boards = """
            SELECT * FROM boards WHERE owner_uuid = $1;
        """
        boards = await conn.fetch(fetch_boards, user_uuid)

        return boards
    except PostgresError:
        raise HTTPException(status_code=500, detail="Error while fetching the user's boards.")


@dbconn
async def get_user_board(conn, user_uuid: UUID4, board_uuid: UUID4):
    try:
        fetch_board = """
            SELECT * FROM boards WHERE owner_uuid = $1 and board_uuid = $2;
        """
        board = await conn.fetchrow(fetch_board, user_uuid, board_uuid)

        return board
    except PostgresError:
        raise HTTPException(status_code=500, detail="Error while fetching a board for the user.")


@dbconn
async def update_board(conn, board_data: Board, user_uuid: UUID4):
    try:
        update_board = """
            UPDATE boards
            SET
                board_name = $1,
                owner_uuid = $2
            WHERE board_uuid = $3 AND owner_uuid = $4
            RETURNING *;
        """
        board = await conn.fetchrow(
            update_board, board_data.board_name, board_data.owner_uuid, board_data.board_uuid, user_uuid
        )

        return board
    except PostgresError:
        raise HTTPException(status_code=500, detail="Error while trying to update the board.")


@dbconn
async def delete_board(conn, board_uuid: UUID4, user_uuid: UUID4):
    try:
        delete_board = """
            DELETE FROM boards WHERE board_uuid = $1 AND owner_uuid = $2;
        """
        deleted_board_response = await conn.fetch(delete_board, board_uuid, user_uuid)

        return deleted_board_response
    except PostgresError:
        raise HTTPException(status_code=500, detail="Error while trying to delete the board.")
