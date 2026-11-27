
"""Game session management for virtual simulations."""

import uuid
from datetime import datetime, timezone
from typing import Any


class GameSessionError(Exception):
    """Raised when a game session operation fails."""


class GameSessionManager:
    """Manage in-memory game sessions.

    Database persistence will be added in a later integration step.
    """

    VALID_STATUSES = {"ACTIVE", "COMPLETED", "CANCELLED"}

    def __init__(self):
        self._sessions: dict[str, dict[str, Any]] = {}

    def create_session(
        self,
        user_id: str,
        game_id: str,
    ) -> dict[str, Any]:
        """Create a new game session."""

        if not user_id or not game_id:
            raise GameSessionError("User ID and game ID are required")

        session_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()

        session = {
            "session_id": session_id,
            "user_id": user_id,
            "game_id": game_id,
            "status": "ACTIVE",
            "created_at": now,
            "updated_at": now,
            "result": None,
        }

        self._sessions[session_id] = session

        return session.copy()

    def get_session(self, session_id: str) -> dict[str, Any]:
        """Retrieve a session."""

        session = self._sessions.get(session_id)

        if session is None:
            raise GameSessionError("Game session not found")

        return session.copy()

    def complete_session(
        self,
        session_id: str,
        result: dict[str, Any],
    ) -> dict[str, Any]:
        """Mark a session as completed."""

        session = self._sessions.get(session_id)

        if session is None:
            raise GameSessionError("Game session not found")

        if session["status"] != "ACTIVE":
            raise GameSessionError("Session is not active")

        session["status"] = "COMPLETED"
        session["result"] = result
        session["updated_at"] = datetime.now(timezone.utc).isoformat()

        return session.copy()

    def cancel_session(self, session_id: str) -> dict[str, Any]:
        """Cancel an active session."""

        session = self._sessions.get(session_id)

        if session is None:
            raise GameSessionError("Game session not found")

        if session["status"] != "ACTIVE":
            raise GameSessionError("Session is not active")

        session["status"] = "CANCELLED"
        session["updated_at"] = datetime.now(timezone.utc).isoformat()

        return session.copy()

    def list_user_sessions(
        self,
        user_id: str,
    ) -> list[dict[str, Any]]:
        """List sessions belonging to a user."""

        return [
            session.copy()
            for session in self._sessions.values()
            if session["user_id"] == user_id
        ]
      
