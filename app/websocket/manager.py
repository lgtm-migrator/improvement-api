from typing import List

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self, manager_id: int):
        self.manager_id = manager_id
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_json_data(self, data: str, websocket: WebSocket):
        await websocket.send_json(data)

    async def broadcast_json(self, data: str):
        for connection in self.active_connections:
            await connection.send_json(data)
