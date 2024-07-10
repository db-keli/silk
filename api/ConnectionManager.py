from fastapi import WebSocket

class ConnectionManager:

    def __init__(self):
        self.connections: list[dict[str,WebSocket]] = []

    async def connect(self, websocket: WebSocket, username):
        await websocket.accept()
        self.connections.append({username:websocket})

    def disconnect(self, websocket: WebSocket, username):
        self.connections.remove({username:websocket})
    async def broadcast(self, data: dict, username: str):
        for connection in self.connections:
            if list(connection.keys())[0] == username:
                await list(connection.values())[0].send_json(data)


connection_manager = ConnectionManager()