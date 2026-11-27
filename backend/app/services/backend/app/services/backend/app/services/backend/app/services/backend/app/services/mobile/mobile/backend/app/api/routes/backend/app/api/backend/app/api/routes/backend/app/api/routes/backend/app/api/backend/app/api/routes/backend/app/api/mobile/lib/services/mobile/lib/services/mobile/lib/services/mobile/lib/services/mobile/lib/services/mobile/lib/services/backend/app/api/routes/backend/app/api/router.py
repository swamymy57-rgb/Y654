
from fastapi import APIRouter

from app.api.routes import (
    health,
    users,
    auth,
    wallet,
    games,
    game_sessions,
    game_results,
    game_play,
    game_websocket,
)

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(users.router)
api_router.include_router(auth.router)
api_router.include_router(wallet.router)
api_router.include_router(games.router)
api_router.include_router(game_sessions.router)
api_router.include_router(game_results.router)
api_router.include_router(game_play.router)
api_router.include_router(game_websocket.router)
