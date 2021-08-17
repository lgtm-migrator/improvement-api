from typing import List
from typing import Optional

from pydantic import Field
from pydantic import UUID4

from app.models.api_model import APIModel


class Board(APIModel):
    board_uuid: UUID4
    board_name: str = Field(..., max_length=150)
    column_order: Optional[List[UUID4]]
    owner_uuid: UUID4


class BoardCreate(APIModel):
    board_name: str
    owner_uuid: UUID4
