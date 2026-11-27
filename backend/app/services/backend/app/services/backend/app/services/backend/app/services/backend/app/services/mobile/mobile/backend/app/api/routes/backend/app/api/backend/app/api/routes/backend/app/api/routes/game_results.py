
"""Game results API routes."""

from fastapi import APIRouter, HTTPException, Query

from app.services.game_results import GameResultManager

router = APIRouter(
    prefix="/game-results",
    tags=["Game Results"],
)

result_manager = GameResultManager()


@router.post("/")
async def create_result(
    user_id: str,
    game_id: str,
    session_id: str,
    score: int = Query(default=0, ge=0),
    points_earned: int = Query(default=0, ge=0),
):
    """Record a game result."""
    try:
        result = result_manager.create_result(
            user_id=user_id,
            game_id=game_id,
            session_id=session_id,
            score=score,
            points_earned=points_earned,
        )

        return {
            "success": True,
            "result": result,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get("/{result_id}")
async def get_result(result_id: str):
    """Get a specific game result."""
    result = result_manager.get_result(result_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Game result not found",
        )

    return {
        "success": True,
        "result": result,
    }


@router.get("/user/{user_id}")
async def get_user_results(user_id: str):
    """Get all results for a user."""
    results = result_manager.get_user_results(user_id)

    return {
        "total": len(results),
        "results": results,
    }
  
