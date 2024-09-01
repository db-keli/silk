"""
    This module contains a class for managing WebSocket connections
"""

from fastapi import WebSocket


class ConnectionManager:
    """
    This class manages WebSocket connections
    """

    def __init__(self):
        self.connections: list[dict[str, WebSocket]] = []

    async def connect(self, websocket: WebSocket, username):
        """
        Registers a new WebSocket connection and adds it to the list of connected clients.

        Args:
            websocket (WebSocket): The WebSocket object for the new connection.
            username (str): The username of the connected client.
        """
        await websocket.accept()
        self.connections.append({username: websocket})

    def disconnect(self, websocket: WebSocket, username):
        """
        Removes a WebSocket connection from the list of connected clients.

        Args:
            websocket (WebSocket): The WebSocket object for the connection to remove.
            username (str): The username of the connected client.
        """
        self.connections.remove({username: websocket})

    async def broadcast(self, data: dict, username: str):
        """
        Broadcasts a message to all clients with the given username.

        Args:
            data (dict): The data to be sent.
            username (str): The username of the clients to receive the message.
        """
        for connection in self.connections:
            if list(connection.keys())[0] == username:
                await list(connection.values())[0].send_json(data)


connection_manager = ConnectionManager()
