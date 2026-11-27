
"""Server-side virtual game engine.

Educational simulation only.
No real-money transactions.
"""

import secrets
from typing import Any


class GameEngineError(Exception):
    """Raised when a game engine operation fails."""


class DiceGameEngine:
    """Server-side dice simulation engine."""

    GAME_ID = "dice"
    GAME_NAME = "Dice Simulation"
    MIN_DICE_VALUE = 1
    MAX_DICE_VALUE = 6

    @classmethod
    def roll_dice(cls, number_of_dice: int = 2) -> dict[str, Any]:
        """Generate dice results using secure server-side randomness."""

        if not isinstance(number_of_dice, int) or isinstance(number_of_dice, bool):
            raise GameEngineError("Number of dice must be an integer")

        if number_of_dice < 1 or number_of_dice > 6:
            raise GameEngineError(
                "Number of dice must be between 1 and 6"
            )

        dice = [
            secrets.randbelow(cls.MAX_DICE_VALUE)
            + cls.MIN_DICE_VALUE
            for _ in range(number_of_dice)
        ]

        return {
            "game_id": cls.GAME_ID,
            "game_name": cls.GAME_NAME,
            "dice": dice,
            "total": sum(dice),
            "number_of_dice": number_of_dice,
            "minimum_possible_total": number_of_dice,
            "maximum_possible_total": number_of_dice * 6,
        }


def get_available_games() -> list[dict[str, str]]:
    """Return available simulation games."""

    return [
        {
            "game_id": "dice",
            "name": "Dice Simulation",
            "category": "MINI_GAME",
            "status": "ACTIVE",
        }
    ]


def play_game(game_id: str) -> dict[str, Any]:
    """Execute a supported virtual simulation game."""

    if game_id != DiceGameEngine.GAME_ID:
        raise GameEngineError("Game not found or not supported")

    return DiceGameEngine.roll_dice()
  
