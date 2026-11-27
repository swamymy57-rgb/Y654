
"""Game result management for virtual simulations."""

import uuid
from datetime import datetime, timezone
from typing import Any


class GameResultError(Exception):
    """Raised when a game result operation fails."""


class GameResultManager:
    """Manage and retrieve game results."""

    def __init__(self):
        self._results: dict[str, dict[str, Any]] = {}

    def record_result(
        self,
        session_id: str,
        user_id: str,
        game_id: str,
        result_data: dict[str, Any],
    ) -> dict[str, Any]:
        """Record a result for a completed game session."""

        if not session_id or not user_id or not game_id:
            raise GameResultError(
                "Session ID, user ID and game ID are required"
            )

        if not isinstance(result_data, dict) or not result_data:
            raise GameResultError("Valid result data is required")

        result_id = str(uuid.uuid4())

        result = {
            "result_id": result_id,
            "session_id": session_id,
            "user_id": user_id,
            "game_id": game_id,
            "result_data": result_data.copy(),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        self._results[result_id] = result

        return result.copy()

    def get_result(self, result_id: str) -> dict[str, Any]:
        """Retrieve a result by ID."""

        result = self._results.get(result_id)

        if result is None:
            raise GameResultError("Game result not found")

        return result.copy()

    def get_session_result(
        self,
        session_id: str,
    ) -> dict[str, Any] | None:
        """Retrieve the result associated with a session."""

        for result in self._results.values():
            if result["session_id"] == session_id:
                return result.copy()

        return None

    def list_user_results(
        self,
        user_id: str,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        """List results belonging to a user."""

        if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1:
            raise GameResultError("Limit must be a positive integer")

        results = [
            result.copy()
            for result in self._results.values()
            if result["user_id"] == user_id
        ]

        results.sort(
            key=lambda item: item["created_at"],
            reverse=True,
        )

        return results[:min(limit, 100)]
      
