
from fastapi import APIRouter

from app.api.routes import (
    health,
    users,
    auth,
    wallet,
    games,
)

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(users.router)
api_router.include_router(auth.router)
api_router.include_router(wallet.router)
api_router.include_router(games.router)
