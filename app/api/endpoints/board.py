import json
from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from pydantic.types import UUID4
from starlette.responses import Response
from starlette.status import HTTP_404_NOT_FOUND

from app.api.dependancies import get_current_active_user
from app.crud.board import create_board
from app.crud.board import delete_board
from app.crud.board import get_user_board
from app.crud.board import get_user_boards
from app.crud.board import update_board
from app.crud.column import create_column_and_update_board_column_order
from app.crud.column import delete_column_and_update_board_column_order
from app.crud.column import get_board_columns_and_column_order
from app.crud.column import update_column_and_update_board_column_order
from app.models.board import Board
from app.models.board import BoardCreate
from app.models.column import Column
from app.models.column import ColumnCreate
from app.models.user import User
from app.websocket import ConnectionManager


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


async def get_board_data(board_uuid: UUID4):
    board_data_records = await get_board_columns_and_column_order(board_uuid)

    if board_data_records:
        board_columns = [json.loads(Column(**column).json()) for column in board_data_records]

        column_order_uuid_list = board_data_records[0]["column_order"]
        column_order = [str(col_uuid) for col_uuid in column_order_uuid_list]

        sorted_board_columns = sorted(board_columns, key=lambda column: column_order.index(column.get("column_uuid")))

        board_data = {"column_order": column_order, "columns": sorted_board_columns}
    else:
        board_data = {"column_order": [], "columns": []}

    return board_data


@board_router.websocket("/ws/{board_uuid}")
async def board_ws_endpoint(websocket: WebSocket, board_uuid: UUID4):
    board_ws_manager = ConnectionManager(manager_id=board_uuid)
    init_board_data = await get_board_data(board_uuid)

    await board_ws_manager.connect(websocket, init_board_data)

    try:
        while websocket in board_ws_manager.active_connections:
            data_dict = await websocket.receive_json()
            crud_type = data_dict.get("crud")

            if crud_type == "create":
                column_create_data = data_dict.get("data")
                new_column_order = column_create_data.get("column_order")

                await create_column_and_update_board_column_order(
                    ColumnCreate(**column_create_data.get("new_column")), new_column_order
                )

            if crud_type == "update":
                column_update_data = data_dict.get("data")
                new_column_order = column_update_data.get("column_order")

                await update_column_and_update_board_column_order(
                    Column(**column_update_data.get("updated_column")), new_column_order
                )

            if crud_type == "delete":
                delete_column_uuid = data_dict.get("data").get("column_uuid")
                new_column_order = data_dict.get("data").get("column_order")

                await delete_column_and_update_board_column_order(board_uuid, delete_column_uuid, new_column_order)

            if crud_type:
                # update board data to everyone who's on the board
                updated_board_data = await get_board_data(board_uuid)
                await board_ws_manager.broadcast_json(updated_board_data)

    except WebSocketDisconnect:
        board_ws_manager.disconnect(websocket)
