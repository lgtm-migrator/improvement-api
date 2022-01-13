from typing import List

from asyncpg import PostgresError
from asyncpg.connection import Connection
from fastapi import HTTPException
from pydantic.types import UUID4

from app.db.decorators import dbconn
from app.models.card import CardAndOrderInColumns
from app.models.card import CardCreate
from app.models.card import CardDelete
from app.models.card import CardNameOrDescriptionUpdate


@dbconn
async def create_card_and_update_column_card_order(
    conn: Connection, card: CardCreate, board_uuid: UUID4, column_card_order: List[UUID4]
):
    try:
        new_card = await conn.fetchrow(
            "SELECT * FROM create_card_and_update_column_card_order($1,$2,$3,$4);",
            card.card_name,
            card.column_uuid,
            board_uuid,
            column_card_order,
        )

        return new_card
    except PostgresError:
        raise HTTPException(status_code=500, detail="Error while trying to create a card.")


@dbconn
async def update_card_name_or_description(conn: Connection, card: CardNameOrDescriptionUpdate):
    try:
        card = await conn.fetchrow(
            "SELECT * FROM update_card_name_or_description($1, $2, $3);",
            card.card_uuid,
            card.card_name,
            card.card_description,
        )

        return card
    except PostgresError:
        raise HTTPException(status_code=500, detail="Error while trying to update the card name or description.")


@dbconn
async def delete_card_and_update_column_card_order(conn: Connection, card: CardDelete, column_card_order: List[UUID4]):
    try:
        deleted_card_response = await conn.fetch(
            "SELECT * FROM delete_card_and_update_column_card_order($1, $2, $3);",
            card.card_uuid,
            card.column_uuid,
            column_card_order,
        )

        return deleted_card_response
    except PostgresError:
        raise HTTPException(status_code=500, detail="Error while trying to delete the card.")


@dbconn
async def update_card_and_order_in_columns(conn: Connection, data: CardAndOrderInColumns):
    try:
        card = await conn.fetchrow(
            "SELECT * FROM update_card_and_order_in_columns($1, $2, $3, $4, $5);",
            data.card_uuid,
            data.source_column_uuid,
            data.source_col_card_order,
            data.destination_column_uuid,
            data.destination_col_card_order,
        )

        return card
    except PostgresError:
        raise HTTPException(status_code=500, detail="Error while trying to update the card order in columns.")


async def handle_card_crud(board_uuid: str, crud_type: str, data: dict):
    column_card_order = data.get("column_card_order")

    if crud_type == "create":
        return await create_card_and_update_column_card_order(
            CardCreate(**data.get("new_card")), board_uuid, column_card_order  # type: ignore
        )

    if crud_type == "delete":
        return await delete_card_and_update_column_card_order(CardDelete(**data.get("delete_card")), column_card_order)  # type: ignore

    if crud_type == "update-name-or-description":
        return await update_card_name_or_description(CardNameOrDescriptionUpdate(**data.get("updated_card")))  # type: ignore


async def get_board_cards(conn: Connection, board_uuid: UUID4):
    try:
        cards = await conn.fetch("SELECT * FROM get_board_cards($1);", board_uuid)

        return cards
    except PostgresError:
        raise HTTPException(status_code=500, detail="Error while fetching the board cards.")
