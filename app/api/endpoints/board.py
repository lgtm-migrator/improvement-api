from typing import List

from fastapi import APIRouter
from fastapi import Depends
from pydantic.types import UUID4
from starlette.responses import Response
from starlette.status import HTTP_404_NOT_FOUND

from app.api.dependancies import get_current_active_user
from app.crud.board import create_board
from app.crud.board import delete_board
from app.crud.board import get_user_board
from app.crud.board import get_user_boards
from app.crud.board import update_board
from app.models.board import Board
from app.models.board import BoardCreate
from app.models.user import User


board_router = APIRouter()


@board_router.post("/create", dependencies=[Depends(get_current_active_user)], response_model=Board)
async def create_new_board(board_data: BoardCreate):
    new_board = await create_board(board_data)

    return Board(**new_board)


@board_router.get("/list", response_model=List[Board])
async def list_user_boards(current_user: User = Depends(get_current_active_user)):
    user_boards = await get_user_boards(current_user.user_uuid)

    return user_boards


@board_router.get("/list/{board_uuid}", response_model=Board)
async def get_one_user_board(board_uuid: UUID4, current_user: User = Depends(get_current_active_user)):
    user_board = await get_user_board(current_user.user_uuid, board_uuid)

    return Board(**user_board) if user_board else Response(status_code=HTTP_404_NOT_FOUND)


@board_router.put("/update", response_model=Board)
async def update_user_board(updated_board_data: Board, current_user: User = Depends(get_current_active_user)):
    new_board = await update_board(updated_board_data, current_user.user_uuid)

    return Board(**new_board)


@board_router.delete("/delete/{board_uuid}")
async def delete_user_board(board_uuid: UUID4, current_user: User = Depends(get_current_active_user)):
    delete_board_response = await delete_board(board_uuid, current_user.user_uuid)

    return delete_board_response
