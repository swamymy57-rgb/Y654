
"""Game play API routes."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.game_engine import DiceGameEngine

router = APIRouter(
    prefix="/game-play",
    tags=["Game Play"],
)

game_engine = DiceGameEngine()


class DicePlayRequest(BaseModel):
    bet_points: int = Field(gt=0, le=1000)


@router.post("/dice")
async def play_dice(request: DicePlayRequest):
    """Play a virtual dice game."""
    try:
        result = game_engine.play_game(
            bet_points=request.bet_points
        )

        return {
            "success": True,
            "game": "dice",
            "result": result,
            "virtual_points_only": True,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get("/available-games")
async def available_games():
    """Get available game engine information."""
    return {
        "games": game_engine.get_available_games()
    }
  
