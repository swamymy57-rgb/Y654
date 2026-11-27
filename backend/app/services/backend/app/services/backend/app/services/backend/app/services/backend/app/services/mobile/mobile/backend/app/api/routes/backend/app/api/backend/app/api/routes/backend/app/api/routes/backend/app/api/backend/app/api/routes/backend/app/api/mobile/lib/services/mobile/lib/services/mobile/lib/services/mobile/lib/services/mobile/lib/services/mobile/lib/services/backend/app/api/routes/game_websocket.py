
"""WebSocket route for live game updates."""

import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.game_websocket import GameWebSocketManager

router = APIRouter(tags=["Game WebSocket"])

manager = GameWebSocketManager()


@router.websocket("/ws/games/{user_id}")
async def game_websocket(
    websocket: WebSocket,
    user_id: str,
):
    await manager.connect(user_id, websocket)

    try:
        await websocket.send_json({
            "type": "connected",
            "message": "Game WebSocket connected",
            "user_id": user_id,
        })

        while True:
            message = await websocket.receive_text()

            try:
                data = json.loads(message)
            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error",
                    "message": "Invalid JSON message",
                })
                continue

            await websocket.send_json({
                "type": "message_received",
                "data": data,
            })

    except WebSocketDisconnect:
        await manager.disconnect(user_id, websocket)

    except Exception:
        await manager.disconnect(user_id, websocket)
        raise
      
