from asyncpg import PostgresError
from asyncpg.connection import Connection
from fastapi import HTTPException
from pydantic.types import UUID4

from app.db.decorators import dbconn
from app.models.board import Board
from app.models.board import BoardCreate


@dbconn
async def create_board(conn: Connection, board: BoardCreate):
    try:
        new_board = await conn.fetchrow("SELECT * FROM create_board($1,$2);", board.board_name, board.owner_uuid)

        return new_board
    except PostgresError:
        raise HTTPException(status_code=500, detail="Error while trying to create a board.")


@dbconn
async def get_user_boards(conn: Connection, user_uuid: UUID4):
    # TODO: Change this later to also list the boards where the user is a member
    # (ie. boards related to user but where they're not the owner)
    try:
        boards = await conn.fetch("SELECT * FROM get_user_boards($1);", user_uuid)

        return boards
    except PostgresError:
        raise HTTPException(status_code=500, detail="Error while fetching the user's boards.")


@dbconn
async def get_user_board(conn: Connection, user_uuid: UUID4, board_uuid: UUID4):
    try:
        board = await conn.fetchrow("SELECT * FROM get_user_board($1, $2);", user_uuid, board_uuid)

        return board
    except PostgresError:
        raise HTTPException(status_code=500, detail="Error while fetching a board for the user.")


@dbconn
async def update_board(conn: Connection, board_data: Board, user_uuid: UUID4):
    try:
        board = await conn.fetchrow(
            "SELECT * FROM update_board($1, $2, $3, $4, $5);",
            board_data.board_name,
            board_data.column_order,
            board_data.owner_uuid,
            board_data.board_uuid,
            user_uuid,
        )

        return board
    except PostgresError:
        raise HTTPException(status_code=500, detail="Error while trying to update the board.")


@dbconn
async def delete_board(conn: Connection, board_uuid: UUID4, user_uuid: UUID4):
    try:
        deleted_board_response = await conn.fetch("SELECT * FROM delete_board($1, $2);", board_uuid, user_uuid)

        return deleted_board_response
    except PostgresError:
        raise HTTPException(status_code=500, detail="Error while trying to delete the board.")


async def get_board_column_order(conn: Connection, board_uuid: UUID4):
    try:
        column_order = await conn.fetchrow("SELECT * FROM get_board_column_order($1);", board_uuid)

        return column_order
    except PostgresError:
        raise HTTPException(status_code=500, detail="Error while trying to fetch board column order.")
