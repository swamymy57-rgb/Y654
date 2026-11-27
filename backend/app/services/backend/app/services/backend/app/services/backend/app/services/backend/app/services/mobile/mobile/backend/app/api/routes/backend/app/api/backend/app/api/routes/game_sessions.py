
"""Game session API routes."""

from fastapi import APIRouter, HTTPException

from app.services.game_sessions import GameSessionManager

router = APIRouter(
    prefix="/game-sessions",
    tags=["Game Sessions"],
)

session_manager = GameSessionManager()


@router.post("/")
async def create_session(user_id: str, game_id: str):
    """Create a new game session."""
    try:
        session = session_manager.create_session(
            user_id=user_id,
            game_id=game_id,
        )
        return {
            "success": True,
            "session": session,
        }
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get("/{session_id}")
async def get_session(session_id: str):
    """Get a game session."""
    session = session_manager.get_session(session_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Game session not found",
        )

    return {
        "success": True,
        "session": session,
    }


@router.post("/{session_id}/complete")
async def complete_session(session_id: str):
    """Complete a game session."""
    try:
        session = session_manager.complete_session(session_id)

        if session is None:
            raise HTTPException(
                status_code=404,
                detail="Game session not found",
            )

        return {
            "success": True,
            "session": session,
        }
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.post("/{session_id}/cancel")
async def cancel_session(session_id: str):
    """Cancel a game session."""
    session = session_manager.cancel_session(session_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Game session not found",
        )

    return {
        "success": True,
        "session": session,
    }


@router.get("/user/{user_id}")
async def get_user_sessions(user_id: str):
    """Get all sessions belonging to a user."""
    sessions = session_manager.list_user_sessions(user_id)

    return {
        "total": len(sessions),
        "sessions": sessions,
    }
  
