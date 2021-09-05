from typing import List
from typing import Optional

from pydantic import Field
from pydantic import UUID4

from app.models.api_model import APIModel


class Column(APIModel):
    column_uuid: UUID4
    column_name: str = Field(..., max_length=150)
    board_uuid: UUID4


class ColumnCreate(APIModel):
    column_name: str
    board_uuid: UUID4
