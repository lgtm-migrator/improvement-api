from typing import Any
from typing import Dict
from typing import List

from fastapi import WebSocket
from fastapi.exceptions import HTTPException

from app.api.dependancies import get_current_user


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket, init_data):
        await websocket.accept()
        self.active_connections.append(websocket)

        auth_data = await websocket.receive_json()
        auth = auth_data.get("type") == "authenticate"

        if not auth:
            self.disconnect(websocket)

        # check auth on connect
        token = auth_data.get("data")

        try:
            await get_current_user(token)
            if init_data:
                await self.send_json_data(init_data, websocket)
        except HTTPException:
            self.disconnect(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_json_data(self, data: str | Dict[str, Any], websocket: WebSocket):
        await websocket.send_json(data)
