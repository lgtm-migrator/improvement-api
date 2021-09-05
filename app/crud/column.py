from typing import List
from typing import Optional

from asyncpg import PostgresError
from fastapi import HTTPException
from pydantic.types import UUID4

from app.db.decorators import dbconn
from app.models.column import Column
from app.models.column import ColumnCreate


@dbconn
async def get_board_columns_and_column_order(conn, board_uuid: UUID4):
    try:
        columns_and_column_order = await conn.fetch("SELECT * FROM get_board_columns_and_column_order($1);", board_uuid)

        return columns_and_column_order
    except PostgresError:
        raise HTTPException(status_code=500, detail="Error while fetching the board columns and column order.")


@dbconn
async def create_column_and_update_board_column_order(conn, column: ColumnCreate, column_order: Optional[List[UUID4]]):
    try:
        column_and_board_column_order = await conn.fetchrow(
            "SELECT * FROM create_column_and_update_board_column_order($1,$2,$3);",
            column.column_name,
            column.board_uuid,
            column_order,
        )

        return column_and_board_column_order
    except PostgresError:
        raise HTTPException(status_code=500, detail="Error while trying to create a column.")


@dbconn
async def update_column_and_update_board_column_order(conn, column: Column, column_order: Optional[List[UUID4]]):
    try:
        column_and_board_column_order = await conn.fetchrow(
            "SELECT * FROM update_column_and_update_board_column_order($1,$2,$3,$4);",
            column.column_uuid,
            column.column_name,
            column.board_uuid,
            column_order,
        )

        return column_and_board_column_order
    except PostgresError:
        raise HTTPException(status_code=500, detail="Error while trying to update a column.")


@dbconn
async def delete_column_and_update_board_column_order(
    conn, board_uuid: UUID4, column_uuid: UUID4, column_order: List[UUID4]
):
    try:
        deleted_column_response = await conn.fetchrow(
            "SELECT * FROM delete_column_and_update_board_column_order($1,$2,$3);",
            board_uuid,
            column_uuid,
            column_order,
        )

        return deleted_column_response
    except PostgresError:
        raise HTTPException(status_code=500, detail="Error while trying to delete the column.")
