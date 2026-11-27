
"""Game lobby catalog for the virtual simulation platform."""

from typing import Any


GAME_CATALOG: list[dict[str, Any]] = [
    {
        "game_id": "dice",
        "name": "Dice Arena",
        "description": "Enjoy a virtual dice rolling simulation.",
        "category": "MINI_GAMES",
        "icon": "dice",
        "theme": "purple",
        "status": "ACTIVE",
        "featured": True,
        "players_label": "Single Player",
        "sort_order": 1,
    },
    {
        "game_id": "number_guess",
        "name": "Number Challenge",
        "description": "Test your number guessing skills.",
        "category": "MINI_GAMES",
        "icon": "hash",
        "theme": "blue",
        "status": "COMING_SOON",
        "featured": True,
        "players_label": "Single Player",
        "sort_order": 2,
    },
    {
        "game_id": "memory",
        "name": "Memory Match",
        "description": "Challenge your memory with matching cards.",
        "category": "PUZZLE_GAMES",
        "icon": "brain",
        "theme": "pink",
        "status": "COMING_SOON",
        "featured": True,
        "players_label": "Single Player",
        "sort_order": 3,
    },
    {
        "game_id": "color_match",
        "name": "Color Match",
        "description": "Explore a colorful matching challenge.",
        "category": "PUZZLE_GAMES",
        "icon": "palette",
        "theme": "orange",
        "status": "COMING_SOON",
        "featured": False,
        "players_label": "Single Player",
        "sort_order": 4,
    },
    {
        "game_id": "card_memory",
        "name": "Card Memory",
        "description": "Find matching cards in this memory game.",
        "category": "CARD_GAMES",
        "icon": "layers",
        "theme": "green",
        "status": "COMING_SOON",
        "featured": False,
        "players_label": "Single Player",
        "sort_order": 5,
    },
]


class GameLobbyService:
    """Provide game catalog and lobby filtering."""

    @staticmethod
    def get_categories() -> list[dict[str, str]]:
        return [
            {"category_id": "ALL", "name": "All Games"},
            {"category_id": "MINI_GAMES", "name": "Mini Games"},
            {"category_id": "PUZZLE_GAMES", "name": "Puzzle Games"},
            {"category_id": "CARD_GAMES", "name": "Card Games"},
        ]

    @staticmethod
    def get_all_games() -> list[dict[str, Any]]:
        return sorted(
            [game.copy() for game in GAME_CATALOG],
            key=lambda game: game["sort_order"],
        )

    @staticmethod
    def get_featured_games() -> list[dict[str, Any]]:
        return [
            game.copy()
            for game in GameLobbyService.get_all_games()
            if game["featured"]
        ]

    @staticmethod
    def get_active_games() -> list[dict[str, Any]]:
        return [
            game.copy()
            for game in GameLobbyService.get_all_games()
            if game["status"] == "ACTIVE"
        ]

    @staticmethod
    def get_games_by_category(
        category: str,
    ) -> list[dict[str, Any]]:
        if category == "ALL":
            return GameLobbyService.get_all_games()

        return [
            game.copy()
            for game in GameLobbyService.get_all_games()
            if game["category"] == category
        ]

    @staticmethod
    def search_games(query: str) -> list[dict[str, Any]]:
        if not query or not query.strip():
            return GameLobbyService.get_all_games()

        search_text = query.strip().casefold()

        return [
            game.copy()
            for game in GameLobbyService.get_all_games()
            if search_text in game["name"].casefold()
            or search_text in game["description"].casefold()
            or search_text in game["category"].casefold()
        ]

    @staticmethod
    def get_game(game_id: str) -> dict[str, Any] | None:
        for game in GAME_CATALOG:
            if game["game_id"] == game_id:
                return game.copy()

        return None

    @staticmethod
    def get_lobby_data() -> dict[str, Any]:
        return {
            "title": "Virtual Games Arena",
            "subtitle": "Play. Explore. Challenge Yourself.",
            "currency": "VPOINT",
            "categories": GameLobbyService.get_categories(),
            "featured_games": GameLobbyService.get_featured_games(),
            "active_games": GameLobbyService.get_active_games(),
            "all_games": GameLobbyService.get_all_games(),
            "total_games": len(GAME_CATALOG),
        }
      
