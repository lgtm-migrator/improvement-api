from typing import List

from pydantic import Field
from pydantic import UUID4

from app.models.api_model import APIModel


class Card(APIModel):
    card_uuid: UUID4
    column_uuid: UUID4
    board_uuid: UUID4
    card_name: str = Field(..., max_length=150)
    card_description: str


class CardCreate(APIModel):
    column_uuid: UUID4
    card_name: str = Field(..., max_length=150)


class CardNameOrDescriptionUpdate(APIModel):
    card_uuid: UUID4
    card_name: str = Field(..., max_length=150)
    card_description: str


class CardDelete(APIModel):
    card_uuid: UUID4
    column_uuid: UUID4


class CardAndOrderInColumns(APIModel):
    card_uuid: UUID4
    source_column_uuid: UUID4
    source_col_card_order: List[UUID4]
    destination_column_uuid: UUID4
    destination_col_card_order: List[UUID4]
