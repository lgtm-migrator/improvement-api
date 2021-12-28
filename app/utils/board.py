import json
from typing import List

from asyncpg import Record

from app.models.card import Card
from app.models.column import Column


def transform_column(column_rec: Record):
    col_model = Column(**column_rec)
    # needed for transforming uuid class into plain string
    return json.loads(col_model.json())


def transform_card(card_rec: Record):
    card_model = Card(**card_rec)
    # needed for transforming uuid class into plain string
    return json.loads(card_model.json())


def transform_and_sort_column_cards(board_card_records: List[Record], column: tuple):
    if not column[1].get("card_order"):
        return []

    card_list = [transform_card(card) for card in board_card_records if str(card.get("column_uuid")) == column[0]]
    return sorted(card_list, key=lambda card: column[1].get("card_order").index(card.get("card_uuid")))
