
"""WebSocket connection manager for virtual games."""

import asyncio
import logging
from collections import defaultdict

from fastapi import WebSocket, WebSocketDisconnect


logger = logging.getLogger(__name__)


class GameWebSocketManager:
    """Manage live WebSocket connections."""

    def __init__(self):
        self._connections: dict[str, set[WebSocket]] = defaultdict(set)
        self._lock = asyncio.Lock()

    async def connect(
        self,
        user_id: str,
        websocket: WebSocket,
    ) -> None:
        """Accept and register a user connection."""

        if not user_id:
            raise ValueError("User ID is required")

        await websocket.accept()

        async with self._lock:
            self._connections[user_id].add(websocket)

        logger.info("WebSocket connected for user %s", user_id)

    async def disconnect(
        self,
        user_id: str,
        websocket: WebSocket,
    ) -> None:
        """Remove a disconnected connection."""

        async with self._lock:
            connections = self._connections.get(user_id)

            if connections is not None:
                connections.discard(websocket)

                if not connections:
                    self._connections.pop(user_id, None)

        logger.info("WebSocket disconnected for user %s", user_id)

    async def send_to_user(
        self,
        user_id: str,
        message: dict,
    ) -> None:
        """Send an update to all connections of one user."""

        async with self._lock:
            connections = list(self._connections.get(user_id, set()))

        disconnected = []

        for websocket in connections:
            try:
                await websocket.send_json(message)
            except (WebSocketDisconnect, RuntimeError, OSError):
                disconnected.append(websocket)

        for websocket in disconnected:
            await self.disconnect(user_id, websocket)

    async def broadcast(
        self,
        message: dict,
    ) -> None:
        """Broadcast an update to all connected users."""

        async with self._lock:
            connections = [
                (user_id, websocket)
                for user_id, sockets in self._connections.items()
                for websocket in list(sockets)
            ]

        disconnected = []

        for user_id, websocket in connections:
            try:
                await websocket.send_json(message)
            except (WebSocketDisconnect, RuntimeError, OSError):
                disconnected.append((user_id, websocket))

        for user_id, websocket in disconnected:
            await self.disconnect(user_id, websocket)

    async def connection_count(self) -> int:
        """Return the total active connection count."""

        async with self._lock:
            return sum(
                len(connections)
                for connections in self._connections.values()
            )


game_websocket_manager = GameWebSocketManager()
      
